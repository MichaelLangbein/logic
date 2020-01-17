#lang racket
(require minikanren)
;; (require cKanren)

;; a relation is a method accepting relation-members and returning a goal
;; a goal is a method accepting a frame and returning a stream of frames or #f
;; a frame is a dictionary, a list of lvar-value tuples
;; a lvar is a vector containing one symbol

;; (define relation
;;    (lambda (el1 el2 el3)
;;       (... such that ...)))


;; when translating procedural code to relational, ...
;; ... translate cond to conde,  (cond: booleans as q&a, conde: goals as q&a. So if you want to keep booleans, keep cond)
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
  (lambda (listL headL)
    (fresh (bodyL)
           (conso headL bodyL listL))))

(define cdro
  (lambda (listL bodyL)
    (fresh (headL)
           (conso headL bodyL listL))))

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

(define lol?
  (lambda (l)
    (cond
      ((null? l) #t)
      ((list? (car l)) (lol? (cdr l)))
      (else #f))))

(define lolo
  (lambda (l)
    (conde
     ((nullo l))
     ((fresh (lhead)
             (caro l lhead)
             (listo lhead)))
     ((fresh (lbody)
             (cdro l lbody)
             (lolo lbody))))))

(define twinso
  (lambda (sth)
    (fresh (x)
           (== (cons x x) sth))))

(define listofo
  (lambda (predo list)
    (conde
     ((nullo list))
     ((fresh (head)
             (caro list head)
             (predo head))
      (fresh (tail)
             (cdro list tail)
             (listofo predo tail))))))

(define listoftwinso
  (lambda (list)
    (listofo twinso list)))

(define eq-car?
  (lambda (x list)
    (eq? x (car list))))

(define member?
  (lambda (m list)
    (cond
      ((null? list) #f)
      ((eq-car? m list) #t)
      (else (member? m (cdr list))))))

(define eq-caro
  (lambda (x list)
    (caro list x)))

(define membero
  (lambda (m list)
    (conde
     ((eq-caro m list))
     ((fresh (body)
             (cdro list body)
             (membero m body))))))

(define memo
  (lambda (m list rest)
    (conde
     ((eq-caro list m) (== list rest))
     ((fresh (body)
             (cdro list body)
             (memo m body rest))))))

;; remove-member
(define rember
  (lambda (x l)
    (cond ((null? l) '())
          ((eq-car? x l) (cdr l))
          ((cons (car l) (rember x (cdr l)))))))

(define rembero
  (lambda (x l out)
    (conde ((nullo l) (== '() out))
           ((eq-caro x l) (cdro l out))
           ((fresh (head body rest)
                   (conso head body l)
                   (rembero x body rest)
                   (conso head rest out))))))


(define append
  (lambda (l1 l2)
    (cond ((null? l1) l2)
          ((cons (car l1) (append (cdr l1) l2))))))

(define appendo
  (lambda (l1 l2 l3)
    (conde ((nullo l1) (== l3 l2))
           ((fresh (head1 body1 apd)
                   (conso head1 body1 l1)
                   (appendo body1 l2 apd)
                   (conso head1 apd l3))))))

;; equivalent to list, but the last element is not '(), but the last element of the inputlist
(define dpair
    (lambda (lst)
      (cond ((null? (cdr lst)) (car lst))
            ((cons (car lst) (dpair (cdr lst)))))))



(define anyo
  (lambda (g)
    (conde
     (g)
     ((anyo g)))))

;; nevero can fail any number of times, whereas falseg can only fail once.
(define neverg (anyo falseg))

;; alwayso can succeed any number of times, whereas trueg can only succeed once.
(define alwaysg (anyo trueg))

;; salo: succeed-at-lest-once




;; Test backend
;; (run* (q)
;;       (== (list 1 q) (list 1 2))) ;; => (2) ?
;; (run* (q)
;;       (== '(1 q) '(1 2))) ;; => (2) ?
;; 
;; (define printo
;;   (lambda (sth)
;;     (print sth)
;;     trueg))
;; 
;; (run* (q)
;;       (printo '(1 q))
;;       (printo '(1 'q))
;;       (printo (list 1 q)))
;; 


;; (define eval
;;   (lambda (query)
;;     (run* (query)
;;           (conde
;;            ((membero query facts))
;;            ((fresh (rule)
;;                    (membero rule rules)
;;                    (eval rule.condition)))))))
 


