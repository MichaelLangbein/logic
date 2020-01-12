import unittest
import sys
import io
from ie import InferenceEngine, Object, Relation, Variable, Rule
from helpers import toList


X = Variable('X')
Y = Variable('Y')
Z = Variable('Z')
V = Variable('V')
A = Variable('a')
B = Variable('b')

class InferenceEngineTestCase(unittest.TestCase):

    def testAllCombinations(self):
        ie = InferenceEngine()
        gen1 = range(3)
        gen2 = range(2)
        gen3 = range(3)
        allCombinations = ie.allCombinations([gen1, gen2, gen3])
        acl = toList(allCombinations)
        self.assertTrue( len(acl) == 3*2*3 )


    def testIsMortal(self):
        ie = InferenceEngine()
        aristoteles = Object('Aristoteles')
        human = Relation('human')
        mortal = Relation('mortal')
        ie.addFact(aristoteles)
        ie.addFact(human, aristoteles)
        ie.addRule((human, Z), 
                   (mortal, Z))
        isAMortal = toList(ie.eval(mortal, aristoteles))
        self.assertTrue( isAMortal == [{}] )
        isSomeoneMortal = toList(ie.eval(mortal, V))
        self.assertTrue( isSomeoneMortal[0] == {V: aristoteles} )


    def testMickeyRecursion(self):
        ie = InferenceEngine()
        mickey = Object('Mickey')
        minnie = Object('Minnie')
        married = Relation('married')
        ie.addFact(mickey)
        ie.addFact(minnie)
        ie.addFact(married, mickey, minnie)
        ie.addRule((married, V, Z), (married, Z, V))
        m = toList(ie.eval(married, minnie, mickey))
        self.assertTrue( m[0] == {} )


    def testBadFamilyRelations(self):
        ie = InferenceEngine()
        michael = Object('Michael')
        andreas = Object('Andreas')
        volker = Object('Volker')
        bruder = Relation('Bruder')
        vater = Relation('Vater')
        X = Variable('jemand')
        Y = Variable('noch jemand')
        V = Variable('vater')

        ie.addFact(michael)
        ie.addFact(andreas)
        ie.addFact(volker)
        ie.addFact(bruder, michael, andreas)
        ie.addFact(vater, michael, volker)
        ie.addRule(('and', (vater, X, V),
                           (bruder, X, Y)),
                    (vater, Y, V))

        jemands = ie.matchInFacts(X)
        self.assertTrue( len(toList(jemands)) == 3 )

        vaterWenn = ie.matchInRules(vater, A, B)
        self.assertTrue( toList(vaterWenn)[0].condition == ('and', (vater, X, B), 
                                                        (bruder, X, A)) )

        volkerIstMeinesBrudersVater = ie.eval('and', (bruder, michael, A),
                                                    (vater, A, volker))
        print(toList(volkerIstMeinesBrudersVater, 1))


    def testAndStopsEarly(self):
        """
            In the printout, verify that there is no line 
            `now evaluating: (uncle, ben, arthur)`
        """
        ie = InferenceEngine()

        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput

        john = Object('John')
        jane = Object('Jane')
        ben = Object('Ben')
        arthur =  Object('Arthur')
        likes = Relation('likes')
        uncle = Relation('uncle')
        ie.addFact(likes, john, jane)
        ie.addFact(uncle, ben, arthur)
        rs = ie.eval('and', (likes, john, jane), # True
                            (likes, jane, john), # False, stopping
                            (uncle, ben, arthur)) # irrelevant

        sys.stdout = sys.__stdout__
        output = capturedOutput.getvalue()
        print(output)
        
        self.assertTrue(output.find("now evaluating: (uncle, ") == -1)
        self.assertTrue( len(toList(rs)) == 0 )


    def testAddCombinationsNotFullyExecuted(self):
        """
            prove that your yielding does not require 
            'allCombinations' to be fully evaluated in an 'and' statement.
            In the printout, verify that there is no line 
            `now evaluating: (uncle, A, B)`
        """
        ie = InferenceEngine()

        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput

        john = Object('John')
        jane = Object('Jane')
        ben = Object('Ben')
        arthur =  Object('Arthur')
        likes = Relation('likes')
        uncle = Relation('uncle')
        ie.addFact(likes, john, jane)
        ie.addFact(uncle, ben, arthur)
        rs = ie.eval('and', (likes, john, jane), # True
                            (likes, Z, john), # False, stopping
                            (uncle, A, B)) # irrelevant


        sys.stdout = sys.__stdout__
        output = capturedOutput.getvalue()
        print(output)
        
        self.assertTrue(output.find("now evaluating: (uncle, ") == -1)
        self.assertTrue( len(toList(rs)) == 0 )


    def testGoodFamilyRelations(self):
        ie = InferenceEngine()

        volker = Object('Volker')
        andreas = Object('Andreas')
        michael = Object('Michael')
        bruder = Relation('Bruder')
        vater = Relation('Vater')

        ie.addFact(volker)
        ie.addFact(andreas)
        ie.addFact(michael)
        ie.addFact(vater, volker, andreas)
        ie.addFact(vater, volker, michael)
        ie.addRule((bruder, X, Y),
                   (bruder, Y, X))
        ie.addRule(('and', (vater, V, X), 
                           (vater, V, Y)), 
                    (bruder, X, Y))

        results = toList(ie.eval(bruder, Z, andreas))
        self.assertTrue( results[0][Z] == andreas )
        self.assertTrue( results[1][Z] == michael )
        self.assertTrue( len(results) == 2 )


    def testMicroShaft(self):
        ie = InferenceEngine()

        ben = Object('ben')
        alyssa = Object('Alyssa')
        cy = Object('Cy')
        lemmy = Object('Lemmy')
        luis = Object('Luis')
        warbucks = Object('Warbucks')
        scrooge = Object('Scrooge')
        robert = Object('Robert')
        aull = Object('Aull')

        bigWheel = Object('big wheel')
        bigWheelAssistant = Object('big wheel assistant')
        accountingChief = Object('accounting chief')
        accountingAssistant = Object('accounting assistant')
        computerWizzard = Object('computer wizzard')
        computerTechnician = Object('computer technician')
        computerProgrammer = Object('computer programmer')
        computerTrainee = Object('computer trainee')

        address = Relation('address')
        job = Relation('job')
        salary = Relation('salary')
        supervisor = Relation('supervisor')
        canDoJob = Relation('can-do-job')

        ie.addFact(scrooge)
        ie.addFact(address, scrooge, Object('Weston'))
        ie.addFact(job, scrooge, accountingChief)
        ie.addFact(salary, scrooge, Object('7500'))
        ie.addFact(supervisor, scrooge, warbucks)

        ie.addFact(robert)
        ie.addFact(address, robert, Object('Allston'))
        ie.addFact(job, robert, accountingAssistant)
        ie.addFact(salary, robert, Object('3000'))
        ie.addFact(supervisor, robert, scrooge)

        ie.addFact(aull)
        ie.addFact(address, aull, Object('Allston'))
        ie.addFact(job, aull, bigWheelAssistant)
        ie.addFact(salary, aull, Object('2500'))
        ie.addFact(supervisor, aull, warbucks)

        ie.addFact(warbucks)
        ie.addFact(address, warbucks, Object('Swellesley'))
        ie.addFact(job, warbucks, bigWheel)
        ie.addFact(salary, warbucks, Object('20000'))

        ie.addFact(ben)
        ie.addFact(address, ben, Object('Slummerville'))
        ie.addFact(job, ben, computerWizzard)
        ie.addFact(salary, ben, Object('6000'))
        ie.addFact(supervisor, ben, warbucks)
        
        ie.addFact(alyssa)
        ie.addFact(address, alyssa, Object('Cambridge'))
        ie.addFact(job, alyssa, computerProgrammer)
        ie.addFact(salary, alyssa, Object('4000'))
        ie.addFact(supervisor, alyssa, ben)

        ie.addFact(cy)
        ie.addFact(address, cy, Object('Cambridge'))
        ie.addFact(job, cy, computerProgrammer)
        ie.addFact(salary, cy, Object('3500'))
        ie.addFact(supervisor, cy, ben)

        ie.addFact(lemmy)
        ie.addFact(address, lemmy, Object('Boston'))
        ie.addFact(job, lemmy, computerTechnician)
        ie.addFact(salary, lemmy, Object('2500'))
        ie.addFact(supervisor, lemmy, ben)

        ie.addFact(luis)
        ie.addFact(address, luis, Object('Slummerville'))
        ie.addFact(job, luis, computerTrainee)
        ie.addFact(salary, luis, Object('2500'))
        ie.addFact(supervisor, luis, alyssa)

        ie.addFact(canDoJob, computerWizzard, computerProgrammer)
        ie.addFact(canDoJob, computerWizzard, computerTechnician)
        ie.addFact(canDoJob, computerProgrammer, computerTrainee)
        ie.addFact(canDoJob, bigWheelAssistant, bigWheel)

        l = toList(ie.eval(job, X, computerProgrammer))
        self.assertTrue(l == [{X: alyssa}, {X: cy}])
        l2 = toList(ie.eval(address, X, Y))
        self.assertTrue(len(l2) == 9)
        l3 = toList(ie.eval(supervisor, X, X))
        self.assertTrue(len(l3) == 0)






if __name__ == '__main__':
    unittest.main()
