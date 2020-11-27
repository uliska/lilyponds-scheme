# Vectors

Vectors are much like lists in that they have values separated with spaces, but
their values are accessed by an "index", which is the position of the value in
the vector.  Indexes are zero-based, so the first position is 0 and the second
is 1, and so on.  The advantage that vectors have over lists is the retrieval of
the values is much faster.

## Creating Vectors

Like lists, vectors can be created as a literal.

```
guile> #(1 "a")
#(1 "a")
```

Or they can be created with the procedure `vector`.

```
guile> (vector 1 "a")
#(1 "a")
```

Note that unlike lists, the literal form of vectors (with the `#`) will assume
that symbols are quoted. So...

```
guile> #(a b)
#(a b)
```

But the procedure will not.

```
guile> (vector a b)
standard input:12:1: While evaluating arguments to vector in expression (vector a b):
standard input:12:1: Unbound variable: a
ABORT: (unbound-variable)
```

## Accessing Vectors

Instead of using `car` and `cdr` as you do with lists, with vectors you use the procedure
`vector-ref` and an index.  (They start at zero.)

```
guile> (define v #(1 "a"))
guile> (vector-ref v 1)
"a"
```

Note that `vector-ref *will* try to evaluate any symbols in the vector, so...

```
guile> (define v #(a, b))
guile> v
#(a, b)
guile> (vectors-ref v 1)
standard input:14:1: In expression (vectors-ref v 1):
standard input:14:1: Unbound variable: vectors-ref
ABORT: (unbound-variable)
```
