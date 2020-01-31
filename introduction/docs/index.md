# Understanding Scheme In LilyPond

## GNU LilyPond

[GNU LilyPond](http://lilypond.org) is an extremely powerful and versatile text
based music notation system with a strong focus on traditional craftsmanship and
the aesthetics of manual plate engraving. LilyPond reads input files in which
the user has textually specified the *content* of a score, and it compiles these
files to graphical scores in PDF, PNG, or SVG format (or additionally to
non-graphical MIDI files). LilyPond's output can be tweaked to the least detail,
but in fact even LilyPond's *behaviour* can be modified and extended right
through to its inner gears! This is possible through LilyPond's built in
extension language,
[Scheme](https://en.wikipedia.org/wiki/Scheme_%28programming_language%29)

## Extending LilyPond

In a way, extending Lilypond with Scheme is like open heart surgery, and it is
definitely not necessary for regular use and engraving scores. However, getting
familiar with Scheme at least basically is always a good idea as one encounters
its language constructs even in entry level LilyPond documents. Understanding
these elements and their integration in LilyPond will make you feel more
comfortable writing LilyPond files, and it opens up the horizon, even without
ambitions to become a serious LilyPond “programmer”.

## The Thorny Path

For anybody except seasoned computer scientists this seems to be a thorny path,
to which the LilyPond user mailing lists blatantly bear witness. The basic
concepts of the language are different to what most users may know from more
familiar script languages such as Python, JavaScript or even VisualBasic. The
integration of two different languages (LilyPond and Scheme) adds to the
complexity, and the advanced interaction with LilyPond's internals gives yet
another layer on top.

## User-friendly Learning Materials

The [introductory chapters](intro/index.html) outline the different aspects to
the complexity of understanding Scheme in LilyPond. But in addition I have
always felt that part of the problem is a lack of suitable learning resources.
Unfortunately the [official
documentation](http://www.lilypond.org/doc/v2.18/Documentation/extending/index.html)
is not exactly helpful in a smooth introduction to the world of extending
LilyPond with Scheme, presumably because it's written too much from a
developer's perspective. This was my motivation to start a category of [Scheme
tutorials](http://lilypondblog.org/category/using-lilypond/advanced/scheme-tutorials/)
on *Scores of Beauty*, the semi-official LilyPond blog. The idea behind these
tutorials is to focus on a single task and explain it at a slow pace and
sufficiently verbosely to give non-programmers the chance to get an idea *why*
something is done a certain way, rather than just having them *copy* some
ready-made code fragments.

## About This Book

When preparing a university course about Scheme in LilyPond I found myself
starting to write the book that *I* would have needed several years ago. More
and more it started heading towards a certain level of comprehensiveness,
although it still doesn't claim to be a proper computer science textbook. In
this online book I'll cover a lot of Scheme topics, from the perspective of its
use in LilyPond. What I'm trying to achieve is giving thorough explanations to
the fundamental concepts and language structures. This tries to overcome or at
least alleviate the obstacles that LilyPond users typically face when trying to
approach Scheme. The book won't be “easy reading”, but it is slow-paced enough
to enable any reader to get a firm understanding of how and why things have to
be written in certain ways when using Scheme in LilyPond.

### Who Should Read This?

This book is for you if you

* want to be more comfortable with the scripting extension in LilyPond
* want to learn something new and powerful
* want to stretch your limits with LilyPond
* want to look under LilyPond's hood and experience the power of extending a
  program to its inner gears
* are simply a curious nature

### The Book's Structure

This book has to cover a range of different topics in several areas of interest.
While slicing content in web-friendly, digestible chunks of information seems
rather straightforward, the number of topics might quickly get out of hand for a
website navigation. Therefore the book is split into a parent and a number of
“child” books, each covering a specific area. The book parts are essentially
equal with regard to design and navigation, but they are differentiated by color
variations. The main book's left-hand navigation includes “downward” links to
the sub books, while each of them points back to the main book.

The main book (which you are currently reading) introduces the topic and gives
an overview about the context of LilyPond as a compiling batch program and its
extensibility with Scheme.

The first part will introduce Scheme as a programming language. It covers very
fundamental details but doesn't claim to be a proper computer science book.
Introducing the programming language is done strictly from the perspective of a
LilyPond user, both regarding possible preconditions and use cases and by
covering exactly LilyPond's version of Scheme.

The second part deals with the integration of Scheme in LilyPond. This aims at
providing familiarity with switching languages in input files, and at explaining
the fundamentals of extending LilyPond's functionality through Scheme.

The third part will then dive into the internals of LilyPond, giving assistance
in the tasks of tweaking LilyPond's behaviour to its inner core. This is where a
number of wizards perform their black magic, and at the point of this writing
(Jan 2020) it is totally unclear how far the journey will go with this book. But
I really hope to be able to give you some foundations to build on so in future
you will not have to *fully* and *helplessly* rely on the generosity of some
friendly community member to donate you some copy&paste-able code.

### Contributing

Like everything in the LilyPond and Free Software world I would be more than
happy for this “book” to become a community-driven resource. If you feel you
have something to say about a topic feel free to contact me directly; if you
have something to comment on or complain about please click on the Github link
at the top right and open an issue in the tracker. In addition, the first
heading of each page includes an “edit” link leading to the actual page source;
if you have an account on Github you will be able to edit the page and open a
pull request for me to review.