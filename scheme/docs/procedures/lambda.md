# The `lambda` Expression

As said in the previous introduction `lambda` is an expression that creates - or
*evaluates to* - a procedure.  It has the general form

```
(lambda <formals> <expressions>)
```

`<formals>` is where the *arguments* are specified that the procedure will be
applied to.  There are three forms for this specification, and I will discuss
the differences in the next chapter.  In this chapter we're using the most common
form.

`<expressions>` is an arbitrary number of expressions that is evaluated in
sequence.  As usual the value of the last expression will become the value of
the procedure as a whole.  But let's consider this with an example:

### Creating a procedure

```
guile> (lambda (x) (+ x x))
#<procedure #f (x)>
```

The printed result (remember that the Scheme console immediately prints the
*value* of the expression typed in) gives us three informations:  first that it
is a *procedure* that we've created, second that it does *not* have a name (the
`#f`) and finally the expected argument list.  What it *doesn't* tell us is how
the procedure creation works.  In order to investigate this we reformat the
expression:

```
(lambda
  (x)
  (+ x x)
)
```

The first argument to `lambda` is `(x)`.  This tells the parser that the
procedure will accept exactly one argument, and this argument will be visible by
the name of `x` in the body of the procedure.  When the formals are written as a
list like here then each element of the list represents the name of one actual
parameter the procedure expects.

The body of the procedure consists of the single expression `(+ x x)` which
simply takes the argument `x` and adds it to itself.  The result of this
“duplication” will become the value of the whole procedure.

#### Parameter types

Here we can see something in action that has been mentioned much earlier in the
introduction to [data types](../index.html): Scheme does *not* impose any
restriction on the data type that is passed to the procedure, in fact a value of
arbitrary type may be locally *bound* to the name `x`.  But as we use `x` in the
expression `(+ x x)` it is clear that only types can be accepted which the `+`
operation can be applied to.  Scheme doesn't “guard” procedures against
unsuitable parameters through type-checking, which has its pros and cons.  The
problem can be that possible errors occur within the procedure and not at its
interface, which can make them harder to pinpoint.  On the other hand this opens
a lot of potential for “polymorphism”, that is the possibility to write a single
interface that behaves differently depending on the type of arguments that are
passed into it.  We will discuss this aspect in a [later
chapter](parameter-types.html).

### *Using* the Procedure

Now we have created a procedure, but it doesn't *do* anything yet, so how can we
make use of it? Correct, by *applying* it. Our expression *is* a procedure
expecting one argument, so we can use it like one: `(procedure arg1)`. Usually
when applying a procedure we refer to it by its *name*, but that name doesn't do
anything else than *evaluating to* the procedure itself, so for Scheme it
doesn't make a difference if we use the name or its definition:

```
guile>
(
 (lambda (x) (+ x x))
 12
)
24
```

We have an enclosing pair of parens to denote the *procedure application*, then
the definition of the procedure in the first position, followed by a number as
the single argument.  The expression correctly evaluates to 24, which
corresponds to 12 + 12.  You should clearly see that this whole `lambda`
expression is in the place where we'd normally place a procedure name, like

```
guile>
(
 random
 12
)
7
```

Of course it rarely makes sense to create a procedure just for a single
application, but for now we'll stick to that approach and dedicate a full
chapter to the different ways of binding and reusing procedures.

### Multiple Paramters and Expressions

Our first procedure accepted a single argument, and its body also consisted of a
single expression.  But of course multiple arguments and epxressions can be
handled:

```
guile>
(lambda (x y)
  (display (format "X: ~a\n" x))
  (display (format "Y: ~a\n" y))
  (+ x y))
#<procedure #f (x y)>
```

This procedure will accept two parameters, which will be visible by the names
`x` and `y` in the procedure body.  This time the body evaluates three
expressions in sequence: the first two expressions print the input arguments to
the console while the third and last one evaluates the sum of the parameters and
returns that as the whole procedure's value.

We can apply this procedure the same way as the previous one, although it starts
to get awkward doing that in the Scheme REPL that doesn't forgive any typing
errors:

```
guile>
((lambda (x y)
    (display (format "X: ~a\n" x))
    (display (format "Y: ~a\n" y))
    (+ x y))
  9
  12)
X: 9
Y: 12
21
```

In the last three lines we can see the printout from the `display` procedure and
finally the *value* of the expression.  *(You may make a mental note of the
characteristic double paren at the opening of this expression.)*
