# `let*` and `letrec`

Creating one or more local bindings with `let` is a powerful concept, but there
are cases where it is limited by the fact that the bindings are only accessible
in the body of the expression.

The easiest way to make the point is an example. For this we will continue to
work with the expression from the previous chapters, factoring out yet another
set of objects to bindings:

```lilypond
dampedYellowWithLet =
#(let ((color (car props))
       (damping (cdr props)))
   (list
    (/ (first color) damping)
    (/ (second color) damping)
    (/ (third color) damping)))
```


### `let*`

Suppose we don't want to repeatedly access `color` in the expression body but
rather have bindings for the RGB values that we can use like

```
(list
  (/ r damping)
  (/ g damping)
  (/ b damping)
)
```

Again, in this example case this doesn't make much sense, but when real-world
objects are complex it can be a crucial simplification.

We might be tempted to write

```lilypond
#(let ((color (car props))
       (r (first color))
       (g (second color))
       (b (third color))
       (damping (cdr props)))
   (list
    (/ r damping)
    (/ g damping)
    (/ b damping)))
```

which seems like it might do the job: create three additional bindings making
use of the `color` binding done previously. However, this doesn't work out:

```
.../main.ly:7:2: error: GUILE signaled an error for the expression beginning here
#
 (let ((color (car props))
Unbound variable: color
```

When we try to access `color` (in `(r (first color))`) that binding hasn't been
created yet because all the bindings are only available when the bindings part
of the expression has been completed.

For this use case there is the alternative `let*`. This works like `let`, with
the difference that each binding is accessible immediately, already within the
bindings part of the expression. Thus the following works:

```lilypond
#(let* ((color (car props))
        (r (first color))
        (g (second color))
        (b (third color))
        (damping (cdr props)))
    (list
     (/ r damping)
     (/ g damping)
     (/ b damping)))
```

In fact the necessity to use the `let*` form is quite regular, and therefore
many people tend to write `(let*` before thinking of the actual use case.  But
while this works always one should consider that the added flexibility always
comes at the cost of added computation, and while this may usually be
negligible it should be good practice not to use up resources without need.

### `letrec`

There is another form of local binding, `letrec`.  This works like `let*` with
the added convenience that *all* bindings are available for *all* other
bindings, regardless of the order.  With this expression it is possible to
create bindings that are mutually dependent.  This isn't required very often,
therefore I won't go into more details about it, but you should at least have in
mind that this option is available.
