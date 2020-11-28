# Music Function Primer

This chapter will give you some building blocks that you can use to try out the
Scheme features discussed in the current bookpart. They are provided “as-is”,
and you should be aware that you are not expected to really understand them at
this point.  I am talking about `music-`, `scheme-` and `void-` functions, which
are discussed in-depth in a [dedicated
chapter](lilypond/functions/music-scheme-void.html). In this chapter I will only
give you a brief overview, and you can use these functions to experiment with
the Scheme concepts discussed in the remainder of this bookpart.

Music-, scheme- and void-functions are expressions just like anything else in
Scheme. In light of the previous chapter you can say that music functions
evaluate to a “music expression”, scheme functions evaluate to any Scheme value,
and a void function's value is `#<unspecified>`.  That is, wherever you can
write music (and overrides are “music” too) you can instead write a music
function, wherever you can use a Scheme value (for example assigning values to
overrides) you can instead write a scheme function, and void functions can be
used whenever no return value is needed but something has got to be *done*.

All three forms basically look the same, and I will demonstrate this with a
scheme function as an example:

```lilypond
mySchemeFunction =
#(define-scheme-function (argument-name)
   (string?)
   ; function body
   )
```

We use a variable name and assign it a (music) function. Following the keyword
`define-scheme-function` is a list of parameter names (in the example just one),
which is then followed by a list of *predicates* (see [data
types](data-types/index.html)).  For each parameter there must be one predicate
specifying the expected data type, in this case `string?`.

The function body can consist of an arbitrary number of expressions, where the
last one specifies the return value (which is then substituted in the LilyPond
document).

You may have seen such functions where the parameter list started with
(literally) `parser location`.  This is not necessary anymore in LilyPond
releases starting with the current 2.19 development line.  The current stable
release 2.18.2 still requires this, but this is a topic that I won't discuss
anymore in this book.

### Scheme Functions

As we've seen Scheme functions are created using the `define-scheme-function`
keyword.  They evaluate the Scheme value (of arbitrary type) that the last
expression in its body evaluates to, and this value is then used in the LilyPond
document:

```lilypond
mySchemeFunction =
#(define-scheme-function (name)
   (string?)
   (string-append name " | " name)
   )

\header {
  title = \mySchemeFunction "Doubled Title"
}
```

This will call the scheme function and assign `Doubled Title | Doubled Title` to
the `title` paper variable.

### Music Functions

Music functions are created using the `define-music-function` keyword.  Instead
of arbitrary Scheme values they are expected to return a music expression, so
the last expression in the body must be “music”. The easiest way to achieve this
is to switch back to LilyPond mode using `#{ #}`. If it is necessary to access
Scheme values from within that one has to - again - use the `#` hash sign:

```lilypond
myMusicFunction =
#(define-music-function (color)
   (color?)
   #{
     \override NoteHead.color = #color
     \override Stem.color = #color
     \override Flag.color = #color
   #})

{
  c'4
  \myMusicFunction #red
  d'8
}
```

The  `#{ #}` is *one* Scheme expression, but as in any LilyPond music expression
it can have many consecutive elements like the overrides in this example.

### Void Functions

Void functions are created using the `define-void-function` keyword.  Regardless
of the value of the last expression in their body they do *not* return anything
and can therefore be used virtually anywhere in a LilyPond file.  Void functions
are used when something has to be done or modified but we don't make use of the
return value:

```lilypond
myVoidFunction =
#(define-void-function (a-value)
   (number?)
   (display (* 2 a-value)))

\myVoidFunction 4
```
