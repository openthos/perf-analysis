all: tester

testgen.h: commute.py
	python2 $^ > $@

tester: tester.c testgen.h
	cc $< -o $@

test: tester
	rm -rf .test
	mkdir .test
	cd .test; ../tester
	rm -rf .test

clean:
	rm -rf .test
	rm -f tester testgen.h

.PHONY: all clean test
