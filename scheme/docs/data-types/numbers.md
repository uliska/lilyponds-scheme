# Numbers

Numbers are ubiquituous in computing, and according to the [Guile
reference](https://www.gnu.org/software/guile/manual/html_node/Numbers.html#Numbers)
there is a whole lot of aspects that can be discussed about them.  However, for
LilyPond users there is not that much required information to begin with.
Scheme supports many different number types, but for LilyPond use, integers and
real numbers are usually sufficient.

To check if a value is a number we can use the predicate `number?`

```
guile> (number? 4.2)
#t

guile> (number? "Hi")
#f
```

## Integers

Integers, or whole numbers, are written as they are, `5`, `-12` or `1234`.  If
written in a LilyPond file they *can* be prepended with the `#` sign or written
literally, so `#13` is equivalent to `13`

```lilypond
\paper {
  min-systems-per-page = 5
  max-systems-per-page = #7
}
```

If arithmetic operations are performed on integers the results are integers as well:

```
guile> (+ 123 345)
468

guile> (* 4 5)
20
```

The predicate for integers is `integer?`


## Real and Rational Numbers

Real numbers are all the non-integer numbers, in computing often referred to as
floating-point numbers. Rational numbers are a subset thereof, namely all
numbers that can be expressed as a fraction of integers.  Fractions are written
as two integers separated by a slash, without any whitespace in between.

```
guile> (real? 1.20389175)
#t

guile> (fraction? 5/4)
#t

guile> (fraction? 1.25)
#f
```


#### Mixing Reals, Rationals and Integers

Above we said that arithmetic operations on integers produce integers again.
However, if only *one* operand is a real number the whole expression gets
converted to reals:

```
guile> (+ 3 1.0)
4.0
```

When integers are divided Scheme will express the result as a fraction that is
shortened as much as possible, but as soon as one real number is involved the
fraction is converted to a floating point number:

```
guile> (/ 4 2)
2

guile> (/ 10 4)
5/2

guile> (/ 4 3)
4/3

guile> (/ 4 3.0)
1.33333333333333
```

#### Exact and Inexact Numbers

Integers and fractions are always *exact* values that can be recalculated as
often as desired, giving always the same result.  Real numbers on the other hand
are *inexact* as they are subject to an arbitrary *precision* as implemented by
the programming language system.  This means that when performing mathematical
operations with real numbers one has to expect the possibility of rounding
errors.  Generally this is not an issue when using Scheme in LilyPond, but it
should be noted that there *is* this issue.

## Calculations With Numbers

In order to learn what operations can be done with numbers in Scheme it may be a
good idea to familiarize oneself with the documentation on
[integers](https://www.gnu.org/software/guile/manual/html_node/Integers.html#Integers)
and
[reals](https://www.gnu.org/software/guile/manual/html_node/Reals-and-Rationals.html#Reals-and-Rationals).
Diving into these pages *now* may also be a good test on how to handle the
reference style of the GNU Guile Manual.
