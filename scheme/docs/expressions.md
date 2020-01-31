# Everything In Scheme Is An Expression

One fundamental idea learners have to internalize is the concept of
*expressions*.  While the difference may be very subtle it is one of the major
walls new Scheme users tend to run into.  In many languages a program consists
of a sequence of *statements* that are *executed*, and function calls are such
statements as well.  In Scheme on the other hand virtually everything is an
*expression* that *evaluates to* some *value*. Understanding this avoids
confusion with regard to program flow, but above all it is the key to getting
one's head around that thing with the countless parens.

We will investigate Scheme expressions using a *Scheme shell* or
[REPL](https://en.wikipedia.org/wiki/Read%E2%80%93eval%E2%80%93print_loop)
(Read-Eval-Print-Loop), which - as the acronym suggests - reads in an
expression, evaluates it and immediately prints the resulting value.  For all
but the most trivial use cases this shell is too limited, but for experimenting
with expressions and data types it is pretty much ideal.  

LilyPond provides such a shell whose most important advantage is that it
provides exactly the environment LilyPond is running in. Firing it up with the
command `lilypond scheme-sandbox` you can test how any given expression behaves
in the LilyPond context:

```
$ lilypond scheme-sandbox
GNU LilyPond 2.19.39
Processing `/home/username/lilypond/usr/share/lilypond/current/ly/scheme-sandbox.ly'
Parsing...
guile>
```

At this `guile>` prompt you can enter any single Scheme expression, and its
value will immediately be printed to the command line.  In the following
examples the remainder of the line starting with `guile>` is the expression that
you will enter at the command prompt, while the subsequent line(s) are the
printout of the expression's evaluation.

#### Literals

The most basic type of expression is the literal value.  Try to enter a simple `5`:

```
guile> 5
5
```

Even at this basic stage we can say that you entered an expression, `5`, which
evaluates to a value, `5`.  Literals are also called *constants* or
*self-evaluating expressions*.  Try this with other literal values of different
types:

```
guile> "I'm a string"
"I'm a string"

guile> -1.6
-1.6

guile> #t
#t

guile> '(1 . "Hello")
(1 . "Hello")

guile> '(1 2 3)
(1 2 3)

guile> red
(1.0. 0.0 0.0)
```

The first three expressions were a *string* literal, a floating point *number*,
and Scheme's notation of the boolean *true* value.  Don't worry, we'll dissect
the strange notation of the last three expressions soon, in later chapters.

#### Procedure Application

OK, just having literal values is not really exciting, so let's type in
something more interesting:

```markdown
guile> (+ 12 17)
29
```

This is a simple addition of two numbers, expressed in Scheme's typical notation
with the operator written first, before the operands.  But actually this isn't
the right perspective to understand the matter.  It is not just an example of a
somewhat unusual syntax but rather the core of how Scheme works.

##### Expressions Apply Procedures

What we just typed in is not a “command” or “statement” but an *expression*, an
expression whose value after evaluation is `29`.  Formally the expression we
typed at the prompt is a *list*, Scheme's most basic and fundamental form of
data.  A list in Scheme is an arbitrary number of elements, grouped by parens.
The current list has three elements: a `+` sign and two integer numbers, 12
and 17.  Whenever Scheme sees such a list it considers the first element a
*procedure name* and tries to call that procedure. The remaining elements of the
list are passed to the procedure, or - in Scheme-speak - the procedure is
*applied* to the remaining elements.  So in our example we apply the procedure `+`
to the values `12` and `17`, which evaluates to `29`.  Therefore the whole
expression evaluates to `29` - and from the perspective of the program the whole
thing *is* `29`.

This is the nucleus of how Scheme works and from which the whole language is
built.  In fact it's the core of the whole Lisp family of languages, “Lisp”
being an acronym for ”List Processing”.

```
guile> (string-append "A" " " "B")
"A B"
```

In this example the list consists of four elements. The procedure
`string-append` is applied to three strings, evaluating to a new string,
concatenated from the three ones.  This example is maybe a little bit easier to
digest as `string-append` looks more like a procedure name than `+`, but
basically it's the same thing as in the previous example.  What we perceive as a
procedure and its arguments is in fact a list whose first element is a
procedure.

##### Applying Procedures to Multiple Arguments

It feels natural that `string-append` concatenates all of its “arguments”, but
as said we are talking of applying the procedure to all remaining list elements.
In order to get a deeper understanding we can look at an example that is more
different from what we are used to:

```
guile> (/ 100 2 2 5)
5
```

What is happening here? We have a procedure `/` and apply it to four remaining
list elements consecutively: divide 100 by 2, divide the result (50) by 2,
finally divide the result (25) by 5.  This *is* quite different from most
programming languages where one would have to explicitly use the operator for
each subsequent division.

##### Procedure “Type”

```
guile> (1 "2" 3.14)
ERROR: Wrong type to apply: 1
ABORT: (misc-error)
```

Oh, what is wrong here, why should `1` be the wrong type to “apply”?  As said
Scheme will interpret the first element of a list as a procedure name and try to
call that procedure.  So obviously that first element must *be* a procedure.
Using the REPL we can easily check what Scheme thinks of these procedures when
passed as literals:

```
guile> string-append
#<primitive-procedure string-append>

guile> +
#<primitive-generic +>
```

Obviously procedures don't really have a “value”, therefore the interpreter uses
this special kind of  `#< >` notation to tell us what it has read.
`string-append` is a “primitive-procedure”, and `+` is a “primitive-generic”
(which more or less is the same as a procedure).

##### Procedure Names vs. Expressions

The error in the previous section is caused by mixing procedures and
expressions.  And it is typically encountered when the input code mistakenly
uses the procedure invocation instead of its name.  In order to demonstrate
the difference we will show another example: a procedure (defined by LilyPond),
entered without and with parentheses:

```
guile> ly:version
#<primitive-procedure ly:version>

guile> (ly:version)
(2 19 39)
```

In the first invocation `ly:version` is considered a literal, revealing that it
is a procedure.  In the second invocation the parens cause that procedure to be
*called*, evaluating to a list with the version numbers for the current LilyPond
version (so you'll likely get a different result when you try it out).

The final example is the real-world cause for the “Wrong type to apply” error
that is also very confusing for beginners:

```
guile> ((+ 1 2))
ERROR: Wrong type to apply: 3
ABORT: (misc-error)
```

What is happening here? We have entered one layer of parentheses too much.  Of
course it's a simplistic example but when you are trying to modify real-world
code this is something you will run into quite often.

So what happens (and will be explained in more detail in the next section) is:
First the inner expression `(+ 1 2)` is evaluated and replaced with the result,
leaving `(3)` to the interpreter. In the next step to evaluate the complete
expression Scheme will try to invoke the procedure `3` because its the first
element in the remaining list. *Now* the error message is completely
understandable.



##### Summary:

Whenever you see an expression wrapped in parentheses you know
that it is a list whose first element should be a procedure, which is then
applied to all remaining list elements *(note that there is the concept of
*quoting* that makes an important difference here.  We will go into detail
about this in a later chapter)*.  The value this expression evaluates to is
the result of the procedure application.  This statement may seem trivial now,
but keeping this in mind very firmly will help you significantly when having
to disentangle complex nested structures in Scheme.

#### Nested Expressions

Every expression *evaluates to* something, and from Scheme's perspective this
“something” then replaces the original expression.  Expressions can *contain*
other expressions, and we speak of ”nested expressions” then.  In that case
Scheme subsequently evaluates the expressions from right to left (or from inside
to outside).

In the following example of a more complex calculation the nested expressions
are evaluated in turn and replaced with the resulting value:

```
guile>(+ (- 14 4) (* 3 (- 5 3)))
16
```

The following list shows the intermediate states of that nested expression up
to its final evaluation to a simple value:

```
(+ (- 14 4) (* 3 (- 5 3))) ; (- 5 3) => 2
(+ (- 14 4) (* 3 2))       ; (* 3 2) => 6
(+ (- 14 4) 6)             ; (- 14 4) => 10
(+ 10 6)                   ; => 16
```

Already at this stage of an only slightly complex calculation the overall
expression has *three* closing parentheses.  It is clear that with more complex
expressions this can quickly grow to a large number of nesting levels,
especially when considering that procedures can be much more complex items than
the simple operators we just had.  Note that this expression still doesn't *do*
anything useful yet, from the program's perspective it just represents `16` - so
it will have to be integrated somewhere, resulting in even more nesting layers.
Take the following expression as a contrived example.

```
guile> (let* ((init-value (+ (- 14 4) (* 3 (- 5 3))))
              (processed-value (* (+ init-value 4) (- init-value 3))))
        (display processed-value))
260
```

You can and should for now ignore everything you don't know about that (we'll
soon cover it in the chapter about [variable binding](binding.html)) but simply
realize that within that “mess” we have inserted the previous expression and
that it actually evaluates to a simple `16`, so the expression could as well
have been written as

```
guile> (let* ((init-value 16)
              (processed-value (* (+ init-value 4) (- init-value 3))))
        (display processed-value))
260
```

Getting lost in nested parens is one of the most common - and potentially
frustrating - experiences new Scheme users have.  But when you strictly keep in
mind that each pair of parens encloses one expression it is possible to keep the
head over water.

#### Some Preliminary Words on Program Flow

So far we have only talked about single expressions.  But of course these don't
make up complete programs.  A Scheme program consists of either a single
expression or a sequence thereof.  Whenever the complexity of the task suggests
factoring out functionality in procedures this is done, but not through
explicitly *calling* them but through expressions that implicitly invoke them,
as we have discussed in this chapter.  Of course users can define their own
procedures, which will be covered later.  But any procedure can be understood as
a single expression that - again - *evaluates* to its “result”.


##### “Empty” Expressions

It has to be said that there are expressions that do *not* evaluate to anything
useful, and Scheme treats their value as `<unspecified>`.  These correspond to
*void functions* in languages like C++ or Java or *procedures* in languages that
discern between *functions* (do return a value) and *procedures* (do not).  At
this point we don't have the means to show these, but it is a good idea to keep
in mind that such “empty” expressions exist.
