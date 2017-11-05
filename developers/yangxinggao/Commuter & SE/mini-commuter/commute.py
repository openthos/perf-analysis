import z3
import copy

#Hold a counter '#' to record 'name'
#Give a thesaurus of 'name' with 'name.#'
def fresh_name(name, map={}):
    if name in map:
        map[name] += 1
        return "{}.{}".format(name, map[name])
    map[name] = 0
    return fresh_name(name)

def If(cond, a, b):
    if hasattr(a, 'ite'):
        return a.ite(cond, b)
    return z3.If(cond, a, b)


class Result(object):
    def __init__(self, ret, state):
        self.ret = ret
        self.state = state

    def copy(self):
        return copy.copy(self)

    def ite(self, cond, other):
        new = self.copy()
        new.ret = If(cond, self.ret, other.ret)
        new.state = If(cond, self.state, other.state)
        return new


class State(object):
    def __init__(self):
	# a rename of 'inode_nlink'
        self.inode_nlink = z3.Function(fresh_name('inode_nlink'), z3.IntSort(), z3.IntSort())
        self.fname_inode = z3.Function(fresh_name('fname_inode'), z3.IntSort(), z3.IntSort())

    def copy(self):
        return copy.copy(self)

    def write_nlink(self, ino, nlink):
        new = self.copy()
        new.inode_nlink = lambda x: If(x == ino, nlink, self.inode_nlink(x))
        return new

    def write_dir(self, fname, ino):
        new = self.copy()
        new.fname_inode = lambda x: If(x == fname, ino, self.fname_inode(x))
        return new

    def __eq__(self, other):

        ino = z3.Int(fresh_name('ino'))
        ino_match =  z3.ForAll([ino],
                               z3.And(self.inode_nlink(ino) == other.inode_nlink(ino)))

        fname = z3.Int(fresh_name('fname'))
        fname_match = z3.ForAll([fname],
                                 self.fname_inode(fname) == other.fname_inode(fname))
        return z3.And(ino_match, fname_match)

    def ite(self, cond, other):
        new = self.copy()
        new.inode_nlink = lambda x: If(cond, self.inode_nlink(x), other.inode_nlink(x))
        new.fname_inode = lambda x: If(cond, self.fname_inode(x), other.fname_inode(x))
        return new

    # API

    def rename(self, srcname, dstname):
        oldstate = self
        src_ino = oldstate.fname_inode(srcname)
        srcexists = src_ino != z3.IntVal(0)
        dst_ino = oldstate.fname_inode(dstname)
        dstexists = dst_ino != z3.IntVal(0)

        return If(z3.Not(srcexists), Result(z3.IntVal(-1), oldstate),
               If(srcname == dstname, Result(z3.IntVal(0), oldstate),
               If(dstexists, Result(z3.IntVal(0), oldstate.write_nlink(dst_ino, self.inode_nlink(dst_ino) - z3.IntVal(1))
                                                          .write_dir(dstname, src_ino)
                                                          .write_dir(srcname, z3.IntVal(0))),
               Result(z3.IntVal(0), oldstate.write_dir(dstname, src_ino)
                                            .write_dir(srcname, z3.IntVal(0))))))


def commutes(state, opA, argsA, opB, argsB):

    resA = opA(*([state] + argsA))
    resAB = opB(*([resA.state] + argsB))

    resB = opB(*([state] + argsB))
    resBA = opA(*([resB.state] + argsA))

    return z3.And(resAB.state == resBA.state, resA.ret == resBA.ret, resB.ret == resAB.ret)

tests = []

def gen_rename_test(testname, model, state, srcA, dstA, srcB, dstB):

    tests.append({
        "name": testname,
        "cleanup": "cleanup_rename_rename_{}".format(testname),
        "opA": "test_rename_rename_opA_{}".format(testname),
        "opB": "test_rename_rename_opB_{}".format(testname),
        "setup": "setup_rename_rename_{}".format(testname),
    })

    srcAinode = model.eval(state.fname_inode(srcA)).as_long()
    srcBinode = model.eval(state.fname_inode(srcB)).as_long()
    dstAinode = model.eval(state.fname_inode(dstA)).as_long()
    dstBinode = model.eval(state.fname_inode(dstB)).as_long()
    gen = {'gen': "void setup_rename_rename_{}() {{\n".format(testname)}
    def mkinode(ino):
        if ino != 0:
            gen['gen'] += '  close(open("__i{}", O_CREAT|O_RDWR, 0666));\n'.format(ino)
    mkinode(srcAinode)
    mkinode(srcBinode)
    mkinode(dstAinode)
    mkinode(dstBinode)
    def link(fname, ino):
        if ino != 0:
            gen['gen'] += '  link("__i{}", "f{}");\n'.format(ino, fname)
    link(model.eval(srcA).as_long(), srcAinode)
    link(model.eval(srcB).as_long(), srcBinode)
    link(model.eval(dstA).as_long(), dstAinode)
    link(model.eval(dstB).as_long(), dstBinode)
    gen['gen'] += '}}\nint test_rename_rename_opA_{}() {{\n'.format(testname)
    gen['gen'] += '  return rename("f{}", "f{}");\n'.format(model.eval(srcA).as_long(), model.eval(dstA).as_long())
    gen['gen'] += '}}\nint test_rename_rename_opB_{}() {{\n'.format(testname)
    gen['gen'] += '  return rename("f{}", "f{}");\n}}'.format(model.eval(srcB).as_long(), model.eval(dstB).as_long())
    gen['gen'] += '\nvoid cleanup_rename_rename_{}() {{\n'.format(testname)
    def unlink(n):
        gen['gen'] += '  unlink("{}");\n'.format(n)
    unlink("__i{}".format(srcAinode))
    unlink("__i{}".format(srcBinode))
    unlink("__i{}".format(dstAinode))
    unlink("__i{}".format(dstBinode))
    unlink("f{}".format(model.eval(srcA).as_long()))
    unlink("f{}".format(model.eval(srcB).as_long()))
    unlink("f{}".format(model.eval(dstA).as_long()))
    unlink("f{}".format(model.eval(dstB).as_long()))
    gen['gen'] += '}\n'
    return gen['gen']


state = State()
srcA, dstA, srcB, dstB = z3.Ints('srcA dstA srcB dstB')
comm = commutes(state, State.rename, [srcA, dstA], State.rename, [srcB, dstB])

s = z3.Solver()
s.add(comm)

condsA = [z3.Not(srcA != z3.IntVal(0)), srcA == dstA, dstA != z3.IntVal(0)]
condsB = [z3.Not(srcB != z3.IntVal(0)), srcB == dstB, dstB != z3.IntVal(0)]

print '#include <unistd.h>'
print '#include <fcntl.h>'

for i in range(0, len(condsA)):
    for j in range(0, len(condsB)):
        path = z3.And(z3.Not(condsA[i]), *condsA[:i])
        path = z3.And(path, z3.Not(condsB[j]), *condsB[:j])
        s.push()
        s.add(path)
        print '/* {} */'.format(z3.simplify(path))
        if s.check() == z3.sat:
            model = s.model()
            name = "{}_{}".format(i,j)
            print gen_rename_test("{}_{}".format(i,j), model, state, srcA, dstA, srcB, dstB)
            print ''
        s.pop()

print """
struct test {
    const char *name;
    void (*setup)(void);
    int (*opA)(void);
    int (*opB)(void);
    void (*cleanup)(void);
};
"""

print 'static struct test tests[] = {'
for test in tests:
    print '  {{ .name = "{}", .setup = &{}, .cleanup = &{}, .opA = &{}, .opB = &{} }},'.format(
        test['name'], test['setup'], test['cleanup'], test['opA'], test['opB'])
print '};'

print
