# Custom Data Types

Now that we've discussed some of the basic data types it is important to
understand that Scheme can be substantially extended with arbitrary “data
types”.  As we have learnt earlier Scheme is very open about types, and
therefore creating data types in Scheme is not like defining classes of objects
with their properties and methods.  Instead one writes *predicates* (see [data
types](index.html#predicates)), basically providing a way to check if a given
object matches the criteria for being “of a given type”.

There is a large number of predicates available beyond the basic Scheme data
types, and it is sometimes difficult to trace where a given data type is
originating.  Predicates can be defined in

* Scheme itself,
* Guile's Scheme implementation,
* LilyPond, or
* Custom (user/library) code

You may now want to have a look at the extensive [list of
predicates](http://lilypond.org/doc/v2.20/Documentation/notation/predefined-type-predicates)
in LilyPond's documentation.  To get our head around the idea of custom data
types we will have a closer look at one data type that is defined by LilyPond:
`color?`.

#### Dissecting a Custom Data Type

Applying a color to a score item is achieved by overriding its `color` property.
(For more details about coloring please refer to the respective pages in
LilyPond's [Learning
Manual](http://lilypond.org/doc/v2.20/Documentation/learning/visibility-and-color-of-objects#the-color-property)
and the [Notation
Reference](http://lilypond.org/doc/v2.20/Documentation/notation/inside-the-staff#coloring-objects).)

```lilypond
\override NoteHead.color = #red
```

The hash sign switches to Scheme, and `red` is given as a symbol referring to a
variable.  Using the Scheme REPL we can investigate what this variable evaluates
to:

```
guile>red
(1.0 0.0 0.0)
```

`red` evaluates to a list of three floating-point numbers.  If you know
something about colors and guess that the three numbers represent the RGB values
within a range of `0` and `1` you are right.  If you want you can do more
experiments by inspecting other colors in the REPL, e.g. `blue`, `green`,
`yellow` or `magenta`.

We can use the predicate `color?` to check if a given value is a color.

```
guile> (color? red)
#t

guile> (color? '(1.0 0.0 0.0))
#t
```

It is not surprising to see that `red` is a `color`, but we also see that we can
pass a literal value to the predicate.  Experimenting with a number of values we
can get closer to understanding what `color?` expects:

```
guile> (color? 'my-symbol)
#f

guile> (color? '(1 0 1))
#t

guile> (color? '(1 0 0.5))
#t

guile> (color? '(2/3 1 0.2))
#t

guile> (color? '(3/2 1 1))
#f

guile> (color? '(0 1 0 1))
#f
```

Obviously a color is a color when it consists of a list of (exactly) three real
numbers in the range of `0 =< n =< 1`.  The numbers can be written as integers,
fractions or reals, as long as they are within the proper range.  In a [later
chapter](../predicates.html) we will have a closer look at how `color?` is
defined, which will confirm this assumption.



---

The manual suggest another way of specifying colors from the list of X11 colors:

```lilypond
\override NoteHead.color = #(x11-color 'LimeGreen)
```

Let's check this as well in the shell:

```
guile> (x11-color 'LimeGreen)
(0.196078431372549 0.803921568627451 0.196078431372549)

guile> (color? (x11-color 'LimeGreen))
#t
```

This time we call a procedure `x11-color` with the symbol `'LimeGreen`, and
again it returns a list of three floating point numbers, which “is” a color.

---

Now that we know what a color *is* we can try out to use custom colors created
ad-hoc:

```lilypond
{
  \override NoteHead.color = #'(0.7 0.3 0.8)
  c''4 c''
}

{
  \override NoteHead.color = #'(3/2 0.3 1)
  c''4 c''
}

```

Not surprisingly only the first example works as well and colors the noteheads
in a nice violet.  The second object violates the requirements of `color?` as
the first number is greater than 1.  As a result LilyPond prints a warning to
the console and ignores the override: `warning: type check for 'color' failed;
value '(3/2 0.3 1)' must be of type 'color'`.

Obviously it is possible to use anything as a color property that evaluates to
something satisfying the `color?` predicate, whether it is a predefined color
variable, an ad-hoc list or a call to a custom procedure.  At the same time the
type check (which is actively performed by LilyPond) acts as a safety net: it
prints a warning and tries to continue the compilation, and so it prevents the
program to crash upon erroneous user input.

---

So in this chapter you have learned about the characteristics of data types and
predicates.  They allow to specify how data has to be formed in order to be
successfully processable by the program.  Guile makes use of that feature to
extend Scheme's functionality, and LilyPond does so as well, so in real-world
code you may encounter a large number of different data types.
