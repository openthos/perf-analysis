Copied from [xiw cse551](http://courses.cs.washington.edu/courses/cse551/17wi/mini/commuter)

# mini-Commuter

This demo of Commuter finds the conditions under which the rename operation
commutes with other rename, and uses these conditions to generate some simple
tests in C to test the commutativity.

`make test` Runs the tests, first by running python on `commute.py` and including
the resulting header file output into `tester.c`, then compiling and running `tester.c`.

`testgen.h` Contains the generated tests.

The tests simply run both operations and confirm that the return values are the same for each.
(It doesn't check that the directory state is the same yet, but that should be simple to add.)
