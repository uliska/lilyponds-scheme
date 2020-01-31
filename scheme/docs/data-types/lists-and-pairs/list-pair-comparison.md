# A Comparison of Pairs and Lists

In an [earlier chapter](accessing-pairs.html) we created a nested pair whose
`car`s were again pairs:

```
guile> (define p (cons (cons (cons (cons (cons 1 2) 3) 4) 5) 6))
guile> d
(((((1 . 2) . 3) . 4) . 5) . 6)
```

This definition is remarkably similar to a definition of a list in the previous
chapter:

```
guile> (define l (cons 1 (cons 2 (cons 3 (cons 4 (cons 5 (cons 6 '())))))))
guile> l
(1 2 3 4 5 6)
```

Earlier we had visualized the structure of the nested pair in a pseudo-code
manner, and now we compare that to the corresponding rendering of the list as
chained pairs, and additionally the same for an improper list `(1 2 3 4 5 . 6)`.

```
# Nested pair
(                          . 6)
 (                    . 5)
  (              . 4)
   (        . 3)
    (1 . 2)

# Proper List
(1 .                                  )
     (2 .                            )
          (3 .                      )
               (4 .                )
                    (5 .          )
                         (6 . '())

# Improper List
(1 .                          )
     (2 .                    )
          (3 .              )
               (4 .        )
                    (5 . 6)
```

This visualization and comparison is provided as an opportunity to get a
“picture” of the structure of different list/pair-like constructs in Scheme.
You can also consider the definitions in the code above, and think about how
unwieldy constructs in Scheme can be managed by taking them apart one piece at a
time.  This is something you should regularly take your time for, then you'll
eventually become really familiar with Scheme and its “way of thinking”.
