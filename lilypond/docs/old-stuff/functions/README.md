# Music and Scheme Functions

{% authors "Urs Liska" %}{% endauthors %}

It's been about a year since I started a category with [Scheme tutorials](http://lilypondblog.org/category/using-lilypond/advanced/scheme-tutorials/), and back then I declared them as a "documentation of my own thorny learning path". By now I've experienced a significant boost in Scheme "fluency" which was triggered by (and at the same time enabled) a number of projects and enhancements, for example the [ScholarLY](http://lilypondblog.org/2015/01/introducing-scholarly/) package and the jump into a fundamental redesign of [openLilyLib](https://github.com/openlilylib/openlilylib). I thought it would be a good idea to pick up the tradition of these tutorials before I forget too much about the difficulties of finding my way around LilyPond's Scheme. This is of course not a carefully crafted "curriculum" but it will always be a random collection of (hopefully) useful snippets of information, each one written with the goal of explaining a single topic in more depth and at the same time more casually than the LilyPond reference can do.

Today I'm writing a tutorial that I would have needed a year ago ;-) about one thing that always vaguely confused me. I usually managed to just get around it by either routinely "doing it as always" or by getting some ready-to-use code snippets from a friendly soul on lilypond-user.  This is the topic of defining `music-`/`scheme-` and `void-`functions in Scheme. I will analyze a music function I introduced in last years' posts and explain what is going on there. Understanding this gave me surprising insights, and I think knowing this kind of stuff is really helpful when trying to get more familiar with using Schem## Special Elements

### Author(s)

Each page can have a (single) block naming the main author(s) of the
page/chapter and (optionally)  give additional information about the authorship.

As each page will also have a "Credits" box giving automatic information the
“Authors” box may only be entered at the beginning of more important pages, e.g.
the first page of a series of subpages.

If a page is intended to have such a box

```
{% authors "John Doe", "Foo Bar"}<optional comment>{% endauthors %}
or
{% authors "John Doe"}{% endauthors %}
```

should be placed immediately after the main heading.  This will produce a block
listing the main author(s) (determining proper wording depending on the number
of authors).  If that block has some content this is printed as additional
information on the authoring inside the block.

**NOTE:** Markdown formatting is not possible in that content part.  If you need
to insert hyperlinks (e.g. to reference documentation, discussion or a blog post)
you will have to write explicit HTML here.

**NOTE:** Currently (as of gitbook 2.1.0) there is a bug that prevents the last
argument (i.e. author) to be taken into account (see the
[issue report](https://github.com/GitbookIO/gitbook/issues/804)).  This has been
fixed and will be part of the next release.  Please ignore this and do *not* add
an empty dummy author at the end of the list, as the issue will go away
automatically and we would have to update the items manually otherwise.
The current page is an exception to demonstrate the cause.

### Credits Info

Each page should print an info box giving detailed credits about all editors and
authors of the page.  This information is generated automatically, and there is
nothing to be configured about it.  Unfortunately the box can't be inserted
automatically (yet), therefore authors should literally place

```
{% credits %}{% endcredits %}
```

at the bottom of each page.

ne-music-function</span> <span class="scheme-delimiter">(</span><span class="scheme-scheme">parser</span> <span class="scheme-scheme">location</span> <span class="scheme-scheme">my-color</span><span class="scheme-delimiter">)</span>
   <span class="scheme-delimiter">(</span><span class="scheme-function function">color?</span><span class="scheme-delimiter">)</span>
   <span class="scheme-lilypond">#{</span>
     <span class="lilypond-keyword keyword">\once</span> <span class="lilypond-keyword keyword">\override</span> <span class="lilypond-grob">NoteHead</span><span class="lilypond-delimiter keyword">.</span><span class="lilypond-variable variable">color</span> = <span class="scheme-scheme">#my-color</span>
     <span class="lilypond-keyword keyword">\once</span> <span class="lilypond-keyword keyword">\override</span> <span class="lilypond-grob">Stem</span><span class="lilypond-delimiter keyword">.</span><span class="lilypond-variable variable">color</span> = <span class="scheme-scheme">#my-color</span>
   <span class="scheme-lilypond">#}</span><span class="scheme-delimiter">)</span>

<span class="lilypond-delimiter keyword">{</span>
  <span class="lilypond-pitch">c</span><span class="lilypond-octave">'</span> <span class="lilypond-usercommand variable">\colorNote</span> <span class="scheme-scheme">#</span><span class="scheme-variable variable">red</span> <span class="lilypond-pitch">d</span><span class="lilypond-octave">'</span> <span class="lilypond-pitch">c</span><span class="lilypond-octave">'</span>
<span class="lilypond-delimiter keyword">}</span>
</pre>

*(See the [other post](http://lilypondblog.org/2014/03/music-functions-2-start-doing-something-useful/) for the output of that example.)*

This is something I knew how to put together for quite some time, but I've always wondered about a few things here (just managed to suppress the questions, because it *did* work), particularly the relation between the `colorNote =` and the `#(define-music-function` part and the `parser location` arguments. But to be honest, I wasn't really clear about the part returning the "music expression" either.

In the current post I will go into quite some detail about the declaration/definition of the music function and the topic of "return values". However, I'll skip the third issue because that's somewhat unrelated to the other two and because the post is already quite long without it.

### Defining the Music Function

Let's start with looking at it from the perspective of the "user" or "caller". `colorNote` is a "music function" that returns a "music expression". This is the part enclosed in the <code><span class="scheme-lilypond">#{</span> <span class="scheme-lilypond">#}</span></code> brackets, containing two overrides (yes, overrides are also "music") and applying the `#my-color` argument passed into the function. So when writing <code><span class="lilypond-usercommand variable">\colorNote</span> <span class="scheme-scheme">#</span><span class="scheme-variable variable">red</span></code> it's quite obvious that I call the *function* `colorNote`, passing it the *argument* `#red`.

But the syntax of how this "function" is defined somehow always startled me, and I'm sure there are many others who could write such a function too, without really knowing what they are doing. Let's have a look at a comparable function definition in Python (for those who know Python):

<pre lang="python">
def colorNote(parser location color):
    return some_music_expression</pre>

Here the syntax is clear that we are defining `colorNote` to be a function object, taking some arguments and returning a value. When we *use* that function later in the code the program execution will jump right into the body of that function definition. But what do we actually do when "defining a music function" in LilyPond?

From the LilyPond documentation (and last year's posts) we learn that the following expressions are equivalent:

<pre class="lilypond"><span class="lilypond-uservariable">myVariable</span> = <span class="lilypond-value value">5</span>

<span class="scheme-scheme">#</span><span class="scheme-delimiter">(</span><span class="scheme-keyword keyword">define</span> <span class="scheme-scheme">myVariable</span> <span class="scheme-number value">5</span><span class="scheme-delimiter">)</span></pre>

Both define a variable `myVariable` and set its value to the integer number `5`. Or, expressed the other way round, they take the value of `5` and *bind* it to the name `myVariable`. Later in the program (or the LilyPond file) one can refer to this name and get the value back.

We can rewrite the definition using the `#(define` syntax like this:

<pre class="lilypond"><span class="scheme-scheme">#</span><span class="scheme-delimiter">(</span><span class="scheme-keyword keyword">define</span> <span class="scheme-scheme">colorNote</span>
   <span class="scheme-delimiter">(</span><span class="scheme-function function">define-music-function</span> <span class="scheme-delimiter">(</span><span class="scheme-scheme">parser</span> <span class="scheme-scheme">location</span> <span class="scheme-scheme">my-color</span><span class="scheme-delimiter">)</span>
     <span class="scheme-delimiter">(</span><span class="scheme-function function">color?</span><span class="scheme-delimiter">)</span>
     ; ...
</pre>


So what is the value we are binding to the name `colorNote` in our example?

Intuitively I would expect that we bind a function's implementation to the name `colorNote`, similar to what the Python example seems to do. But here we don't seem to assign a function or function body but `define-music-function` instead. If you start thinking about it this seems very strange. Fortunately you can continue thinking about it and it becomes clear, so stay tuned...


Maybe you notice a small but important difference to the above definition of `myVariable`: `define-music-function` is enclosed in parentheses, while `5` was not. Parens (usually) indicate we are calling a procedure in Scheme, and this call *evaluates to* something. Whenever you want to use a *value* you can instead call a procedure, and the value this procedure evaluates to is then used as your value. (You may want to read this paragraph again...  or consider the following mathematical examples. In Scheme `(+ 3 2)` evaluates to 5, `(- 3 2)` evaluates to 1, and `(+ 3 (+ 1 1))` evaluates to `(+ 3 2)` which then evaluates to 5.)

So what we really do with our music function is *call* `define-music-function` which *evaluates to a "music function"* and *bind* this result to the name `colorNote`. Later in the LilyPond file when we call `\colorNote` we do not execute the code after `\colorNote =` (which is what would happen in the Python example) but instead we call the music function that has been created when `\colorNote` has been initially parsed. *(For a more detailed and technical discussion you may read the [Wikipedia article](https://en.wikipedia.org/wiki/First-class_function) about "first class functions")*.

`define-music-function <argument-list> <argument-predicates> <body>` itself takes three arguments, each enclosed in its own parenthesis (here the parens are used for grouping items to a list and not for a procedure call):

- the list of argument names:
  <span class="scheme-delimiter">(</span><span class="scheme-scheme">parser</span> <span class="scheme-scheme">location</span> <span class="scheme-scheme">my-color</span><span class="scheme-delimiter">)</span>
- a list of argument predicates (types that the arguments have to have)
  <span class="scheme-delimiter">(</span><span class="scheme-function function">color?</span><span class="scheme-delimiter">)</span>
- the actual implementation body

`my-color` is an arbitrary name that has been chosen for an argument.  It lets you access the value that has been passed into the music function at that position. Note that this is the only argument that the user has to supply when calling the music function, `parser` and `location` are passed implicitly. According to the manual `parser location` simply has to be copied literally, which is also confusing - but we won't go into this detail today.

`color?` is the type of the (single) value that can be passed to the function, so you can't for example write `\colorNote #'thisIsNotAColor` (which would pass a Scheme *symbol* to the function).

**Side note:** *You also can define music functions that don't have such arguments, so the first element in `define-music-function` would be `(parser location)`. It has always startled me why I'd have to add `()` in such cases, but now this becomes clear: `define-music-function` expects a list of argument predicates as its second argument, and if there are no arguments to be type-checked then this second argument is still expected, and  an empty list has to be passed as the `<argument-predicates>`.*

### The "Return Value" - Music-, Scheme- and Void Functions

**Digression:** "Procedures" and "Functions"

Before going into the topic of the different function types I have to dwell on a certain fuzziness in terminology: *procedures* and *functions*. When reviewing this post I realized that I wasn't completely clear about the distinction and used them interchangeably. My [request](http://lists.gnu.org/archive/html/lilypond-user/2015-04/msg00548.html) on the lilypond-user mailing list raised a discussion showing that it actually isn't a trivial topic. So while in the end it is more or less neglectable there are things you may want to digest in order not to get confused when people use these terms in the LilyPond/Scheme context.

Some programming languages make a distinction between procedures and functions, some don't. *If* a language distinguishes, it is mostly the question of a return value: functions return a value, procedures don't. This means that while both are separate blocks of code that can be *called* from within a program, functions produce a value that can be worked with while procedures just "do" something which doesn't directly affect the calling code.

Other languages don't make a distinction and call both types procedures or functions and usually have a syntactic way to clarify the behaviour. However, it's quite common that people distinguish although their programming language doesn't. If you notice this just try to ignore that and don't be confused.

The implementation of the Scheme programming language that is used by LilyPond is [Guile 1.8](https://www.gnu.org/software/guile/docs/docs-1.8/guile-ref/). In this basically everything is considered a *procedure*, regardless of having a return value or not. Take the following expression:

<pre class="lilypond"><span class="scheme-delimiter">(</span><span class="scheme-keyword keyword">car</span> <span class="scheme-scheme">'</span><span class="scheme-delimiter">(</span><span class="scheme-number value">1</span> <span class="scheme-number value">2</span> <span class="scheme-number value">3</span> <span class="scheme-number value">4</span> <span class="scheme-number value">5</span><span class="scheme-delimiter">))</span></pre>

This *expression* is a *procedure call*, namely the call to the procedure `car`. The list `'(1 2 3 4 5)` is passed as the *argument* to `car`, which *evaluates to* `1`, the first element of the list. So the *"return value"* that is then used in the program is `1`. Other procedures, for example <code><span class="scheme-delimiter">(</span><span class="scheme-keyword keyword">display</span> <span class="scheme-scheme">'</span><span class="scheme-delimiter">(</span><span class="scheme-number value">1</span> <span class="scheme-number value">2</span> <span class="scheme-number value">3</span> <span class="scheme-number value">4</span> <span class="scheme-number value">5</span><span class="scheme-delimiter">))</span></code> do *not* evaluate to anything, so the "value" in the place of the procedure call is `<unspecified>`.

Both are called "procedure" in Guile's terminology although one returns a value and the other does not. However, you will often encounter the naming convention of calling the "returning" versions "function". This is actually against the official naming convention of the Scheme dialect that LilyPond uses, but it is quite common and doesn't pose a real-world problem. And - as far as I can see - this is also true for the terms "music function", "scheme function" and "void function".

---

OK, let's get back on track and consider the "return value" of our music function. Above I wrote that `colorNote` returns a music expression containing two overrides. But what does *that* actually mean?

The *body* of a procedure in Scheme is a sequence of expressions, and each expression can be either a value or a procedure call. The value of the last expression in the body is the value the whole function *evaluates to* - or, more colloquially, is the *return value* of the function. In the case of `\colorNote` this last expression is not a Scheme expression but a LilyPond music expression, as indicated by the `#{ #}`. From Scheme's perspective this is a single value (of type `ly:music?`), but from LilyPond's (or rather a user's) perspective this music expression can also be a grouped sequence of music elements - in our example we have two consecutive overrides.

To conclude we can say that a "music function" is a procedure whose last expression evaluates to LilyPond-music. It can be called everywhere that you can write a music expression in LilyPond - just like in our initial example at the top of this post.

Now, what are `scheme-` and `void-`functions then?

The whole subject of defining these functions/procedures is identical to the definition and calling of music functions, the only (but crucial) difference is the *return value*. A procedure defined using `define-scheme-function` can return any valid Scheme value, and it can be used anywhere the respective Scheme value can be used. The following example takes a string as its argument and returns sort of a palindrome version (just for the sake of the example). The type of the return value is `string?`, and this can for example be used to set a header field.

<pre class="lilypond"><span class="lilypond-uservariable">addPalindrome</span> =
<span class="scheme-scheme">#</span><span class="scheme-delimiter">(</span><span class="scheme-function function">define-scheme-function</span> <span class="scheme-delimiter">(</span><span class="scheme-scheme">parser</span> <span class="scheme-scheme">location</span> <span class="scheme-scheme">my-string</span><span class="scheme-delimiter">)</span>
     <span class="scheme-delimiter">(</span><span class="scheme-keyword keyword">string?</span><span class="scheme-delimiter">)</span>
     <span class="scheme-delimiter">(</span><span class="scheme-function function">ly:message</span> <span class="scheme-string string">"We will add the reverse of the string to itself"</span><span class="scheme-delimiter">)</span>
     <span class="scheme-delimiter">(</span><span class="scheme-keyword keyword">string-append</span> <span class="scheme-scheme">my-string</span> <span class="scheme-delimiter">(</span><span class="scheme-keyword keyword">string-reverse</span> <span class="scheme-scheme">my-string</span><span class="scheme-delimiter">))</span>
     <span class="scheme-delimiter">)</span>

<span class="lilypond-keyword keyword">\header</span> <span class="lilypond-delimiter keyword">{</span>
  <span class="lilypond-variable variable">title</span> = <span class="lilypond-usercommand variable">\addPalindrome</span> <span class="lilypond-string string">"OT"</span>
<span class="lilypond-delimiter keyword">}</span>

<span class="lilypond-delimiter keyword">{</span>
  <span class="lilypond-pitch">c</span><span class="lilypond-octave">'</span>
<span class="lilypond-delimiter keyword">}</span></pre>

The "body" of this procedure is a sequence of two expressions. The first one `(ly:message` prints something to the console output but doesn't evaluate to a value, the second is the call to `string-append`, which is a procedure call that evaluates to a string.

**Side note 1:** *Here again you can see an example of nested procedure calls and their evaluations: `string-append` here takes two arguments, the first being a value (namely the argument `my-string`), while the second argument is again a procedure call. The operations that Scheme actually performs one after another are:*

<pre class="lilypond">
<span class="scheme-delimiter">(</span><span class="scheme-keyword keyword">string-append</span> <span class="scheme-scheme">my-string</span> <span class="scheme-delimiter">(</span><span class="scheme-keyword keyword">string-reverse</span> <span class="scheme-scheme">my-string</span><span class="scheme-delimiter">))</span>
<span class="scheme-delimiter">(</span><span class="scheme-keyword keyword">string-append</span> <span class="scheme-scheme">my-string</span> <span class="scheme-delimiter">(</span><span class="scheme-keyword keyword">string-reverse</span> <span class="scheme-string string">"OT"</span><span class="scheme-delimiter">))</span>
<span class="scheme-delimiter">(</span><span class="scheme-keyword keyword">string-append</span> <span class="scheme-scheme">my-string</span> <span class="scheme-string string">"TO"</span><span class="scheme-delimiter">)</span>
<span class="scheme-delimiter">(</span><span class="scheme-keyword keyword">string-append</span> <span class="scheme-string string">"OT"</span> <span class="scheme-string string">"TO"</span><span class="scheme-delimiter">)</span>
<span class="scheme-string string">"OTTO"</span>
</pre>

So the nested expression in the first line of this example eventually evaluates to "OTTO". And as this is the last expression in the procedure body its value will be the return value of the procedure as a whole, which in this example is used as the title of the score.

**Side note 2:** *You can see that there is a single closing parenthesis on the last line of the procedure. This matches the opening paren in <code><span class="scheme-scheme">#</span><span class="scheme-delimiter">(</span><span class="scheme-function function">define-scheme-function</span></code>. Scheme's coding guidelines suggest not to place parens on their own lines but rather concatenate them at the end of previous lines. As you can already see in these simple examples nesting procedure calls can quickly build up, so it's not uncommon to encounter Scheme procedures with, say, ten closing parens in the last line. However, I laid it out like this to explicitly show that each line in the example is one expression. Temporarily reformatting is a very useful tool for debugging procedures or to understand the structure of existing procedures you are looking at. Don't hesitate to insert line breaks and make use of your editor's assistance to re-indent the code as this will make things much clearer. Once everything is ready it's advisable to re-compress the procedure again, even if you are used to other layouts that are common in other programming languages.*


Probably you can by now guess what a *void-function* is - basically the same as the other two, but *without* a return value. So you will want to use `define-void-function` when you want the procedure to actually *do* something (also known as "side effects") but don't need any return value. The following example will print out a message to the console:

<pre class="lilypond"><span class="lilypond-uservariable">displayLocation</span> =
<span class="scheme-scheme">#</span><span class="scheme-delimiter">(</span><span class="scheme-function function">define-void-function</span> <span class="scheme-delimiter">(</span><span class="scheme-scheme">parser</span> <span class="scheme-scheme">location</span><span class="scheme-delimiter">)</span>
     <span class="scheme-delimiter">()</span>
     <span class="scheme-delimiter">(</span><span class="scheme-function function">ly:input-message</span> <span class="scheme-scheme">location</span> <span class="scheme-string string">"This was called from a 'void-function'"</span><span class="scheme-delimiter">)</span>
     <span class="scheme-delimiter">)</span>

<span class="lilypond-delimiter keyword">{</span>
  <span class="lilypond-pitch">c</span><span class="lilypond-octave">'</span>
  <span class="lilypond-usercommand variable">\displayLocation</span>
<span class="lilypond-delimiter keyword">}</span></pre>

There is just one expression in the function body, printing a message. In the case of `define-void-function` it doesn't matter if this (respectively the last) expression evaluates to something or not, the function won't return any value at all. This also has the effect that you can actually call void functions from *anywhere*. The parser won't try to use them as a value but will simply execute its code. So the following example is equally valid and working.

<pre class="lilypond"><span class="lilypond-uservariable">displayLocation</span> =
<span class="scheme-scheme">#</span><span class="scheme-delimiter">(</span><span class="scheme-function function">define-void-function</span> <span class="scheme-delimiter">(</span><span class="scheme-scheme">parser</span> <span class="scheme-scheme">location</span><span class="scheme-delimiter">)()</span>
   <span class="scheme-delimiter">(</span><span class="scheme-function function">ly:input-message</span> <span class="scheme-scheme">location</span> <span class="scheme-string string">"This was called from a 'void-function'"</span><span class="scheme-delimiter">))</span>

<span class="lilypond-usercommand variable">\displayLocation</span>
</pre>

I hope this post helped you understanding a few basic things about how music, scheme, and void functions work and how they are integrated in LilyPond documents. This is only a tiny start, but understanding these concepts thoroughly definitely helps with proceeding to more complex and more powerful functions. As a final "assignment" I'll leave it to you to figure out what the `location` does in the last example, how it is used and how its value actually got into the function.

{% credits %}{% endcredits %}
