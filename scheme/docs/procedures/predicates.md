# Defining Predicates

In the discussion of [custom data types](data-types/custom.html) we discussed
the variety of types in Scheme is extended using *predicates*.  Instead of
defining “classes” or “prototypes” and instantiate objects as having a certain
type predicates are used to determine if a given expression/value matches
certain criteria.  Generically speaking a predicate is a procedure expecting one
argument that evaluates to `#t` or `#f` depending on criteria specific to the
requested type.  In this chapter we get back to that topic as an exercise that
will help us get a better understanding of procedure definitions.

In that earlier chapter we introduced the `color?` predicate. Now we're in the
position to investigate its actual definition which can be found in the file
`scm/output-lib.scm` within LilyPond's installation directory:

```lilypond
(define-public (color? x)
  (and (list? x)
       (= 3 (length x))
       (every number? x)
       (every (lambda (y) (<= 0 y 1)) x)))
```

We define a procedure with the name of `color?` and one argument `x`.  Appending
a question mark to the name is the Scheme convention for predicates.  (And it is
created with `define-public` because `output-lib.scm` is a Scheme *module*, and
earlier I told you that definitions have to be explicitly made public within
modules.)

The body of the expression is one single `and` expression, so the procedure will
evaluate to a true value if all of the sub-conditions are met.  If on the other
hand *any* single subexpression evaluates to `#f ` the predicate will also
evaluate to `#f`. The (four) conditions that a value has to meet in order to be
a “color” are:

* `(list? x)`
  The value has to be a *list*
* `(= 3 (length x))`
  This list must have exactly three elements
  (representing the red, green and blue components)
* `(every number? x)`
  All three elements must be (real) numbers
* `(every (lambda (y) (<= 0 y 1)) x)`

The last condition should be inspected more closely.  `every` is like `and` but
with lists. **TODO**: *Reference to subchapter of "list operations"*: it applies
a procedure to a list of arguments, one after another, and returns either `#f`
or the value of the application to the last list element.  But what *is* the
procedure that is applied here? it's a `lambda` expression, in other words: an
unnamed local procedure:

```
(lambda (y) (<= 0 y 1))
```

which `every` will apply to each element of the `x` list.  The local procedure
expects a single argument `y` and will check if it is a number between
(including) 0 and 1.  This `<=` expression expects numbers and would trigger
errors otherwise, but from the previous subexpression in the `and` we know that
it *is* a number. `<=` will evaluate to `#t` or `#f` and not to an arbitrary
value, so the `every` expression will do so as well - it is not possible that
any other “true value” than `#t` will be the outcome.  Therefore finally the
value of the whole predicate will be either `#t` or `#f`.  This is the specific
requirement when writing predicates: they have to return real `#t` and not just
true values.

## Practising With Predicates

To get a better understanding of predicates and types let's write a few
predicates as an exercise and investigate some characteristics.

#### Specifying Type More Narrowly

start with something really simple: checking for a
positive integer number:

```lilypond
#(define (positive-integer? x)
   (and (integer? x)
        (> x 0)))
```

Again we have an `and` expression in the body, this time we first check if `x`
is an integer number and then if it's greater than zero.  Now let's see a
somewhat more involved predicate, checking if a color is “reddish” (which we
define as the “red” component being stronger than the sum of the “green” and
“blue” parts):

```lilypond
#(define (reddish? col)
   (and (color? col)
        (>= (first col)
            (+ (second col) (third col)))))

#(display (reddish? red))
% => #t
#(display (reddish? blue))
% => #f
#(display (reddish? (list 0.7 0.35 0.4)))
% => #f
#(display (reddish? magenta))
% => #t
```

First we check if the tested object is a color in the first place, and of course
we don't reimplement that check but use the existing `color?` predicate.  As the
second subexpression of the `and` we build the sum of the second and third list
elements and compare that to the first list element.

#### Choice

A common situation is that values with one out of several types can be accepted
in a certain place.  For these cases there already are a number of `X-or-Y?`
predicates available, and one can easily write custom predicates as well.
Imagine for some obscure reason you expect a variable to be either a list, a
color or a symbol, then you can create the following predicate:

```lilypond
#(define (list-or-color-or-symbol? x)
   (or (list? x)
       (color? x)
       (symbol? x)))
```

While the previous - “narrowing” - predicates used the `and` conditional this
type of predicates tends to use `or` instead.

Another typical “choice” type of predicate would check if a value is part of a
predefined list:

```lilypond
#(define (mode? x)
   (and (symbol? x)
        (or (eq? x 'major)
            (eq? x 'minor))))
```

This would return `#t` when (and only when) applied to `'major` or `'minor`.

#### Caveat: “True Values”

As a last example I'm going to show you a somewhat more involved example with a
caveat: checking if an object is an association list that contains a specific
key:

```lilypond
#(define (alist-with-color? x)
   (and (list? x)
        (every pair? x)
        (assq 'color x)))

#(display
  (alist-with-color?
   '((amount . 5)
     (color . red))))
```

Surprisingly, when we compile this code the output on the console isn't `#t` or
`#f` but `(color . red)`.  This is because the predicate procedure has the value
its last expression has, and this is the `assq` in this case.  From the
discussion of [association lists](../alists/index.html) we recall that the
return value is either `#f` or the retrieved *pair* - but what we need is a
simple `#t` in this case.

This means whenever a test used in a predicate returns “a true value” it has to
be wrapped in order to really return `#t` or `#f`. Which is fortunately very
easy to do:

```lilypond
#(define (alist-with-color? x)
   (and (list? x)
        (every pair? x)
        (if (assq 'color x)
            #t
            #f)))
```

The `assq` is wrapped in an `if` expression, so if `assq` returns “a true value”
the expression manually returns `#t` instead.

A good exercise to do on your own now would be to write a predicate
`alist-with-key?` where you can additionally specify the key whose presence
you'd like to check.
