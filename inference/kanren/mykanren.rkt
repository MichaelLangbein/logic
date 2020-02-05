#lang racket


(define empty-substs '())

(define extend-substs
  (lambda (key val susbts)
         (cons (cons key val) susbts)))

(define var?
  (lambda (v)
     (symbol? v)))

(define findFirstSubstitution
  (lambda (val assocList)
    (let
        ((firstAssoc (car assocList))
         (restAssocList (cdr assocList)))
      (cond
        ((eq? val (car firstAssoc)) (cdr firstAssoc))
        ((not (null? restAssocList)) (findFirstSubstitution val restAssocList))))))

(define walk
  (lambda (variable substitutions)
    (let ((firstSubst (findFirstSubstitution variable substitutions)))
      (cond
        ((and (not (void? firstSubst)) (var? firstSubst)) (walk firstSubst substitutions))
        ((not (void? firstSubst)) firstSubst)
        (else variable)))))

(define walk*
  (lambda (variable substitutions)
    (let ((variable (walk variable substitutions)))
      (cond
        ((var? variable) variable)
        ((pair? variable) (cons
                            (walk* (car variable) substitutions)
                            (walk* (cdr variable) substitutions)))
        (else variable)))))


;; ----------------------------------------------------------------------------------------------
;; goals take arguments and a list of substitutions and augment/reduce that list of substitutions
;; ----------------------------------------------------------------------------------------------


(define trueG
  (lambda (substs)
    substs))

(define falseG
  (lambda (substs)
    #f))

(define unifyG
  ;; the goal behind the relation (== a b)
  (lambda (a b substs)
    (let ((a (walk a substs)
          (b (walk b substs))        ;; resolve as far as possible
      (cond 
        ((eq? a b) substs)                            ;; (== 1 1) does not change substs, neither does (== x x)
        ((var? a) (extend-substs a b substs))         ;; (== x 1) adds (x . 1) to the substs
        ((var? b) (extend-substs b a substs))))))))   ;; (== 1 x) adds (x . 1) to the substs
