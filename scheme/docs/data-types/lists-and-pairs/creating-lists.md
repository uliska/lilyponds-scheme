# Creating Lists

As with pairs lists can be created either as literals or by using a creation
procedure, `list`.  In its literal form a list is written as a sequence of
values separated by spaces. The creation is the same in plain Scheme and
LilyPond:

```
guile> '(1 2 3 4)
(1 2 3 4)
guile> (list 1 2 3 4)
(1 2 3 4)
```

```lilypond
% top-level variable definitions
myList = #'(1 2 3 4)
myOtherList = #(list 1 2 3 4)
```

Just as with pairs there is the difference between the quoted and the regular
syntax, which makes a difference as soon as the list elements are not exlusively
self-evaluating anymore:

```
guile> '(red green blue)
(red green blue)
guile> (list red green blue)
((1.0 0.0 0.0) (0.0 1.0 0.0) (0.0 0.0 1.0))
```

In the first, quoted version the symbols are read as literal values whereas in
the second version with the list constructor they are evaluated to their
individual lists before being added to the outer list.  The last expression
eventually evaluates to a list consisting of three lists.

Also as with pairs the list elements can be of arbitrary data types, but this
can only be achieved using the `list` procedure as otherwise everything will be
“quoted”.  We won't discuss the following example in detail as this would be
redundant.

```
guile> (list 'red 12 random (random 12))
(red 12 #<primitive-procedure random> 1)
```

#### Symbol Lists in LilyPond

There is a special kind of list that is needed regularly in LilyPond: a list in
which all elements are symbols.  LilyPond defines the predicate `symbol-list?`
for this purpose, and we can check a given list against it:

```
guile> (symbol-list? '(1 2 3 4))
#f
guile> (symbol-list? '(a b c d))
#t
```

In order to simplify input in LilyPond files the parser accepts a practical
shorthand notation:

```lilypond
% regular Scheme syntax
mySym = #'(red green blue)

% LilyPond-style Symbol list
myOtherSym = this.is.one.symbol.list

% As of 2.19.39 commas may be used instead of dots
myLastSym = red,green,blue
```

`mySym` and `myLastSym` are now identical and would be displayed just like
regular lists.  Note that there must not be spaces around the commas or dots.

However, there is a caveat when entering symbol lists like that in LilyPond
input files, namely the parser must be able to unambiguously identify the
symbols.  Concretely the elements must avoid

* pitch names
* numbers
* special characters

which are perfectly acceptable in Scheme syntax but have a different meaning for
the LilyPond parser.

Enter the following in a LilyPond file and study the resulting (somewhat re-formatted) error messages on the console output:

```lilypond
one = #'(this is a symbol-list)
failOne = this.is.a.symbol-list
```
```
error: syntax error,
       unexpected NOTENAME_PITCH,
       expecting UNSIGNED or SCM_IDENTIFIER or SCM_TOKEN or STRING
failOne = this.is.
                  a.symbol-list
```

The output indicates that the offending part is the `a` element, which is
interpreted as a `NOTENAME_PITCH` instead of being one of the types the LilyPond
parser allows here.  If *any* element of the symbol list has the same name as a
pitch name *in the currently active document language* the list must be entered
using the more extensive Scheme syntax.


```lilypond
two = #'(this doesn@t work)
failTwo = this.doesn@t.work
```
```
error: bad expression type
failTwo = this.doesn
                    @t.work
```

Any special characters will make the LilyPond parser fail with a symbol list.
However, it is noteable that underscores and hyphens *are* accepted.

**TODO:** Find out what “bad expression type” actually means.


```lilypond
three = #'(one false4 symbol-list)
failThree = one.false4.symbol-list
```
```
error: syntax error, unexpected UNSIGNED
failThree = one.false
                     4.symbol-list
```

While Scheme allows a symbol `false4` LilyPond stumbles over it because it tries
to read the combination of characters and subsequent number as pitch and
duration of a note - which doesn't make any sense in this context.

```lilypond
four = #'(one 4false symbol-list)
failFour = one.4false.symbol-list
#(display failFour)
```
```
error: syntax error, unexpected SCM_TOKEN, expecting '='

#(display failFive)
(one 4)
```

This one is a tricky error message as the input to `failFour` actually causes
the LilyPond parser to wreak havoc.  The error is raised not during the parsing
of `failFour` but at the beginning of the next expression, and therefore it
refers to an item that shouldn't be of any interest.  Obviously the parser
reads `(one 4)` and then stops making any sense of the input.  The error message
is rather cryptic in this case as the item that is printed in the message is
*not* the item that caused the error.  And of course it can be a very different
kind of error message depending on what is following in the input file.

However, it is somewhat strange that `4` should be read as a symbol. And indeed,
type-checking (which you will only be able to do after the next chapter) reveals
the `4` to be an integer. We'll discuss this with the next and final example.


```lilypond
four = #'(4 this seems to work)
wrongFour = 4.this.seems.to.work
```

This final assignment works without errors, however, it does *not* produce a
symbol list:

```lilypond
#(display (symbol-list? wrongFour))
#f
```

Obviously it is possible to enter plain integer numbers in a list with dot
notation, but they are then inserted in the list as integers, not symbols.

To conclude, it is a very convenient (and common) shorthand to enter symbol
lists using LilyPond's dot (or comma) notation, but it has its issues and
difficulties.
