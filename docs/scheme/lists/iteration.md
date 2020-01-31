# Iterating Over Lists

Iterating over the elements of a list is an extremely common programming task.
However, this is an area where Scheme is quite different from other languages,
and its idioms are very elegant - once they are not confusing anymore. It is
therefore  important to really understand this topic in order to work
efficiently without being constantly frustrated.

Most languages approach this iteration in a `for` loop. The basic approach would
be counting an index variable and accessing each list element through this
index. For example in “classic” C++

```cpp
int v[5] = {4,3,2,1,0};
for (int i=0; i<5; i++)
{
    printf("%d: %d", i, v[i]);
}

```

Of course this works, but the loop construct is semantically unrelated to the
actual list iteration because it uses an independent counter variable.  Moreover
you are responsible yourself for not exceeding the list index.  Therefore
languages provide a loop construct that is closer to the list, e.g. in Python

```python
values = [4, 3, 2, 1, 0]
for v in values:
    print v
```

“Modern” C++ provides an equivalent construction:

```cpp
int v[5] = {4,3,2,1,0};
for (int x : v)
{
    printf("%d", x);
}
```

This approach makes the elements of the list available in the body of the loop.
This is closer to the list semantics, and it guarantees that the actual range of
list elements is used.  However, the *body* of the loop is still unrelated to
the list, as you could do *anything* inside.

Scheme's approach is similar to Python's (and the second C++ variant) in
actually iterating over the elements of a list passed as argument. But it goes
one step further by *applying a procedure* to each element. There are two
procedures available, differing in what they evaluate to, `map` and `for-each`
which we will discuss in detail. However, as these concepts are mostly useful
with custom procedures these discussion is post-poned to a [later
chapter](../loops/index.html).
