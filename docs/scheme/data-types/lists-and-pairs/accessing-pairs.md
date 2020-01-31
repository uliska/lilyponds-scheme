# Accessing Pairs

In the previous chapter we have investigated the different aspects of *creating*
pairs, now we'll look into retrieving values from pairs.  This is not too
complicated but it is necessary to have a firm understanding of it before
proceeding to *lists*.

#### Preparing the Ground

To start off let us create a few pairs for later reuse (so we don't have to
re-type them in the REPL), at the same time taking the opportunity to practise
the creation of pairs:

```
guile> (define a (cons 1 2))
guile> a
(1 . 2)
```

*(As an aside: with `define` we bind a value to the symbol `a`, namely the value
the expression `(cons 1 2)` evaluates to, which is the pair `(1 . 2)`.  You may
notice that the `(define ...)` expression itself does *not* evaluate to anything
(as nothing is written to the console), but afterwards `a` evaluates to the pair.
So later we can simply refer to the pair using `a`.)*

```
guile> (define b (cons '(3 . 4) "5"))
guile> b
((3 . 4) . "5")
```

Here we create a pair `(3 . 4)` to become the first element of our pair `b`.
You can see that it is possible to *nest* pairs and to use arbitrary data types
as the elemennts of a pair.

```
guile> (define c (cons (cons 6 7) "8"))
guile> c
((6 . 7) . "8")
```

Again we create a pair as the first element of `c`.  This example shows how an
element can be the result of a procedure application, in this case a nested
`cons`.  In order to read/understand such an expression one should recall what
we learnt about expressions in general and “resolve” it one step at a time: the
inner `(cons 6 7)` evaluates to a pair `(6 . 7)`, and this pair is then used as
the first parameter to the outer procedure `(cons '(6 . 7) "8")`, which is then
bound to the name `c`.  As material for later retrieval exercises we will create
an even more extreme example of nested pairs:

```
guile> (define d (cons (cons (cons (cons (cons 1 2) 3) 4) 5) 6))
guile> d
(((((1 . 2) . 3) . 4) . 5) . 6)
```

The second element is `6`, the first element is a pair whose second element is
`5` whose first element is a pair ... The following (non-functional) rendering
may be a helpful visualization of the structure:

```
(                          . 6)
 (                    . 5)
  (              . 4)
   (        . 3)
    (1 . 2)
```

Our final definition assigns a *procedure* to the first element and the
evaluation of a *procedure application* to the second element of the pair.
Presumably you will get a different random number if you try this on your
computer, but as it is really pseudo-random you will get the same sequence of
numbers whenever you restart your scheme-sandbox.

```
guile> (define e (cons random (random 100.0)))
guile> e
(#<primitive-procedure random> . 74.1503668178218)
```

Now we have five pairs `a` through `e` that we can work with, starting to
retrieve the individual items from the pairs.

## Retrieving Elements from Pairs

So we have learnt how to create pairs in different ways, from writing them as a
literal to rather complex procedure applications.  For writing property
overrides in LilyPond this should be sufficient in most cases, but as soon as
you want to actually *work* with Scheme it will be necessary to access the
individual elements of pairs (and later lists).  For this Scheme provides the
basic functions `car` and `cdr`.


#### Basic Retrieval Procedures

The first element of a pair is retrieved using `car` and the second using `cdr`:

```
guile> a
(1 . 2)

guile> (car a)
1

guile> (cdr a)
2
```

Applying `car` to `a` evaluates to 1, with `cdr` the result is 2.  One can also
say “The ‘car’ of ‘a’ is 1, and its ‘cdr’ is 2.” “cdr” can be spelled out as
“could-er” to make it more speakable.

These two procedures are very fundamental to working with Scheme, and you will
see them a lot in real code.  While the concept is as simple as that it is
important to have a really firm understanding of it, as you will see the first
complications already in the next two sections.

#### Using Procecures Stored in a Pair

We had defined `e` to hold the procedure `random` as its first element, so
retrieving this should give us the procedure. Testing in the REPL happens to
confirm this assumption:

```
guile> (car e)
#<primitive-procedure random>
```

So if we have a procedure at our disposal, shouldn't it be possible to *use* it,
just like a normal procedure, something like `(random 100)`? And in fact this
works perfectly:

```
guile> ((car e) 100)
81
```

Now you may wonder about the nested parens here, but dissecting it slowly it
should easily become clear. `(car e)` evaluates to the procedure `random`, so
the expression `((car e) 100)` first evaluates to `(random 100)`, which is the
regular syntax for applying procedures, and this application will eventually
evaluate to the (random) value 81.

On a more general level what we see here is that whenever an element of a pair
is not of a simple (or “primitive”) data type it will be retrieved just as what
it *is*, be it an object, a compound data type - or a procedure.  We'll have a
closer look at this in the next section.


#### Nested Retrieval

As we have seen elements of a pair can be pairs themselves:

```
guile> b
((3 . 4) . "5")
guile> (car b)
(3 . 4)
```

In order to retrieve the elements of this pair we can again apply the `car` and
`cdr` procedures - to `(car b)`:

```
guile> (car (car b))
3
guile> (cdr (car b))
4
```

We can “serialize” the nested applications by saying that “3 is the car of the
car of b” and “4 is the cdr of the car of b”.

Scheme provides shortcuts for this type of nested pair retrieval, for the
previous examples these would be `caar` and `cdar`.  There are numerous
variations available that can be looked up in the [Guile
reference](http://www.gnu.org/software/guile/manual/guile.html#Pairs).  The
meaning of these procedures can be “resolved” by considering each `a` in
the name as “the car of” and each `d` as “the cdr of”. So `cdar` can be
resolved to “ the cdr of the car of <some-value>”, `caddar` would be “the car
of | the cdr of | the cdr of | the car of” something.  Of course the value that
is passed to such a procedure must *have* a corresponding level of nesting,
otherwise it will trigger an error:

```
guile> (caar b)
3
guile> (cdar b)
4
guile> (cadr b)
standard input:15:1: In procedure cadr in expression (cadr b):
standard input:15:1: Wrong type (expecting pair): "5"
ABORT: (wrong-type-arg)
```

The first two are the shorthands for the previous applications, but what has
gone wrong with the third one? Let's resolve this expression manually to
understand the error message. The original value is `((3 . 4) . "5")`, and what
we are requesting is “the car of the cdr of” that value. The cdr of the initial
value is `"5"`, and applying the `car` procedure to this fails for obvious
reasons - as we are told explicitly: In order to retrieve the `car` of something
this something has to be a pair, but when our `cadr` reaches the `car` there is
only a simple string left from the orginal object.

Now let's finally investigate our multiply nested pair `d`: `(((((1 . 2) . 3) .
4) . 5) . 6)`. Using `car` returns yet another pair etc.:

```
guile> (car d)
((((1 . 2) . 3) . 4) . 5)
guile> (car (car d))
(((1 . 2) . 3) . 4)
```

Nesting cars and cdrs it is possible to retrieve any single element from the
nested pair. For example the `4` is the `cdr` of what we have just arrived at,
or “the cdr of the car of the car of” the original `d`. The shorthand should
therefore be `cdaar`:

```
guile> (cdr (car (car d)))
4
guile> (cdaar d)
4
```

As an exercise you can retrieve each single integer from `d`, both with the
nested procedure applications and the shorthands. Below are the solutions but
you are strongly encouraged to try it out yourself *before* looking at them.

---

```
guile> d
(((((1 . 2) . 3) . 4) . 5) . 6)
guile> (cdr d)
6
guile> (cdr (car d))
5
guile> (cdar d)
5
guile> (cdr (car (car d)))
4
guile> (cdaar d)
4
guile> (cdr (car (car (car d))))
3
guile> (cdaaar d)
3
guile> (cdr (car (car (car (car d)))))
2
guile> (cdaaaar d)
ERROR: Unbound variable: cdaaaar
ABORT: (unbound-variable)
guile> (car (car (car (car (car d)))))
1
guile> (caaaaar d)
standard input:17:1: In expression (caaaaar d):
standard input:17:1: Unbound variable: caaaaar
ABORT: (unbound-variable)
```

There are two invocations that fail because Scheme (or rather Guile) doesn't
have these defined as shorthands.  In these cases you have to apply and nest the
regular procedures.  However, if you like to get your head around this
additional complexity you can consider the folloiwng (closing) example:
`caaaaar` is not defined but `caaaar` returns a pair. Therefore you can apply
`car` to the result of `caaaar`. And you can even continue on that track, thus
nesting the shorthands in arbitrary ways:

```
guile> (car (caaaar d))
1
guile> (caar (caaar d))
1
guile> (caaar (caar d))
1
guile> (caaaar (car d))
1
```
