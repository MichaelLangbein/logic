#lang racket


(define empty-subst '())

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
                           

