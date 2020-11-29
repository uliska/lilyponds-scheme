# `cond`

The `cond` conditional is used when there are more than two options to handle.
All the considerations about “true values” and the evaluation of subexpressions
discussed in the previous chapter about `if` apply here as well, so if anything
is unclear please refer to that chapter.

The general form of a `cond` expression is

```
(cond
  (clause1)
  (clause2)
  ...
)
```

Each *clause* starts with a test, and if the test succeeds the clause is
evaluated and its value returned.  The last clause may have the keyword `else`
instead of a test, and if none of the previous tests succeeds this final else
clause is evaluated.

### Different Forms of clauses

I just wrote that the clauses are evaluated if their test succeeds, but that's a
little bit sloppy.  Actually there are three different forms of valid clauses,
and the evaluation is different in each.  The point was mainly that the first
successful test determines which clause is responsible for the return value.

#### The Most Common Form

The most common form for each clause is

```
(test exp1 exp2 ...)
```

In this case one or more expressions are evaluated and the value of the last
expression is returned as the value of the `cond` expression:

```lilypond
#(display
  (let ((rand (random 100)))
    (cond
     ((> rand 50)
      (display rand)
      (newline)
      "Random number is greater than 50")
     ((< rand 50)
     (display rand)
     (newline)
      "Random number is smaller than 50")
     (else
      (display rand)
      (newline)
      "Random number equals 50"))))
```

First we generate a random integer and locally bind it to `rand`.  In the `cond`
expression we have three cases, expressed by two tests and an else clause.  In
each clause three expressions are evaluated, and the third - a literal string -
is returned as the value of the `cond` expression, which is passed along as the
value of the `let` expression as well.  Note that the `cond` expression itself
is surrounded by parens as well as each individual clause, but the expressions
*within* the clauses are not.

#### Test Only

Another form for the clauses is

```
(test)
```

If a clause is expressed in this way a successful test will directly return its
value, without evaluating further expressions.  This is where the concept of
“true values” comes into play: if the test returns a value that is considered
“true” we can directly use it.  In the chapter about [retrieval from
alists](../alists/retrieving.html) we learned about the `assq` procedure that will
return either a key-value pair from an association list or `#f` if the given key
is not present in the alist.  This way we can directly return the resulting
entry or pass control along to the next clause.  The following example creates
an alist of colors and then tries to retrieve a color through a `cond`
expression (in real life we would get the alist from “somewhere” so we don't
know which keys it contains):

```lilypond
colors =
#`((col-red . ,red)
   (col-blue . ,blue)
   (col-yellow . ,yellow))

#(display
  (cond
   ((assq 'col-lime colors))
   ((assq 'col-darkblue colors))
   ((assq 'col-red colors))
   (else `(col-black . ,black))))
```

`assq` will return `#f` for the first two tests because the given keys are not
in the `colors` alist.  However, the third test gives a match with the
`'col-red` key, therefore the `assq` expression evaluates to the pair `(col-red
1.0 0.0 0.0)`.  Since this is a “true” value it is returned as the value of the
`cond` expression and consequently printed to the console.  If none of the tests
would succeed the `else` clause would create a pair with the same structure as
the pairs returned by the other clauses, so anyone *using* the return value
would surely get valid data.

#### Apply a Procedure to the Test Result

A final form for the clauses is

```
(test => proc)
```

In this case `proc` should be a procedure that takes exactly one argument. If
the test returns a true value `proc` will be applied to this result.  We can use
this form to improve our previous example so that it only returns the actual
color part of the alist entry:

```lilypond
#(display
  (cond
   ((assq 'col-lime colors) => cdr)
   ((assq 'col-darkblue colors) => cdr)
   ((assq 'col-red colors) => cdr)
   (else black)))
```

We perform the same test as before, but when it returns the pair this pair will
be passed to the procedure `cdr` which will directly extract the second part of
the pair.  The `else` clause has been adjusted accordingly.

This form is actually a very nice form of ”syntactic sugar” because it greatly
simplifies that task.  Of course we could get the same result - the color part
extracted from the pair - with the other forms as well, but in an unnecessarily
complicated way. The relevant clause could for example be written like this:

```lilypond
((assq 'col-red colors)
 (cdr (assq 'col-red colors)))
```

Once we know that we're at the right key we can retrieve the value again and
pass it along to `car`, which seems pretty inefficient.  So we can avoid using
`assq` twice by hooking in a local binding:

```lilypond
((let ((result (assq 'col-red colors)))
   (if result
       (cdr result)
       #f)))
```

Basically this makes use of the previous form, as the `let` expression evaluates
to either the color or to `#f`.  Apart from that hint I leave it to you to
dissect this expression as an exercise to repeat the topic of local binding.
But honestly, `((assq 'col-red colors) => cdr)` is much more elegant, isn't it?
