# Learning the Language

The first and of course most fundamental challenge in learning Scheme in
LilyPond is - Scheme itself.

Learners who are not used to functional programming tend to find Scheme
confusing, with the most prominent aspect being the overwhelming number of
parens *(“parens” is a shortname for “parentheses” and is often used colloquially
in computer literature although it's dubious if that term can be considered
proper English. However, as it “flows” much better while the proper term is
comparably awkward I will stick to the shortened form throughout this book)*.
Cryptic error messages triggered by the slightest parenthesizing error are not
likely to make the learning curve more pleasing.  In my experience *evaluating
expressions*, as explained in detail in a [later
chapter](../scheme/expressions.html), is the first and most important concept
that has to be thoroughly understood.  Once that has been digested, everything
else will be much easier to comprehend.  I will try to make this learning
process as smooth as possbile in the [main bookpart](../scheme/index.html) about
Scheme.

But there is another substantial cause for confusion, and while this book can't
*eliminate* it the mere *knowlegde* of its existence will be of great help.
Concretely, knowing that you're not alone will make you feel significantly less
dumb and helpless.  I'm talking about the fact that any Scheme keyword or
function can have a number of different origins.

Most likely you will encounter existing Scheme code either by looking into
arbitrary files or when investigating code that someone shared with you.
Probably code shared in response to requests on the mailing lists is the single
most common opportunity to get in initial touch with Scheme. The next natural
step - after having managed to get such code to run at all - is usually the
desire to modify that code in order to avoid having to ask the kind donor again.
And this is where users are typically faced with incomprehensible heaps of code -
and parens.  Lacking the basic understanding of the fundamental ideas usually
makes it unlikely to successfully change anything in the code.  Figuring out
what is going on in the code is made pretty complicated because there is no
single place to look up the names, and web searches are generally not very
helpful either.

What makes finding information about any given name or construct so difficult is
that it can be defined in many different contexts:

* *Core Scheme  *
  These are the easiest cases.  But not every core feature is supported by each
  Scheme implementation.
* *Guile* (i.e. the actual Scheme implementation)  
  Of course Guile is the reference for which Scheme elements are available in
  LilyPond
* *Guile modules*  
  Not everything a Scheme system provides is available by default.  Guile offers
  a huge number of modules that have to be included for its functionality to be
  accessible.  LilyPond includes a number of such Guile modules automatically,
  but code that you see may depend on additional modules.  As a consequence code
  that works in one context may trigger `unknown escaped string` errors in others.
* *LilyPond*  
  LilyPond itself defines a large number of Scheme functions and keywords.  
  Searching the net for these as “Scheme” keywords will probably fail
* *User code*  
  Many names you encounter in Scheme code are functions or variables defined
  elsewhere in the file or in a user-provided library.  In a way this is a clear
  case but experience tells that these names cause a whole lot of additional
  confusion if you can't really discern the previous four items either.

When looking at existing Scheme code you'll likely encounter *all* of these in
one place, and this can be pretty confusing - in a way it feels like a system of
equations with *at least* one variable too much.  There is no once-and-for-all
solution to this issue, but I can encourage you to keep calm and try to slowly
disentangle everything step by step.  And to ask.  Probably it's not that you
are too stupid for it, it's more likely that you're trapped in the described
situation.  So feel free to ask on the mailing lists, and try not to be
satisfied by a solution that “just works” but ask until you have understood the
underlying principle.

The bookpart about [Scheme](../scheme/index.html) will cover Scheme concepts on
their own, but always from the perspective of LilyPond.
