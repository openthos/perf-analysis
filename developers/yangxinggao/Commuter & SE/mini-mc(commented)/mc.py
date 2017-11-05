# -*- coding: utf-8 -*-

# Copyright (c) 2015 Xi Wang
#
# This file is part of the UW CSE 551 lecture code.  It is freely
# distributed under the MIT License.

# ---------------------------------------------------------------
# symbolic
# ---------------------------------------------------------------

from mc_util import *

def sched_fork(self):
  pid = os.fork()
  if pid:
    solver.add(self)
    r = True
    mc_log("assume (%s)" % (str(self),))
  else:
    solver.add(Not(self))
    r = False
    mc_log("assume ¬(%s)" % (str(self),))
  if solver.check() != sat:
    mc_log("unreachable")
    sys.exit(0)
  return r

setattr(BoolRef, "__bool__", sched_fork)
setattr(BoolRef, "__nonzero__", getattr(BoolRef, "__bool__"))

# ---------------------------------------------------------------
# concolic
# ---------------------------------------------------------------

def sched_flip(self, trace):
  print("#######")
  print "Meet an condition:", self
  solver.push()
  solver.add(self)
  r = (solver.check() == sat)
  solver.pop()
  if r:
    cond = self
  else:
    cond = Not(self)
  trace.append(cond)
  print "The new trace:", trace
  mc_log("%s: %s" % (self, r))
  print("#######")
  return r

def mc_fuzz(f, init_keys, init_vals, cnt = 0):
  assert len(init_keys) == len(init_vals)
  mc_log("=" * 60)
  mc_log("#%s: %s" % (cnt, ', '.join(["%s = %s" % (k, v) for k, v in zip(init_keys, init_vals)])))

  trace = []
  setattr(BoolRef, "__bool__", lambda self: sched_flip(self, trace))
  setattr(BoolRef, "__nonzero__", getattr(BoolRef, "__bool__"))

  print "SOLVER: the old solver: ", solver.assertions()
  solver.push()
  for k, v in zip(init_keys, init_vals):
    solver.add(k == v)
    #add the init value here
  print "Run f() with the new value" 	
  print "SOLVER: add the init values into solver: ", solver.assertions()
  try:
    f()
    print "Running f(): DONE!"
  except:
    typ, value, tb = sys.exc_info()
    sys.excepthook(typ, value, tb.tb_next)
  solver.pop()
  print "SOLVER:pop back: ", solver.assertions()
  delattr(BoolRef, "__bool__")
  delattr(BoolRef, "__nonzero__")

  # this path done
  if trace:
    solver.add(Not(And(*trace)))
    print "The trace after running f(): ", trace
    print "SOLVER: add the neg trace into solver:", solver.assertions()
  # choose a new path
  while trace:
    solver.push()
    solver.add(Not(trace[-1]))
    trace = trace[:-1]
    print "trace pop out:",trace
    solver.add(*trace)
    print "SOLVER:check the new path reachable:", solver.assertions()
    r = solver.check()
    solver.pop()
    if r == sat:
      m = solver.model()
      new_init_vals = [m.eval(k, model_completion=True) for k in init_keys]
      cnt = mc_fuzz(f, init_keys, new_init_vals, cnt + 1)

  return cnt
