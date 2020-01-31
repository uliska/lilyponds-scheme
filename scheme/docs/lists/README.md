# List Operations

Lists are maybe the most important building blocks in Scheme, and processing
lists is fundamental to working with Scheme.  Having a better understanding now
how lists are organized we will investigate a number of higher-level operations
that can be done with lists.

The first topic to be covered is accessing lists and retrieving their elements
beyond the basic `car` and `cdr` procedures.  After that we'll investigate how
to retrieve specific elements from lists and how lists can be modified. Finally
we'll see how to process all elements of a list in sequence.

This chapter will *not* cover all list operations comprehensively, as this is
the task of the official
[reference](https://www.gnu.org/software/guile/docs/docs-1.8/guile-ref/Lists.html#Lists).
However, in order to make efficient use of the reference it is necessary to have
a good understanding of the concepts, and therefore I will cover a subset of the
functionality at a slower pace.
