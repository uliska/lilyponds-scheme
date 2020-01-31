# Looking Up Values from Association Lists

Retrieving a value from an alist means looking up the key and returning the
corresponding value.  In our previous alist `my-new-alist` we want to get the
`green` variable for the key `color2`.

As the alists are regular lists we could go ahead and figure out a way to
iterate over the list, comparing each element's `car` with the given key and if
we find something return the corresponding `cdr`.  You are not ready to do that
yet, but fortunately this isn't necessary anyway.  As association lists are so
fundamental that Guile provides a number of specific procedures that can be used
directly.

### Guile's alist Retrieval Procedures

Guile's procedures are documented in the
[reference](https://www.gnu.org/software/guile/docs/docs-1.8/guile-ref/Retrieving-Alist-Entries.html#Retrieving-Alist-Entries),
but looking at that page might be quite confusing at this moment.

There are two basic forms of procedures, and both come in three variants (and
additionally everything is doubled for C and Scheme).  The three variants differ
in the method they use for determining a matching key, which Guile calls the
“level of equality”.  This is a discussion I would like to spare you for now,
and you can keep in mind that as long as you stick to *symbols* as alist keys
you should use the “q” variants of the procedures, `assq` and `assq-ref`.  If at
one point you should need other types as alist keys you have to get familiar
with Scheme's concept of equality and Guile's/LilyPond's implementation of it.

#### Different Return Targets

`assq` and `assq-ref` differ in what they return for the match: `assq` returns
the `(key . value)` pair for a match while `assq-ref` returns just the value.
Both return `#f` if the requested key is not present in the alist.  Please note
the annoying detail that the order of arguments is reversed: `assq` expects
first the *key* while `assq-ref` wants the *alist* first:

```
guile> (assq 'color2 my-new-alist)
(color2 0.0 1.0 0.0)

guile> (assq-ref my-new-alist 'color2)
(0.0 1.0 0.0)

guile> (assq 'color4 my-new-alist)
#f

guile> (assq-ref my-new-alist 'color4)
#f
```

So which procedure should be used then, or which one in which situation?
Generally it is more common that you want to use the *value* rather than the
key-value pair, so this seems to indicate using `assq-ref` preferably.  But
while this is *often* true there is an important caveat: the behaviour with
non-existent keys.  As seen both procedures return `#f` if the key is not
present in the alist, and in our example with the colors this probably doesn't
cause any problems.  However, the issue becomes crucial when `#f` is a valid
value in the alist.  

```
guile> (define bool-alist
       '((subdivide . #t)
         (use-color . #f)))

guile> (assq-ref bool-alist 'use-color)
#f

guile> (assq-ref bool-alist 'use-colors)
#f
```

Both invocations return `#f`, but only in one case this refers to the actual
*value* of the entry, while in the other it is the result of the key not being
present.

Please don't think this is only used to catch typing errors - as this example
might suggest.  It is very common to process alists where it is not known which
keys are present.  In such cases you *have* to use `assq` and unfold the
resulting pair yourself:

```
guile> (assq 'use-color bool-alist)
(use-color . #f)

guile> (assq 'use-colors bool-alist)
#f

guile> (cdr (assq 'subdivide bool-alist))
#t
```

The pair with `#f` as its `cdr` indicates an actual *false* value while the
plain `#f` refers to a missing key.  Unpacking the `cdr` of the result is a
minor hassle, but there still is an issue that you can't handle at the moment:
when the return value is `#f` (i.e. the key is not present) you can't extract
the `cdr` from that (just try out `(cdr #f)`).  In order to properly handle the
situation you will have to wait a little longer until you have digested
[conditionals](../conditionals.html).

#### Caveat: About the Uniqueness of alist Keys

Both `assq` and `assq-ref` return the value for *the first* occurence of the key
in the alist.  This is important because Scheme has no inherent way to guarantee
that keys in alists are unique.  If you think of the fact that alists are
regular lists with a specific form then this is pretty clear - how *should*
there a way for enforcing uniqueness?

In the next chapter you will see how one can take care of uniqueness when adding
entries to an alist, but as long as you can't directly control an alist you have
to expect duplicate keys.

```
guile> (define al
'((col1 . 1)
  (col2 . 2)
  (col1 . 3)))
guile> (assq 'col1 al)
(col1 . 1)
```
