# Scheme Concepts

The following chapters introduce fundamental concepts of Scheme.  To some extent
this introduction is independent from LilyPond, as most of the concepts are
general Scheme techniques.  However, they are all taken from the LilyPond
perspective.

We start with discussing *data types*, followed by a sequence of discussions of
more complex concepts and techniques.

# Data Types

When talking to a computer there's no room for ambiguity.  Approaching a
computational task with irony is almost bound to fail, as the programming
language will always want to know what it really *is* you are talking about.
Therefore in programming languages each value has a *type*, and this is not
different in Scheme.  If a function processes a number you have to *give* it a
number, sometimes you even have to make a difference between, say, integer and
real numbers, e.g. between `1` and `1.0`. And so on.

Scheme is extremely flexible and permeable with regard to type. If you have an
expression like

```
(some-procedure arg1 arg2)
```

then Scheme will not check in any way what types the values `arg1` and `arg2`
have.  Any type mismatch will only become visible upon the procedure application
within the expression:

```
guile> (+ "1" "2")
ERROR: In procedure +:
ERROR: Wrong type argument in position 1: "1"
ABORT: (wrong-type-arg)
```

You can compare this behaviour with other programming languages.  In “strongly
typed” languages like Java or C++ the function interface would already act as a
shield against arguments with wrong types.  The `"1"` and `"2"` wouldn't even
reach the `+`, so to say.  Other languages, like e.g. Python or JavaScript will
try to make the best out of it. In the example they would both *concatenate* the
two digits and return `"12"`.

So Scheme doesn't check the type of an argument passed into an expression but
doesn't do anything to help with improper types either.  This is an important
characteristic because instead of the three literal elements the expression
could equally consist of expressions themselves whose resulting type will only
be known at runtime:

```
((return-a-procedure) (return-arg1) (return-arg2))
```

So Scheme is open for very elegant and concise dynamic programming tricks.
Admittedly this is still pretty abstract.  What you should remember at *this*
point is that the type of an expression's elements is not enforced by Scheme,
but that passing arguments of unsuitable type will cause errors during procedure
application.

#### Predicates

Of course it's not a good idea to simply throw values at a procedure and wait for
errors to occur or not.  In Scheme it is therefore very common to check the type
of a value before using it.  As a response the program will either reject the
value or  select suitable code to be executed. This will be discussed in a later
chapter on [conditionals](../conditionals.html).

Scheme does not have a (regular) way of revealing the type of something directly
(which is part of the open characteristic).  The approach taken instead is
something like asking “is this object behaving like a certain type, does it have
the right properties?” This is achieved using *predicates*.  Predicates are
procedures that take an object and return *true* if the object matches a certain
definition or *false* otherwise.  By convention the name of a predicate has a
trailing question mark, so for example `number?` checks if a given value is a
number etc.

```
guile> (string? "I'm a string")
#t

guile> (integer? 4.2)
#f

guile> (boolean? #f)
#t

guile> (boolean? "true")
#f
```

We will come back to the topic of predicates after having discussed writing
procedures, for now we will continue with the discussion of a number of basic
data types.

If at some point you might want to get more in-depth information about simple
data types you should consult the
[reference](https://www.gnu.org/software/guile/manual/html_node/Simple-Data-Types.html#Simple-Data-Types)
in the Guile manual.
