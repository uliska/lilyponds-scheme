\version "2.19.40"

start = 1
myList =
#'(1 .
    (2 .
      (3 .
        (4 . 5))))

#(display myList)

#(define (random-positions) (cons (random 5.0) (random 5.0)))

#(define beam-pos 0)

#(define (inc-bar-positions)
   (set! beam-pos (+ beam-pos 0.25))
   (cons beam-pos (+ beam-pos 0.5)))


{
  \override Beam.positions = #(cons (random 5.0) (random 5.0))
  \once \override DynamicText.extra-offset = #(cons (random 5.0) (random 5.0))
  c'8 \p b a b
}