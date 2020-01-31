# Creating Lists of Music Expressions

Using music functions is very handy to make overrides parametrical, for example using a construct like the following:

```lilypond
colorGrob =
#(define-music-function (grob color)(symbol? color?)
   #{
     \once \override #grob #'color = #color
   #})

{
  c'
  \colorGrob NoteHead #red
  d'
  \colorGrob Flag #green
  e'8 f'
}
```

However, often it is necessary to wrap multiple expressions in the single music expression that a music function can return, for example

```lilypond
#{
  \once \override NoteHead.color = #color
  \once \override Dots.color = #color
  \once \override Flag.color = #color
  % etc.
#}
```
