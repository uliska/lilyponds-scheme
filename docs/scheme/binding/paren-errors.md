# Parenthesizing Errors with `let`

The typical way to mastering `let` expressions is paved with parenthesizing
errors, which I can tell from experience.  Therefore I think it is a good idea
to not only explain how these expressions *should* be structured but to also
inspect *wrongly* structured expressions.

This chapter discusses the parenthesizing errors most commonly made with `let`
expressions, how to identify and how to fix them.  For most of the examples we
take the expression from the previous chapter as a reference:

```lilypond
dampedYellowWithLet =
#(let ((color (car props))
       (damping (cdr props)))
   (list
    (/ (first color) damping)
    (/ (second color) damping)
    (/ (third color) damping)))
```


### Missing Final Closing Parenthesis

Although a decent editor should assist the user with matching parens it *still*
happens regularly (for example through copy & paste) that the number of parens in
an expression doesn't match.  In this example I removed the closing paren of the
whole expression:

```lilypond
dampedColorWithLet =
#(let ((color (car props))
       (damping (cdr props)))
   (list
    (/ (first color) damping)
    (/ (second color) damping)
    (/ (third color) damping))
```

```
.../main.ly:7:2: error: GUILE signaled an error for the expression beginning here
#
 (let ((color (car props))
error: syntax error, unexpected EVENT_IDENTIFIER
#
 (let ((color (car props))
.../

main.ly:15:1: end of file
```

This error message gives us two indicators for the type of error we made.

The primary hint is the `syntax error, unexpected EVENT_IDENTIFIER` message,
which is always triggered when the total number of opening and closing parens in
a Scheme expression isn't balanced.  The Scheme parser (= GUILE) determines the
expression by matching parens, and within that expression parens are regular
tokens of the Scheme language.  But when the final closing paren is missing
Scheme can't make any sense of the *starting* paren - which is why the error
message is pointing to the *start* of the expression.  In that position Scheme
can only understand the `(` as LilyPond's token for starting a slur - and
therefore as the “identifier” for a “slur *event*” - which is obviously not
correct in this place.

The other indicator is the `end of file`.  Line 15:1 happens to the the end
of the actual file used to create the example, so LilyPond is complaining about not
being able to close all open expressions - which is exactly what we triggered by
removing a closing paren.

So the error message clearly indicates that the Scheme expression starting in
line 7 is not properly closed, that is at least one closing paren is missing,
and your task is to identify the place where the expression *should* be
completed.  The first approach for a solution should then be to add a closing
paren at the end of the expression.


### Extra Closing Parenthesis

```lilypond
dampedColorWithLet =
#(let ((color (car props))
       (damping (cdr props)))
   (list
    (/ (first color) damping)
    (/ (second color) damping)
    (/ (third color) damping))))
```

```
.../main.ly:12:32: error: syntax error, unexpected EVENT_IDENTIFIER
    (/ (third color) damping)))
                               )
```

Again, we have the `unexpected EVENT_IDENTIFIER` message, but this time it is
pointing to the *end* of the expression, and it isn't GUILE that “signaled” it.
In fact Scheme could successfully read the full expression up to the closing
paren and handed responsibility back to the LilyPond parser.  Now LilyPond
encounters the “end of a slur”, which doesn't make any sense in this place.

Of course the solution is simply - and already suggested visually by the layout
of the error message - to remove the extra paren.


### Missing Paren Closing the Bindings

One very common error can occur *because* the editor can assist the user with
paren matching.  While figuring out to balance opening and closing parens the
user manages to miss one closing paren after the *bindings* and adds another,
extra, one at the end so the overall balance of the expression is correct:

```lilypond
dampedColorWithLet =
#(let ((color (car props))
       (damping (cdr props))
   (list
    (/ (first color) damping)
    (/ (second color) damping)
    (/ (third color) damping))))
```

```
.../main.ly:7:2: error: GUILE signaled an error for the expression beginning here
#
 (let ((color (car props))
In file ".../main.ly", line 6: Missing expression in
(let ((color (car props))
(damping (cdr props))
(list (/ (first color) damping)
(/ (second color) damping)
(/ (third color) damping)))).
```

*(Note that the `(let)` expression in the error message is printed on one line,
I have just wrapped it here for better display.)*

This error can be determined from the `Missing expression in (let ...)`
explanation.  As written in the previous chapter a `let` expression consists of
a *bindings* expression and one or more further expressions that form the *body*
of the `let`.  If there is missing a closing paren at the end of the bindings
the parser won't close that part of the expression properly and integrate the
body in it as well. Of course after the closing paren there is no expression
left to form the body of the `let`.

### Extra Closing Paren After the Bindings

This error occurs as the opposite attempt to the previous one.  In order to
match the overall number of parens one adds an extra one after the bindings part
and correspondingly removes one at the end of the expression.

```lilypond
dampedColorWithLet =
#(let ((color (car props))
       (damping (cdr props))))
   (list
    (/ (first color) damping)
    (/ (second color) damping)
    (/ (third color) damping))
```

```
...main.ly:7:2: error: GUILE signaled an error for the expression beginning here
#
 (let ((color (car props))
.../main.ly:9:4: error: syntax error, unexpected EVENT_IDENTIFIER

   (list In file ".../main.ly", line 6: Missing expression in
   (let ((color (car
   props)) (damping (cdr props)))).
```

As a result of this attempt the Scheme expression is already completed after the
bindings, and so the remainder starting with `(list` is already back in the
LilyPond domain. Therefore the `(` before `list` (Line 9:4) is the “offending”
slur for LilyPond's parser - and the remaining lines aren't valid LilyPond input
either (actually you could already *see* that from the missing syntax
highlighting).

In addition Scheme complains about a missing body because it would expect one or
more expressions between the two lost parens in line 8.


### Missing Extra Parens Around the Bindings

In the following - correct - example there is only *one* binding in the `let`
expression.  In such cases the double parens around the bindings part look
somewhat strange:

```lilypond
dampedColorWithLet =
#(let ((color (car props)))
   (display color))
```

Consequently it is a common error to leave out that seemingly redundant extra layer:

```lilypond
dampedColorWithLet =
#(let (color (car props))
   (display color))
```

```
.../main.ly:7:2: error: GUILE signaled an error for the expression beginning here
#
 (let (color (car props))
In file ".../main.ly", line 6: Bad binding color in expression
(let (color (car props)) (display color)).
```

So we have a “bad binding color” here.  If dissected properly even that message makes sense.

As seen in the previous chapter the bindings part of a `let` expression has the form

```
(
  (name value)
  (name value)
  ...
)
```

where each `(name value)` expression is a single binding.  In the above error
example Scheme reads the first opening paren after `let` as the start of the
bindings part and expexts a binding in the form `(name value)` to follow.
Instead it encounters `color`, which obviously isn't a properly formed binding.

So the “bad binding” error indicates a missing opening paren at the beginning of
the bindings part.
