from ie.base import Fact, Relation, TestableRelation, Variable, Object, Rule
from ie.engine import InferenceEngine
from ie.relations import And, Or
from ie.geo import GeoObject, intersects
from shapely.geometry import Polygon, LineString


ie = InferenceEngine()
    
aristoteles = Fact('Aristoteles')
mortal = Relation('mortal')
human = Relation('human')
alf = Fact('Alf')
X = Variable('X')
allMenMortal = Rule((human, X), (mortal, X))
ie.addFact(human, aristoteles)
ie.addFact(mortal, alf)
ie.addRule(allMenMortal)

aristotelesIsMortal = ie.evalExpression(mortal, aristoteles)
someoneIsMortal = ie.evalExpression(mortal, Variable('someone'))
bothHumanAndMortal = ie.evalExpression(And, (human, X), (mortal, X))

assert aristotelesIsMortal == [(mortal, aristoteles)]
assert someoneIsMortal == [(mortal, alf), (mortal, aristoteles)]
assert bothHumanAndMortal == [(And, (human, aristoteles), (mortal, aristoteles))]

anne = Object('Anne')
bill = Object('Bill')
charlie = Object('Charlie')
doreen = Object('Doreen')
eve = Object('Eve')
girl = Relation('girl')
boy = Relation('boy')
child = Relation('child')
daughter = Relation('daughter')
son = Relation('son')
S = Variable('S')
M = Variable('M')
F = Variable('F')
sonIf = Rule((And, (child, S, M, F), (boy, S)), (son, S, M, F))
daughterIf = Rule((And, (child, S, M, F), (girl, S)), (daughter, S, M, F))
ie.addRule(sonIf)
ie.addRule(daughterIf)
ie.addFact(girl, anne)
ie.addFact(boy, bill)
ie.addFact(boy, charlie)
ie.addFact(girl, doreen)
ie.addFact(girl, eve)
ie.addFact(child, doreen, anne, bill)
ie.addFact(child, charlie, anne, bill)
ie.addFact(child, eve, anne, bill)
billsParents = ie.evalExpression(son, charlie, M, F)
daughters = ie.evalExpression(daughter, X, M, F)

assert billsParents == [(son, charlie, anne, bill)]
assert daughters == [(daughter, doreen, anne, bill), (daughter, eve, anne, bill)]


volker = Object('Volker')
andreas = Object('Andreas')
michael = Object('Michael')
brother = Relation('brother')
father = Relation('father')
ie.addFact(brother, michael, andreas)
ie.addFact(father, volker, andreas)
ie.addFact(father, volker, michael)
volkerIsMyBrothersFather = ie.evalExpression(And, (father, volker, X), (brother, michael, X))
assert volkerIsMyBrothersFather == [(And, (father, volker, andreas), (brother, michael, andreas))]
# TODO: ie.evalExpression(father, volker, (brother, michael, X))



france = GeoObject('France', Polygon([[0,0],[1,0],[1,1]]))
germany = GeoObject('Germany', Polygon([[0,0],[1,1],[0,1]]))
rhine = GeoObject('Rhine', LineString([[-1,-1],[0,0],[1,1]]))
controls = Relation('controls')

someRiver = Variable('river', GeoObject)
someCountry = Variable('country', GeoObject)
contrIntersecting = Rule([intersects, someRiver, someCountry], [controls, someCountry, someRiver])
ie.addRule(contrIntersecting)
ie.addFact(germany)
ie.addFact(france)
ie.addFact(rhine)

someoneControlsRhine = ie.evalExpression(controls, someCountry, rhine)
assert someoneControlsRhine == [(controls, germany, rhine), (controls, france, rhine)]


vei1 = Object('vei1')
vei2 = Object('vei2')
vei3 = Object('vei3')
vei4 = Object('vei4')

lahar1 = GeoObject('lahar1', Polygon( [
            [
              -78.43757629394531,
              -0.6825094932250956
            ],
            [
              -78.51242065429688,
              -0.707226913459037
            ],
            [
              -78.46435546875,
              -0.7566613544516054
            ],
            [
              -78.43757629394531,
              -0.6825094932250956
            ]
          ]))

lahar2 = GeoObject('lahar2', Polygon([
            [
              -78.43757629394531,
              -0.6811362994451107
            ],
            [
              -78.55705261230469,
              -0.7209587570082753
            ],
            [
              -78.52615356445312,
              -0.8040354989710435
            ],
            [
              -78.44444274902344,
              -0.7429296202184131
            ],
            [
              -78.43757629394531,
              -0.6811362994451107
            ]
          ]))

lahar3 = GeoObject('lahar3', Polygon([
            [
              -78.4368896484375,
              -0.6804497024083547
            ],
            [
              -78.58589172363281,
              -0.7250783020332547
            ],
            [
              -78.57627868652344,
              -0.856901647439813
            ],
            [
              -78.43894958496094,
              -0.7758857091816899
            ],
            [
              -78.4368896484375,
              -0.6804497024083547
            ]
          ]))

lahar4 = GeoObject('lahar4', Polygon([
            [
              -78.4368896484375,
              -0.6797631052738666
            ],
            [
              -78.60099792480469,
              -0.7237051207737014
            ],
            [
              -78.62297058105469,
              -0.9372293187556252
            ],
            [
              -78.42727661132811,
              -0.7834381104743875
            ],
            [
              -78.4368896484375,
              -0.6797631052738666
            ]
          ]))

ashf1 = GeoObject('ashf1', Polygon([
            [
              -78.42315673828125,
              -0.6667177412833734
            ],
            [
              -78.49525451660156,
              -0.6639713444373289
            ],
            [
              -78.47671508789062,
              -0.72164534810518
            ],
            [
              -78.41285705566406,
              -0.6969280040937404
            ],
            [
              -78.42315673828125,
              -0.6667177412833734
            ]
          ]))

ashf2 = GeoObject('ashf2', Polygon([
            [
              -78.4149169921875,
              -0.6605383462350551
            ],
            [
              -78.52272033691406,
              -0.6529857418598318
            ],
            [
              -78.4808349609375,
              -0.7401832682254668
            ],
            [
              -78.39981079101562,
              -0.6969280040937404
            ],
            [
              -78.4149169921875,
              -0.6605383462350551
            ]
          ]))

ashf3 = GeoObject('ashf3', Polygon([
            [
              -78.40599060058594,
              -0.6509259386917885
            ],
            [
              -78.54949951171875,
              -0.6406269102851875
            ],
            [
              -78.4918212890625,
              -0.7580345254974054
            ],
            [
              -78.38058471679686,
              -0.6969280040937404
            ],
            [
              -78.40599060058594,
              -0.6509259386917885
            ]
          ]))

ashf4 = GeoObject('ashf4', Polygon([
            [
              -78.39157104492188,
              -0.6392537049263806
            ],
            [
              -78.58932495117188,
              -0.6179689753949585
            ],
            [
              -78.50349426269531,
              -0.7896173377761679
            ],
            [
              -78.35311889648438,
              -0.7037939461932426
            ],
            [
              -78.39157104492188,
              -0.6392537049263806
            ]
          ]))


laharSim = Relation('LaharSimulation')
for vei, lahar in [(vei1, lahar1), (vei2, lahar2), (vei3, lahar3), (vei4, lahar4)]:
    ie.addFact(laharSim, vei, lahar)

ashfallSim = Relation('AshfallSimulation')
for vei, ashfall in [(vei1, ashf1), (vei2, ashf2), (vei3, ashf3), (vei4, ashf4)]:
    ie.addFact(ashfallSim, vei, ashfall)


V = Variable('V', Object)
L = Variable('L', GeoObject)
AOI = GeoObject('AOI', Polygon([
            [
              -78.44032287597656,
              -0.7703930452206605
            ],
            [
              -78.39225769042969,
              -0.7703930452206605
            ],
            [
              -78.39225769042969,
              -0.7353771481492902
            ],
            [
              -78.44032287597656,
              -0.7353771481492902
            ],
            [
              -78.44032287597656,
              -0.7703930452206605
            ]
          ]))
ie.addFact(AOI)
dangerousVeis = ie.evalExpression(And, (laharSim, V, L), (intersects, L, AOI))
allDangerousVeis = ie.evalExpression(And, (Or, (laharSim, V, L), (ashfallSim, V, L)), (intersects, L, AOI))

assert dangerousVeis == [(And, (laharSim, vei3, lahar3), (intersects, lahar3, AOI)), 
                         (And, (laharSim, vei4, lahar4), (intersects, lahar4, AOI))]
assert allDangerousVeis == [(And, (laharSim, vei3, lahar3), (intersects, lahar3, AOI)), 
                            (And, (laharSim, vei4, lahar4), (intersects, lahar4, AOI)),
                            (And, (ashfallSim, vei4, ashf4), (intersects, ashf4, AOI))]
