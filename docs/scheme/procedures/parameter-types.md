# Handle Different Parameter Data types

At several places we have seen that Scheme doesn't enforce types for procedure
arguments but that (naturally) certain procedure applications may only work with
certain types, e.g. numbers or strings.  So while the following procedure `double`
can be invoked with parameters of arbitrary type everything except numbers will
cause errors:

```lilypond
#(define (double x)
   (+ x x))
```

But with everything we know by now about types, predicates and local binding we
can rewrite this procedure in a robust manner.  Concretely, what we want to
achieve is: if `x` is a number we create the double, if it is a string that
represents a number then first convert it and then double it, but return it as a
string again.  Finally, if it is a string that can't be converted to a number
then it should be “doubled” in the way some other languages understand it:
concatenating the string to itself. Finally we need a fallback action if it is
neither a string nor a number.

The requirement of two specific cases plus a fallback suggests to use the `cond` conditional:

```
(cond
  (number: just double it)
  (string:
    (if it can be converted to a number:
        convert, double, return back
    )
    (else concatenate)
  )
  (else: report an error)
)
```

Leaving out the more complex handling of the string this looks like this in LilyPond:

```lilypond
#(define (double x)
   (cond
    ((number? x)
     (+ x x))
    ((string? x)
     "not implemented yet")
    (else
     "'double' needs a number or a string as parameter")))
```

To implement the string handling we have to know the procedure `string->number` that will return a number - or `#f` if the conversion fails.  This is exactly what we need. We could now do something like:

```
(if (string->number x)
    (string->number y)
    ... else clause)
```

but that looks inefficient because the conversion is actually processed twice.
Now (as we have seen) this is exactly the use case for local binding: we bind
the result of that procedure to a local variable, and if that has a true value
we use it, otherwise do the alternative concatenation:

```lilypond
#(define (double x)
   (cond
    ((number? x)
     (+ x x))
    ((string? x)
     (let ((num (string->number x)))
       (if num
           (number->string (+ num num))
           (string-append x x))))
    (else
     "'double' needs a number or a string as parameter")))

#(display (double 3))
#(newline)
#(display (double "3"))
#(newline)
#(display (double "A"))
#(newline)
#(display (double '(2 . 3)))
```

If the string can be converted to a number this value will be doubled and
converted back to a string, otherwise the original input string is taken and
concatenated to itself.  Now the invocations correctly return `6`, `6` (as a
string), `AA` and the error string.

A perfect exercise would now be to extend that procedure to handle the last
invocation as well: if the parameter is a pair holding two numbers we return a
pair with the numbers doubled each.

---

This is the general approach to handle variable parameter types in Scheme.  If
you don't know what type the input parameter will have and your procedure body
has to care about types then you can block or choose within the procedure body
using built-in or custom predicates.
