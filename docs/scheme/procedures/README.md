# Defining Procedures

Procedures are the driving force of programming languages because that's where
the static data is actually processed.  So far we have used a number of
procedures that are provided by Scheme or have been defined by Guile or
LilyPond.  Now we're going to “roll our own”, and that's about where the fun
starts (i.e. where we start being able to achieve something useful).

Procedures are created using the `lambda` expression, that is: a `lambda`
expression *evaluates to a procedure*.  At the core of things even the
fundamental language features are expressed as evaluating expressions!  This
also means that procedures are *values* just like every other value in Scheme.
So procedures can be used like any other value, e.g. bound to different names,
stored in pairs or whatever.  We will discuss this in more detail in the
following chapters.

There are different ways `lambda`-generated procedures handle arguments, which
is important enough to warrant a dedicated chapter.  Some words have to be spent
on the binding of procedures to names, which is how procedures can actually be
made useful.  And finally we will have a closer look at a specific type of
procedures: predicates. The main use of this chapter is to get some practise
with writing procedures.
