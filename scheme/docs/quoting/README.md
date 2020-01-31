# Quoting

A very fundamental concept in Scheme is *quoting*.  Unfortunately it is often
made unnecessarily confusing for new users.  If introduced slowly enough and
digested thoroughly the idea isn't that complicated after all.  But instead
users are mostly confronted with it through code pasted from some helpful
snippet, and when trying to modify that unknown code they are left alone with
sloppily placed comments on mailing lists or ready-made corrections.

Quoting is hidden beneath the keywords `quote`, `quasiquote`, `unquote` and
`unquote-splicing` and their slightly confusing shorthands `'` (single quote),
<code>&#96;</code> (backtick), `,` (comma) and `@` (at), combined
with picky requirements regarding the placement of parens.

Being thrown back to one's own experimentation and to trying to adapt other's
code is a recipe for frustration in this case.  Therefore we'll proceed slowly
and dissect this valuable item in the Schemer's toolkit step by step.
