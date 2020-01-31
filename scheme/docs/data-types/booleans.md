# Booleans

*Boolean expressions* are expressions that represent a “true” or ”false” value.
This sounds trivial, but in fact, although *any* programming language relies on
having some boolean representation , there are significant differences in how
they are actually handled.

Scheme has two explicit constants for true and false, namely `#t` and `#f`.
They start with the `#` hash sign, therefore it has to be stressed that *in
LilyPond* these constants have to be written with *two* hash signs, one for
switching to Scheme and the other as part of the constant itself.  This is
consequent but often causes confusion:

```
guile>#t
#t

guile>#f
#f
```

but

```lilypond
\paper {
  ragged-bottom = ##t
  ragged-last-bottom = ##f
}
```


#### `#t` vs. ”A true value”

We have already encountered booleans in predicates, which are procedures that
evaluate to `#t` or `#f`.  However, beside the two boolean *constants* there is
the concept of “true value” and “false value”. Expressions that “have a true
value” do *not* necessarily “evaluate to `#t`”.  Rather they are everything that
is not `#f`.  This distinction will become important when we talk about
[conditionals](../conditionals.html).
