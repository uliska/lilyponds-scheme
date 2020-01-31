# Strings

[Strings](https://en.wikipedia.org/wiki/String_%28computer_science%29) are
sequences of characters and more or less handle what we see as *text* in
documents.  From the perspective of data processing and programming languages
dealing with strings is surprisingly complex, and working with strings is a
fundamental task also when you're writing Scheme in LilyPond.  Guile provides a
large number of functions for string processing, but we'll only cover a few
specific aspects in this “data types” introduction.  You can find all details
about Scheme's string processing in the [Guile
manual](https://www.gnu.org/software/guile/docs/docs-1.8/guile-ref/Strings.html#Strings).

### Writing Strings

In Scheme strings are always written using *double* quotes. Other languages
understand single and double quotes interchangeably or with subtly different
meanings, but single quotes are reserved for a completely different purpose in
Scheme:

```
guile> "Hello"
"Hello"

guile> Hello
ERROR: Unbound variable: Hello
ABORT: (unbound-variable)

guile> 'Hello'
Hello'
```

The first example enters a *string* that evaluates to itself - strings are
self-evaluating, literals, constants in Scheme.  The second example interprets
the input as a name for a variable that has not been defined yet.  And the final
example interprets the input as a “quoted symbol”, with the trailing single
quote characteristically being part of the symbol.  You will read more about
both cases in [symbols](symbols.html) and [quoting](../quoting.html).

As you have seen in the section about [including Scheme in
LilyPond](../including.html) LilyPond's parser treats strings specially and
doesn't require an explicit switch to Scheme mode through `#`. For all strings
that don't contain any special characters and that are single words you don't
even have to use quotation marks. As said the first three of the follwoing
assignments are equivalent while for the last one the quotation marks are
mandatory:

```lilypond
\header {
  title = #"MyPiece"
  title = "MyPiece"
  title = MyPiece
  title = "My Piece"
}
```


### Escaping Special Characters

There are a number of special characters that can't directly be inserted in
strings, although Guile/LilyPond supports Unicode out-of-the-box.  Inserting
such non-standard characters is done using “escaping”: the parser sees an
*escape character* and treats the immediately following content as a special
object.  In Scheme - just like in many other languages - this escape character
is the `\` backslash.

#### Quotation Marks

The most obvious character that has to be escaped is the double quote itself -
as the parser would interpret this as the *end* of the string by default:

```lilypond
\header {
  title = "My \"Escape\" to Character Land"
  subtitle = "Where things can go "terribly" wrong"
}
```

In this example the title is escaped correctly while in the second example the
quotes break the string variable, which you can already see from the syntax
highlighting.  LilyPond will in this case produce a pretty confusing error
message but will at least point you to the offending line of the input file.

*Note:* this is only true for straight double quotes.  From a typographical
*perspective it is often better to use typographical (or "curly") quotes anyway
*(e.g. `“English”`, `„Deutsch“` or `«Français»`).  These don't need escaping.

#### The backslash

So if the backslash is used to indicate an escape character how can a backslash
be used as a character in text?  Well, in a way that's self-explaining: through
escaping it. To print a backslash you have to escape it - with a backslash:

```lilypond
\markup "This explains the \\markup command."
```

#### Arbitrary Escaped Characters

There is a list of other special ASCII characters in the
[reference](https://www.gnu.org/software/guile/docs/docs-1.8/guile-ref/String-Syntax.html#String-Syntax)
from which you're most likely to come across the *newline* `\n` and the
*tabulator* `\t` escape sequences.

However, there's a last item we want to discuss here: arbitrary special
characters.  The reference page linked just above states that using the `\x`
escape sequence it is possible to address characters numerically.  But while
this only works for the very limited set of ASCII characters and doesn't support
Unicode in general, this isn't generally possible for use in LilyPond strings.
There are cases where it is possible while others don't work, but it can be said
that it is generally not recommended.  Instead there are two options to
include special characters, apart from the option of directly including the
special characters in the input files - if all participating modules support
that.

It is possible to encode special characters using their Unicode code point
either as hexadecimal or as decimal numbers.  Alternatively LilyPond provides a
number of ASCII escape sequences which can be made available from within a
`\paper` block:

```lilypond
\paper {
  #(include-special-characters)
}
```

Both options as well as a list of escape sequences (which are modeled after HTML
escape sequences) can be found in LilyPond's
[documentation](http://lilypond.org/doc/v2.19/Documentation/source/Documentation/notation/special-characters)
