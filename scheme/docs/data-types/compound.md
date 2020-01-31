# Compound Data Types

The data types we have seen so far was a selection of “simple” data types.
These “atomic” data types can be seen as building blocks from which larger data
types and objects can be composed.  In the context of the “data types” chapter
we are not going to discuss “objects” in the sense of real-world models but
start with compound data types.  

Compound data types are types that have more than one atomic member.  For
example if you imagine a data type representing a “point” in a two-dimensional
space it will have two members, namely values on both axes.  In Scheme we would
express this as a *pair*, which is Scheme's most fundamental compound data type.

We will take a close look at *lists* and *pairs* now, and after that investigate
how *custom data types* can look like in Scheme.
