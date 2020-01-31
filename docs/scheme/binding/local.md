# Local Bindings

A much more interesting - but also complicated - topic is the *local* binding,
which is done with the `let` expression and its relatives.   The primary use
case for local binding is the reuse of evaluations.  When the result of a
complex expression is used more than once it is more efficient and gives a
cleaner input structure to create a local binding for the result and (re)use
that.

Colloquially spoken you can say that `let` allows you to create one or more
local variables and then evaluate one or more expressions.  But in fact `let`
represents exactly *one* expression with some local bindings and an expression
*body*.  The `let` expression itself evaluates to a value that can then be used
externally.

With `let` we finally reach the point where the nested parentheses in Scheme can
become pretty daunting, with lots of frightening and confusing error messages in
the console.  I remember very well how I desparately moved, removed and added
random parens to make `let` expressions work, and once I managed to get them
compile without errors I had no idea *why* and couldn't make use of the
experience for future challenges.  This was until I started understanding how
consequently the expressions are structured and what each part is actually
necessary for, and if you follow me through the next few chapters you will
hopefully reach a comfortable level of familiarity pretty soon.
