#include <assert.h>
#include <stdio.h>
#include "testgen.h"

int main(int argc, char **argv) {
    size_t i;
    for (i = 0; i < sizeof(tests) / sizeof(struct test); ++i) {
        struct test *test = &tests[i];

        printf("Testing %s\n", test->name);

        test->setup();
        int opA = test->opA();
        int opAB = test->opB();
        test->cleanup();
        test->setup();
        int opB = test->opB();
        int opBA = test->opA();
        test->cleanup();

        assert(opA == opBA);
        assert(opB == opAB);
    }
}
