# Symbols

Symbols are a double-edged thing in Scheme.  While seeming completely natural
they can cause substantial confusion for beginners.

The [Guile
reference](https://www.gnu.org/software/guile/docs/docs-1.8/guile-ref/Symbols.html#Symbols)
states that *“Symbols in Scheme are widely used in three ways: as items of
discrete data, as lookup keys for alists and hash tables, and to denote variable
references.”* This sounds pretty complicated, but I hope to make that become
clear soon.

On a first level you can see symbols as “names for something”.
Symbols are quite similar to strings in so far as they are sequences of
characters - but written without additional quotation marks. And in some
contexts in LilyPond they can even be used interchangeably. But still they *are*
something different.

First of all symbols are not self-evaluating. Earlier we learnt about
self-evaluating expressions in Scheme, so for example `4` evaluates to the value
`4`, and `"Hello"` evaluates to the string with content `Hello`. A symbol on the
other hand doesn't evaluate to itself but always denotes something else - it is
a symbol *for something*.  When Scheme encounters the symbol `Hello` it will
treat it as the reference to a *variable* whose *name* is `Hello` and will then
evaluate to the *value* of that variable.

```
guile> 4
4
guile> "Hello"
"Hello"
guile> Hello
ERROR: Unbound variable: Hello
ABORT: (unbound-variable)
```

In this case there is no variable with the name `Hello`, which triggers this
error. But earlier we saw how that works when a respective variable exists:

```
guile> red
(1.0 0.0 0.0)
```

`red` is a symbol (defined in LilyPond) that evaluates to the value of a
variable which represents a list of three numbers.

Often we need the symbol “itself” to pass along as data.  To achieve this we
make use of *quoting* - a way to tell Scheme that a symbol does *not* denote
something else.  There are two equivalent ways to express this:

```
guile> (quote red)
red
guile> 'red
red
```

`quote` is a procedure that takes one argument - a symbol -, and prevents the
evaluation of that symbol.  This is a somewhat confusing concept, and therefore
we have a dedicated section on [quoting](../quoting.html).

There is much more to symbols than can be said in this short introduction, and
we will come back to the topic whenever necessary. In need of more detailed
information one can head for the section in the [Guile
reference](https://www.gnu.org/software/guile/docs/docs-1.8/guile-ref/Symbols.html#Symbols).

**TODO:**  
Presumably there are substantial aspects still missing from this page.
