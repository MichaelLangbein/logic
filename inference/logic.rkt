#lang racket
(require minikanren)

;; a relation is a method accepting relation-members and returning a goal
;; a goal is a method accepting a frame and returning a modified frame or #f
;; a frame is a dictionary, a list of lvar-value tuples
;; a lvar is a vector containing one symbol

;; (define relation
;;    (lambda (el1 el2 el3)
;;       (... such that ...)))


;; when translating procedural code to relational, ...
;; ... translate cond to conde,
;; ... translate lambda to fresh,
;; ... translate let to ==.


(define trueg
  (lambda (frame) frame))

(define falseg
  (lambda (frame) #f))

(define printg
  (lambda (frame)
    (print frame)
    (trueg frame)))

(define trueo
  (lambda () trueg))

(define falseo
  (lambda () falseg))

(define conso
  (lambda (headL bodyL listL)
    (== (cons headL bodyL) listL)))

(define caro
  (lambda (someListL headL)
    (fresh (bodyL)
           (conso headL bodyL someListL))))

(define cdro
  (lambda (someListL bodyL)
    (fresh (headL)
           (conso headL bodyL someListL))))

(define pairo
  (lambda (sth)
    (fresh (x y)
           (conso x y sth))))

(define nullo
  (lambda (something)
    (== something '())))

(define eqo
  (lambda (a b)
    (== a b)))

(define listo
  (lambda (l)
    (conde
     ((nullo l))
     ((pairo l) (fresh (rest)
                       (cdro l rest)
                       (listo rest))))))
