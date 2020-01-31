# Preventing Evaluation

As we have seen in an [earlier chapter](../expressions.html) Scheme has the
concept of self-evaluating expressions, which is applicable for most simple data
types: `5` evaluates to `5`, `"foo"` to `"foo"`, and `#t` to `#t`.

However, [symbols](data-types/symbols.html) are different as they are by default
names referring to something else and evaluating to that else's value. `red`
evaluates to the color definition list `(1.0 0.0 0.0)`, `random` evaluates to a
procedure.  However, sometimes we need to work with the names themeselves,
regardless of some entity the refer to or not. We might want to express
something like “hey, we want violet”, no matter how violet is constructed as a
color and whether it is actually defined.

In order to achieve this we can *quote* any Scheme value to prevent it from
being evaluated.  This is done using the `quote` procedure which is applied to a
single object:

```
guile> red
(1.0 0.0 0.0)

guile> (quote red)
red
```

In this case Scheme doesn't care that there is a variable `red` referring a list
of three values and representing the color “red”.  Scheme will also ignore that
there is no color “violet” in

```
guile> violet
ERROR: Unbound variable: violet
ABORT: (unbound-variable)

guile> (quote violet)
violet
```

Quoting can not only be applied to symbols but (as said) to *any* Scheme value,
for example procedures:

```
guile> random
#<primitive-procedure random>

guile> (quote random)
random
```

In all these cases we are dealing with names just as names, without any notion
of a content the names might be referring to.

#### Shorthand Notation

Using `quote` is the explicit way to quote objects, but far more often you will
encounter and use the shorthand notation with a prepended single quote.

```
guile> 'red
red

guile> 'violet
violet

guile> 'random
random
```

However, you should still be familiar with at least reading the explicit form,
as Scheme may use it to format expressions that you may display for learning or
debugging purposes..
