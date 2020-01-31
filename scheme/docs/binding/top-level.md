# Top-level Bindings

Like most programming languages Scheme has the concept of *scope*, which
basically means that names are visible and invisible in/from certain places.

*Top-level bindings* are variable definitions outside of any expression, somewhere
in the input files.  Bindings created on top-level are globally visible in the
LilyPond files, both from and in included files as well.  But of course they are
only visible *after* they have been created, and it is an error to refer to them
earlier in the input file.  There is a notable difference that will be discussed
in the context of [procedure definitions](../defining-procedures.html).

In the chapter about [including](../including.html) Scheme in LilyPond we have
already seen top-level bindings (or “global variables” as they are often named
in other languages).  As demonstrated there bindings can be created in LilyPond
and in Scheme syntax, and both produce equivalent bindings

```lilypond
% This is written in a LilyPond file
variableA = "Hello, I'm defined in LilyPond"
#(define variableB "And I'm defined in Scheme")
```

Now we have *bound* two strings to the variable names `variableA`
and `variableB`.  Structurally the bindings are equivalent and both variables
can equally be referred to using Scheme and LilyPond syntax (`\variableA` vs.
`#variableA`).  The only difference is in the rules for naming the variables, as
one will be parsed by LilyPond and the other by Scheme/Guile. LilyPond is rather
restricted with regard to identifier naming while Scheme more or less allows
everything.
**TODO:** Reference to LilyPond naming options (including advanced options)
For example the following definition is perfectly valid in Scheme, while the
LilyPond definition would fail:

```lilypond
#(define f9!^¡ "What is this?")

f9!^¡ = "What is this?"
```

Such a variable will *not* be available through LilyPond's backslash syntax, but
you can always access the actual Scheme value using the `#` hash sign:

```lilypond
{
  c'1 \mark #f9!^¡
}
```


## Special Scope in Scheme Modules

As said earlier ariables defined in *LilyPond* files this way are *globally*
visible also from or in included files.  However, defined in *Scheme* modules
there are different rules of visibility or “scope”.  For now you are far from
writing Scheme modules, so I'm only mentioning the fact.

By default, when you bind a variable in a Scheme file using `(define)`,  it is
only visible from within the same module, respectively file.  In order to make
it available from outside one has to use `(define-public)` instead.  This is an
important method to hide elements that should not be accessed directly from
outside.

Additionally there is the concept of  `(define-session-public)`, which *does*
make an element publicly visible, but only for the current compilation out of a
set of multiple files that are being processed.
