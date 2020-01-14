#lang racket/base


;; pair == (head . tail)
;; list == recursive pairs, with last pair's tail being '()


(define-syntax-rule (infix a o b)
  (o a b))