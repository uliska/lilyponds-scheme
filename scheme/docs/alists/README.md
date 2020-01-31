# Association Lists

Now that we've become familiar with lists and pairs we can investigate a special
incarnation of them: *association lists*, or *alists*.  These are lists that
associate *keys* with *values* and allow the retrieval of values by their keys,
which is the same behaviour as what *dictionaries* do in other languages such as
e.g. Python.  Alists are for example used to store all the properties in
LilyPond's objects.

Technically a Scheme alist is not some predefined type, but it should be seen
the other way round: a list whose elements are pair representing a key-value
relationship is considered an association list.

## Inspecting alist Structure

In order to save some typing we start a session with defining an association list:

```
guile>
(define my-alist
 '(
    (color1 . red)
    (color2 . green)
    (color3 . blue)
  )
)
guile> my-alist
((color1 . red) (color2 . green) (color3 . blue))
```

This is not the commonly used Scheme layout but intends to give a better idea of
the structure.  Normally the expression would be written in a more condensed
manner (note particularly that all the trailing parens are lined up at the end
of the last line), for example:

```
guile>
(define my-alist
 '((color1 . red)
   (color2 . green)
   (color3 . blue)))
```

Inside the `define` I created a list with three elements using the `'()` syntax,
and each of these elements is a pair associating a name for a color with a
concrete color.  This is a regular list of pairs, but one can say it is an
association list because of that specific structure.  As it *is* a regular list
you can access its elements with the usual methods applicable to lists and
pairs:

```
guile> (car my-alist)
(color1 . red)

guile> (cadr my-alist)
(color2 . green)

guile> (first my-alist)
(color1 . red)

guile> (cdar my-alist)
red
```

I strongly suggest you take the opportunity to practice by trying to retrieve
every single element from this alist, taking specific care about extracting the
elements from the last pair.

### Types and Quotes

Of course the keys and values can have arbitrary types, as is the rule with
Scheme pairs.  But it is considered best practice to use *symbols* as keys,
which has some advantages we won't discuss here.  And this points us to an issue
where we can start to see the practical use case for the different quoting
methods we have discussed in the previous chapter.

`my-alist` maps the *name* (symbol) `color1` to the *name* `red`.  However, if
we make use of such an association list we usually want to map the name `color1`
to the *color* `red`. The real-world use case of this might be that we have
defined a certain type of thing (e.g. the composer name) to be formatted using
“color1” and have the user specify a concrete color for that stylesheet. Or we
might highlight editorial additions with a color and want to set that to black
when the score is compiled for publication.

So we have to make sure that the *value* parts of the pairs have the right type,
which is not possible using the syntax used above.  But while all the options
are available that we discussed in the *quoting* chapter I will only use the
most common idiom here: *quasiquote* the whole list and *unquote* the values
(note the backtick in front of the list's parenthesis):

```
guile> (define my-new-alist
`((color1 . ,red)
  (color2 . ,green)
  (color3 . ,blue)))
guile> my-new-alist
((color1 1.0 0.0 0.0) (color2 0.0 1.0 0.0) (color3 0.0 0.0 1.0))
```

If you are wondering why the three pairs look like lists instead of pairs you
should go back and check out the “Digression” section in the chapter about
[creating quoted lists and pairs](../quoting/lists-and-pairs.html).

But of course we don't want to only create alists but to actually *do* something
with them, which we'll discuss in the following chapters.

As processing alists is so central to working with Scheme it is no wonder that a
number of dedicated procedures exist for adding, updating, retrieving and
removing entries from alists are available.  They are not hard to understand in
principle, but in my experience there are two issues one has to be very careful
about: the seemingly arbitrary order of arguments that is expected by the
different procedures, and the fact that some procedures modify the alists
in-place while others just return new copies.  This is something one has to
learn very thoroughly - or be sure to always look it up when using the
procedures.
