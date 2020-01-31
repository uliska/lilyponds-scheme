# Binding Procedures

Procedures are *objects* like everything else in Scheme, and therefore
procedures can be *bound* to names just like any other variable.  Not all
programming languages support this handling of procedures as [first-class
functions](https://en.wikipedia.org/wiki/First-class_function).  This typical
concept of *functional programming* languages allows to pass functions as
arguments to and return them from functions.  And just as with other objects we
can bind procedures locally or globally.


### Top-level Binding of Procedures

When a procedure has been bound to a global name it can be used from anywhere in
the program, just like the built-in procedures or those provided by LilyPond.
Basically we do exactly the same as with other
[top-level](../binding/top-level.html) bindings of variables:

```
(define <name> <object>)
```

with the `<object>` being the `lambda` expression:

```
guile>
(define my-proc
  (lambda (x y)
     (+ x y)))
guile> my-proc
#<procedure my-proc (x y)>
```

The `lambda` expression creates a procedure adding its two arguments, and this
procedure is now bound to the (global) name `my-proc`.  So from now on we can
*use* `my-proc` just like any other procedure (including errors ...):

```
guile> (my-proc 2 3)
5
guile> (my-proc 2)
ERROR: Wrong number of arguments to #<procedure my-proc (x y)>
ABORT: (wrong-number-of-args)
```

#### Alternative Syntax for Top-level Binding

The above example was the very “literal” binding of a `lambda` expression to a
name, and this can be done with either of the three forms of `lambda`.  But
there's also a shorthand notation that is equivalent but that you'll be likely
to encounter (and use) more often.

The previous example could equally have been written as

```
guile>
(define (my-proc x y)
  (+ x y))
guile> my-proc
#<procedure my-proc (x y)>
guile> (my-proc 2 3)
5
```

The general form for this is that the following are equivalent:

```
(define <var-0> (lambda (<var-1> ... <var-n>) <exp1> ...))
(define (<var-0> <var-1> ... <var-n>) <exp1> ...)
```

`<var-0>` will be the name to which the procedure is bound while the remaining
`var`s represent the actual arguments.

---

There are shorthands for the other two forms of `lambda` expressions as well,
but I'll just mention them shortly, as the above seems to be the most common
form by far.

The form accepting an arbitrary list of arguments as its corresponding shortcut
like this:

```
(define <var-0> (lambda <var-1> <exp1> ...))
(define (<var-0> . <var-1>) <exp1> ...)

guile>
guile> (define
(my-name . args)
(length args))
guile> my-name
#<procedure my-name args>
guile> (my-name 'a 'b 'c)
3
```

Finally, the hybrid form looks like this:

```
(define <var-0> (lambda <var-1> ... <var-n> . <var-rest>) <exp1-> ...)
(define (<var-0> <var-1> ... <var-n> . <var-rest>) <exp1> ...)

guile>
(define
  (my-name arg-1 arg-2 . arg-rest)
  (length arg-rest))
guile> my-name
#<procedure my-name (arg-1 arg-2 . arg-rest)>
guile> (my-name 1 2 3 4 5)
3
```

### Local Binding of Procedures

We can bind procedures in a `let` block to reuse not only *values* but actual
*functionality*.  Basically it is all the same as what we've seen about `lambda`
expressions and variable bindings, so I think we're at a point where I don't
have to go into that much depth anymore.  However, we can take the opportunity
to practise and demonstrate a few other things in context instead.  What we can
do for the first time is using data that has actually been passed as
*arguments*. We will create a named procedure that accepts two values, a color
and a damping value to provide shaded versions of colors that can be applied as
LilyPond overrides.

```lilypond
#(define damp-color
   (lambda (color damping)
     (let ((damp-element
            (lambda (elem)
              (/ (elem color) damping))))
       (list
        (damp-element first)
        (damp-element second)
        (damp-element third)))))

{
  c'
  \override NoteHead.color = #(damp-color red 1.2)
  d'
  \override NoteHead.color = #(damp-color blue 2)
  e'
}
```

The procedure `damp-color` is created accepting two arguments, the color `color`
and the factor `damping`.  Inside this procedure we create a local binding with
`let`, binding a `lambda` expression to the name `damp-element`.  In the body of
the `let` expression we create a list with three elements that make use of this
locally bound procedure.  This list will be the value of the `let` expression,
and as this is the last expression in the procedure it will propagate to become
the value of the procedure as well.  Finally we use that procedure to produce
overrides in the LilyPond domain.

There is one more “feature” hidden in this example (step back a moment and try
to discover it yourself).  When we invoke the local procedure we pass it
`first`, `second` and `third` as arguments, which seems somewhat natural - but
what *are* these?

```
guile> first
#<primitive-procedure car>
guile> second
#<primitive-procedure cadr>
guile> third
#<primitive-procedure caddr>
```

`first`, `second` and `third` are procedures, actually they are shorthands to
built-in list accessor procedures.  So what reaches the local procedure as
`elem` is not actually a *value* but a *procedure*.  This is what I referred to
as *first class functions* at the beginning of this chapter.  Inside the local
procedure we are doing `(elem color)`, that is: we take the procedure that is
not hard-coded but passed in as an argument and apply it to `color`, which is a
value that we have obtained as the argument to the outer procedure.
