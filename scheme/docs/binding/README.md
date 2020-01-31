# Binding Variables

One of the bread-and-butter tasks in programming is handling variables.  We
already have seen predefined and custom variable definitions, but now it is time
to have a closer look at the topic.

We have seen that *symbols* can be used as self-evaluating *data* or as
*references* to something else: the quoted symbol `'red` simply evaluates to
that name while the symbol `red` evaluates to the list `(1.0 0.0 0.0)`.

```
guile> 'red
red

guile> red
(1.0 0.0 0.0)
```

The usual Scheme terminology for the latter case is to say that “the name `red`
*evaluates to* that list” and that “the list is *bound* to the variable/name
`red`”.

In the case of `red` this binding is available because it has been created
explicitly somewhere in the LilyPond initialization files, but when we need our
own variable name, say `violet` evaluating to `(0.5 0.0 1.0)`, we have to
“create the binding” ourselves.

Bindings can be created at top-level or locally, which we'll investigate in the
following chapters.
