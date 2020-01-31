\version "2.19.40"

one = #'(this is a symbol-list)
failOne = this.is.a.symbol-list

#(display "")

#(display failOne)

two = #'(this doesn@t work)
%failTwo = this.doesn@t.work

#(display "")

three = #'(one false4 symbol-list)
%failThree = one.false4.symbol-list

four  = #'(4 this seems to work)
wrongFour = this.'4.seems.to.work

%five = #'(one 4false symbol-list)
%failFive = one.4false.symbol-list

{
  c
}
#(display failFive)