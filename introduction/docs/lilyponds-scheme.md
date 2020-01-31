# LilyPond's Scheme

LilyPond uses *Scheme* as its extension language, OK.  But it has to be noted
that this is only half of the story, and in order not to get confused it's
crucial to have a clear idea of what this actually means.

## *Why* An Extension Language?

LilyPond adheres to the concept of compiling plain text input files.  This makes
it possible to include compiler instructions beyond the basic *contents* in the
files, and these are written using an *extension language*.  Programs could use
arbitrary languages or even invent their own, but in LilyPond's case it was a
natural choice to use Scheme, as it is the official extension language of
[GNU](http://gnu.org), GNU LilyPond's parenting organization and application
framework.

LilyPond's internal architecture is also based heavily on Scheme, and as a
consequence you can interact with LilyPond's internals the same way, as a
developer working on LilyPond *or* a user writing input files.  This makes the
potentials of the extension language so incredibly powerful.

## *What* Is Scheme?

Scheme is a programming language from the
[Lisp](https://en.wikipedia.org/wiki/Lisp_%28programming_language%29) family of
languages, which adhere to the paradigm of [functional
programming](https://en.wikipedia.org/wiki/Functional_programming).  This is
very different from the concept of [imperative
programming](https://en.wikipedia.org/wiki/Imperative_programming#History_of_imperative_and_object-oriented_languages)
which the majority of (non-professional) programmers is more familiar with and
which is present in languages like Python, JavaScript or (Visual) BASIC, Java or
the C family of languages.  This makes getting in touch with Scheme challenging
for many potential users.

## *Which* Scheme?

It is important to note that *Scheme is not (necessarily) Scheme*, as there are
many Scheme
[implementations](http://community.schemewiki.org/?scheme-faq-standards#implementations)
around.  In real life this means that when you search for “Scheme” solutions on
the internet you have to expect  results that may not be (completely) compatible
with LilyPond.  If you are not fully aware of that fact looking for help on the
net can be quite off-putting.

The Scheme implementation used by LilyPond is the one included in [Guile
1.8](http://www.gnu.org/software/guile/), which is the official application
platform and extension language of the [GNU](http://gnu.org) operating and
software system *(please note that Guile 1.8 is not the current version of
Guile, so even web searches for “Guile Scheme” may bring up incompatible
results)*.   Therefore the official resource for any questions is the [GNU Guile
Reference Manual](https://www.gnu.org/software/guile/docs/docs-1.8/guile-ref/),
especially the [API
reference](https://www.gnu.org/software/guile/docs/docs-1.8/guile-ref/API-Reference.html#API-Reference).
But it has to be said that this documentation is suited rather as a *reference*
if you are already experienced with Scheme.


Apart from this the only trustworthy resources for Scheme *in LilyPond* are the
[LilyPond manual](http://lilypond.org/doc/v2.18/Documentation/extending/), this
book, tutorials on [Scores of Beauty](http://lilypondblog.org) or the
[lilypond-user](https://lists.gnu.org/mailman/listinfo/lilypond-user) mailing
list.


## *How* To Use Scheme in LilyPond?

Learning to use Scheme in LilyPond causes challenges on three layers:

* learning the language,
* integrating Scheme code in LilyPond code, and
* (advanced) interaction with LilyPond internals through Scheme.

The following pages will flesh this out somewhat more detailed, while the rest
of the book will provide an idea about the “look and feel” of writing Scheme in
LilyPond.  Selected language characteristics are introduced slowly and
thoroughly, while at the same time discussing how Scheme code can painlessly be
mixed with LilyPond input code.  The higher mysteries of advanced interaction
with LilyPond internals are deferred to a later bookpart.
