# Logical Operators: `not/and/or`

Often conditional switches are more complex than a simple true/false decision.
Sometimes it is more convenient to ask if something is *false* than if it's
*true*, and regularly multiple conditions have to be considered in relation.  To
achieve this Scheme offers the procedures `not`, `and` and `or`.

### `not`

`not` is basically the inversion of a test: it returns `#t` if the expression it
tests evaluates to `#f` and to `#f` in all other cases.

```
guile> (not #f)
#t

guile> (not #t)
#f

guile> (not '(1 2 3))
#f

guile> (not (< 2 1))
#t
```

The first two expressions are clear, `not` simply inverts the boolean literals.
The third example shows that *any* object has a “true value” and is inverted to
`#f`.  The final example demonstrates that the value passed to `not` can (of
course) be a complete expression which in this case evaluates to `#f`, which is
then inverted by the `not`.

### `and`

`and` takes any number of subexpressions and evaluates them one after another
until any one evaluates to `#f`.  In this case the `and` expression evaluates to
`#f` as well.  If *all* subexpressions evaluate to a true value the `and`
returns the value of the last subexpression.  This is an important point: `and`
does *not* evaluate to `#t` or `#f` as one might expect, instead it evaluates to
`#f` or an arbitrary value.  You have to take that into account when you need to
*use* that value:

```
guile>
(and
  #t
  (> 2 1)
  (odd? 2)
  "Hi")
#f
```

This expression holds four subexpressions that are tested sequentially:

* `#t` is obviously a true value
* `(> 2 1)` evaluates to `#t` as 2 *is* greater than 1
* `(odd? 2)` evaluates to `#f` as 2 is *not* an odd number
* "Hi" *would* be considered a true value, but it isn't tested anymore because
  `and` has exited already upon the previous subexpression.

```
guile>
(and
  '(1 . 2)
  (list? '())
  #t
  '(1 2 3))
(1 2 3)
```

In this `and` expression *all* subexpressions have true values, therefore the
whole expression evaluates to the value of the last subexpression, the list `(1
2 3)`.  So this is where you must *not* expect `#t` but rather *any*
true value.

### `or`

`or` behaves very similarly to `and`, except that it returns a subexpression's
value as soon as that returns a true value.  Only if none of the subexpressions
return true values the `or` expression returns `#f`.  And as with `and` you have
to expect “a true value” and not `#t` for the successful subexpression.

In the case of `or` this can be used very straightforwardly to provide
fallthrough values: check for a number of tests, and if all fail return the
fallback value as the last subexpression.  For example we can easily rewrite the
test from the previous chapter using `or`:

```lilypond
colors =
#`((col-red . ,red)
   (col-blue . ,blue)
   (col-yellow . ,yellow))

#(display
  (or
   (assq 'col-lime colors)
   (assq 'col-darkblue colors)
   (assq 'col-red colors)
   (cons 'black black)))
```

## Nesting of Logical expressions

When more than one condition have to be nested dealing with “operator
precedence” is a confusing issue in many languages: which conditionals are
evaluated first, do we therefore have to group them with brackets, etc.?
Scheme's approach to this topic is very straightforward, and once you get the
fundamental idea it is no magic anymore: Each conditional expression tests one
single value, and that value can be the result of another logic expression.
Period.  From there you can create arbitrary levels of nesting.

What does the expression `(not (and #t #f))` return and why? We have a `not`
which will invert the boolean state of the value it is applied to.  That value
is the expression `(and #t #f)`, which will evaluate to `#f`.  So the first
evaluation step is to evaluate the inner expression, which leads to `(not #f)`,
which eventually results in `#t`.

Let's inspect a more complex expression:

```
(or (not (> 2 1)) (and #t '() (> 4 5)) "Hehe")
```

This is an `or` expression with three subexpressions: `(not (> 2 1))`, `(and #t '() (>
4 5))` and `"Hehe"`.  `or` will evaluate each of these subexpressions from left
to right, and once *any* subexpression eavaluates to anything other than `#f` it
will return that subexpression's value.  So let's retrace that one by one:

```
(not (> 2 1))
(not    #t  )
#f
```

The first subexpression evaluates to `#f` so we have to continue. The second
subexpression is an `and` expression which itself has multiple subexpressions:
`#t`, `'()` and `(> 4 5)`:

```
#t
#t ; a true value

'()
() ; a true value

(> 4 5)
#f
```

The first two subexpressions of the `and` have true values, but the last one is
`#f`, therefore the whole `and` subexpression evaluates to `#f`, and we have to
continue with the last subexpression, `"Hehe"`.  This subexpression has a true
value, so finally our `or` returns that one and can be considered successful.

As a conclusion, nested logical expressions in Scheme are just like any other
nested expressions: they have to be evaluated one by one, from inside to outside
and in the case of `and` and `or` from left to right, and so everything can be
resolved unambiguously.
