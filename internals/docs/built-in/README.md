# Built-in Scheme Functions

LilyPond's documentation has a page "Scheme Function", which is
[here](http://lilypond.org/doc/v2.18/Documentation/notation/scheme-functions)
for the current stable version 2.18 and
[here](http://lilypond.org/doc/v2.19/Documentation/notation/scheme-functions)
for the current development version 2.19.

This is a reference of an enormous number of extremely useful functions, namely
all those Scheme function starting with `ly:` that provide an interface with
the inner state and workings of LilyPond and a score document.  Unfortunately
this page is extremely difficult to digest - to a point to being barely usable
as more than a *reminder* of what's available.  This is mostly due to the fact
that this whole page is generated from "docstrings", concise explanations
stored directly in the source code.  So if you are feeling dumb when reading
the docs be assured that you're not alone.  Usually it is only possible to get
some value out of it when someone on the `lilypond-user` mailing list gives you
some snippets to digest or to simply insert into your current project.

The purpose of this section of the book is to provide usable explanations of the
different Scheme functions, giving you the knowledge that is necessary to
successfully make use of that "communication channel" into LilyPond's heart.

{% credits %}{% endcredits %}