from typing import List
from basics import Fact, Statement, Rule


'''
The knowledge-base contains a bipartite graph of facts and rules.
'''

class KnowledgeBase:
    def __init__(self):
        self.facts: List[Fact] = []
        self.rules: List[Rule] = []

    def addFact(self, newFact: Fact):
        self.facts.append(newFact)

    def addRule(self, newRule: Rule):
        self.rules.append(newRule)



class InferenceEngine:
    def __init__(self, knowledgeBase):
        self.knowledgeBase = knowledgeBase

    def isTrue(self, statement) -> bool:
        pass

    def forwardChain(self):
        for rule in self.knowledgeBase.rules:
            premisses = rule.premisses
            facts = self.knowledgeBase.selectAllBy(premisses)
            


if __name__ == "__main__":
    pass