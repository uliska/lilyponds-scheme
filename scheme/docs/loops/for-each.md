# Iterating Over Lists: `for-each`

`for-each` is very much like `map` with one single difference: the results of
the procedure are not used for anything. Concretely, `for-each` iterates over
the elements of a list (or multiple lists) and applies a procedure to each,
without creating a new list from the results.

```
guile> (for-each display '(1 2 3 4 5 6 7 8 9))
123456789
```

In this short example the procedure `display` is applied to all the numbers in
the list. `display` simply prints the value to the console but doesn't evaluate
to anything. So one can also say `for-each` applies the procedure only for its
*side-effects*, not for its *value*.

It is also possible to apply procedures that *do* evaluate to something, but
that value will simply not be used, so the following example is actually
useless:

```
guile> (for-each symbol->string '(a b c d e))
```

This will convert all the symbols in the list to strings but not *do anything*
with them.

Everything that is said about processing multiple lists with `map` applies to
`for-each` as well.

But actually `for-each` is most useful in combination with custom procedures,
even more so than `map`.
