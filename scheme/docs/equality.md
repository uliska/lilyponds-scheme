# Three Different Levels of Equality

Comparing the equality of values is a regular task in programming, usually as the base for a decision.  However, deciding whether two values are “equal” isn't as
trivial as one might think, and different programming languages have different
approaches to this question.

Scheme has three different concepts of equality, represented by the three
equality operators `eq?` `eqv?` and `equal?`. We will see these three again in
various incarnations, as variants to different comparison operators.  The exact
interpretation of each level of equality is left to the discretion of the
“implementation”, so everything described here is explicitly valid for [Guile
Scheme](https://www.gnu.org/software/guile/docs/docs-1.8/guile-ref/Equality.html#Equality)
only and may differ from any information you might encounter regarding MIT
Scheme or Racket etc.

Objects of different *type* are never equal in Scheme.

## eq?

`eq?` checks for the *identity* of two objects, and the scope of that identity
is very narrow in Scheme.  Basically this predicate returns true if and only if
the two arguments refer to the *same object in memory*, regardless of their
values.  This means that for a lot of comparisons `eq?` isn't applicable, but it
is by far the most efficient predicate.

Most importantly *symbols* with the same name *are* identical, so `(eq?
'my-symbol 'my-symbol)` will always evaluate to `#t`.  Strings with the same
content are, on the other hand, *not* equal in the sense of `eq?`: `(eq?
"my-string" "my-string")` will always evaluate to `#f`. Consequently you should
try to use symbols wherever possible to *name* things, especially keys in
[association lists](alists/index.html).

Booleans of the same value are identical, which can be used in decision
processes: `(eq? #t (number? 2.4))` evaluates to `#t` because the evaluation of
the `number?` predicate evaluates to `#t`, which is “identical” to the other
`#t` argument.

Another object that is unique and can be compared with `eq?` is the end-of-list
element `()`: `(eq? (cdr '(1)) (cdr '(2)))` evaluates to `#t` because the `()`
exists only once.

**Note:** Numbers and characters *may* be `eq?` to the numbers and characters
with the same content, but - according to the reference - you can't rely on
that fact. So depending on the context both is possible: `(eq? 1 1) => #t` or
`(eq? 1 1) => #f`.

## eqv?

Numbers and characters should rather be compared with `eqv?`.  This doesn't look
for *identity* but for *equivalence* of the compared objects - for numbers and
characters.  For all other data types `eqv?` behaves the same as `eq?` and
should regularly not be used: `(eq? '(1 . 2) '(1 . 2))` evaluates to `#f` even
if the pairs have the same content.

## equal?

For all cases except the ones mentioned above `equal?` should be used - which is
the least strict but also the most “expensive” procedure. In the case of
compound data types `equal?` checks for equivalent content recursively, walking
over the individual elements and comparing their content. So all these
expressions evaluate to `#t`:

```
(equal? "a-string" "a-string")
(equal? '(1 . 2) '(1 . 2))
(equal? (list 1 2 3 4) (list 1 2 3 4))
```


**TODO:** Investigate and discuss the difference between `=` and `eqv?` or
**`string=?` and `equal?`.
