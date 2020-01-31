# Understanding Scheme In LilyPond

[GNU LilyPond](http://lilypond.org) is an extremely powerful and versatile text
based music notation system with a strong focus on traditional craftsmanship and
the aesthetics of manual plate engraving.  LilyPond reads input files where the
user has textually specified the *content* of a score and compiles them to
graphical scores in PDF or SVG format (or additionally to non-graphical MIDI
files).  LilyPond's output can be tweaked to the least detail, but in fact even
LilyPond's *behaviour* can be modified and extended right through to its inner
gears!  This is possible through LilyPond's built in extension language,
[Scheme](https://en.wikipedia.org/wiki/Scheme_%28programming_language%29)

In a way, extending Lilypond with Scheme is like open heart surgery, and it is
definitely not necessary for regular use and engraving scores.  However, getting
familiar with Scheme at least basically is always a good idea as one encounters
its language constructs even in entry level LilyPond documents.  Understanding
these elements and their integration in LilyPond will make you feel more
comfortable writing LilyPond files, and it opens up the horizon, even without
ambitions to become a serious  LilyPond “programmer”.

For anybody except seasoned computer scientists this seems to be a thorny path,
to which the LilyPond user mailing lists blatantly bear witness.  The basic
concepts of the language are different to what most users may know from more
familiar script languages such as Python, JavaScript or even VisualBasic.  The
integration of two different languages (LilyPond and Scheme) adds to the
complexity, and the advanced interaction with LilyPond's internals gives yet
another layer on top.

The [introductory chapters](intro/index.html) give an outline to the different aspects
to the complexity of understanding Scheme in LilyPond.  But in addition I have
always felt that part of the problem is a lack of suitable learning resources.
Unfortunately the [official
documentation](http://www.lilypond.org/doc/v2.18/Documentation/extending/index.html)
is not exactly helpful in a smooth introduction to the world of extending
LilyPond with Scheme, presumably because it's written too much from a
developer's perspective.  This was my motivation to start a category of [Scheme
tutorials](http://lilypondblog.org/category/using-lilypond/advanced/scheme-tutorials/)
on *Scores of Beauty*, the semi-official LilyPond blog.  The idea behind these
tutorials is to focus on a single task and explain it at a slow pace and
sufficiently verbosely to give non-programmers the chance to get an idea *why*
something is done a certain way, rather than just having them *copy* some
ready-made code fragments.

When preparing a university course about Scheme in LilyPond I found myself
writing the book that *I* would have needed several years ago.  More and more it
started heading towards a certain level of comprehensiveness, although it still
doesn't claim to be a proper computer science textbook.  In this book I'll cover
a lot of Scheme topics, from the perspective of its use in LilyPond.  What I'm
trying to achieve is giving thorough explanations to the fundamental concepts
and language structures.  This tries to overcome or at least alleviate the
obstacles that LilyPond users typically face when trying to approach Scheme. The
book won't be “easy reading”, but it is slow-paced enough to enable any reader
to get a firm understanding of how and why things have to be written in certain
ways when using Scheme in LilyPond.

This book is for you if you

* want to be more comfortable with the scripting extension in LilyPond
* want to learn something new and powerful
* want to stretch your limits with LilyPond
* want to look under LilyPond's hood and experience the power of extending a
  program to its inner gears
* are simply a curious nature

Originally this material was conceived as an integrated part of  [The Plain Text
And Music Book](https://book.openlilylib.org).  However, as it grew so much I
decided to extract it and release it as an independent web book.  Of course the
book is “work in progress”, as thanks to its nature as an online book it's
easily possible to make available what's already been written.  The outline
already gives an impression of what's planned, but experience tells that it
will be both refined and extended during the actual writing process.  If you
find actual errors or sections that could be expressed more clearly, don't
hesitate to contact me and/or open an issue at the book's [Issue
Tracker](https://github.com/uliska/scheme-book/issues).

*NOTE: This book is available on https://scheme-book.ursliska.de but currently
it cannot be built, so the online version is not up-to-date against the state
of the sources in this repository.*
