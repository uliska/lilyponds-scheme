# Alternative `lambda` Signatures

In the previous chapter we discussed the creation of procedures with the signature

```
(lambda (<var> ...) <exp1> <exp2> ...)
```

In this each `<var>` represents a single argument that is expected by and then
available within the procedure.  But this isn't the only form of specifying a
procedure's *signature* in Scheme, there are two other options available,
allowing for more flexibility.

---

The following form allows to pass an arbitrary number of actual arguments to a
procedure:

```
(lambda <var> <exp1> <exp2> ...)
```

All arguments that follow the `lambda` expression are then wrapped into a list
that is bound to the name `<var>` within the procedure body:

```
guile>
((lambda var-list
    (display (car var-list))
    (newline)
    (length var-list))
 'one 'two 'three 'four)
one
4
```

The four arguments are wrapped in the list `'(one two three four)` which is
available as `var-list` in the procedure.  This way we can handle arbitrary
numbers of arguments within a function.  The first expressions in the procedure
body print the first element of the argument list while the last expression
determines the value of the whole expression, which is then printed on the last
line of output.

Please note that a) when you pass a single argument to such a procedure you
*still* have to unpack it from the list, and b) there is no extra pair of parens
around the variable declaration or the procedure body - it's basically `lambda`
with an arbitrary number of expressions, whose first represents the name to
which the argument list will be bound.

---

A third form is actually a hybrid of the two others, accepting both a fixed
number of named arguments plus a list of unnamed remaining ones.

```
(lambda (<var-1> ... <var-n> . <var-last>) <exp1> <exp2> ...)
```

The “formals” are given as an improper list here, while the starting entries
`<var-1>` through `<var-n>` represent individual actual arguments, while
`<var-last>` after the dot collects all remaining arguments in a list:

```
guile>
((lambda (x y . z)
    (* (+ x y)
       (length z)))
    1 2 3 4 5 6)
12
```

Of course the procedure is pretty useless, but it shows how the signature works.
We have two actual arguments, `x` and `y`, which are taken from the first two
arguments passed to the list: `x = 1` and `y = 2`.  The remaining arguments are
wrapped to the list `'(3 4 5 6)` and bound to the name of `z`.  The body adds
`x` and `y` (= 3) and multiplies that with the number of remaining arguments
(4).

---

As said earlier it will rarely make sense to create a procedure using `lambda`
for a single application as seen so far.  I think each of these examples would
have been realized simpler with “normal” expressions.  Procedures are getting
interesting when they are *bound* to a name and made *reusable*.
