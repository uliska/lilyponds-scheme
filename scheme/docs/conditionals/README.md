# Conditionals

All programming languages provide constructs to choose code to execute based on
some conditions.  These constructs are known as *conditionals*, and Scheme is no
exception to this rule. The keywords provided by Scheme are `if`, `cond` and
`case`, and they are accompanied by the *logical operators/expressions* `and`,
`or` and `not`.

There is a conceptual difference to conditionals in other languages, though.
Colloquially one would phrase the *if* conditional as “*if* a certain condition
is met *then* do the following”. In Scheme, however, the conditional is a single
expression, and depending on the tested condition this evaluates to one of its
subexpressions. We will investigate this closer in the following chapters.
