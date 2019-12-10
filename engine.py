from typing import List
from basics import Fact, Statement, Rule


class KnowledgeBase:
    def __init__(self):
        self.facts: List[Fact] = []

    def addFact(fact: Fact):
        self.facts.push(fact)


class InferenceEngine:
    def __init__(self):
        self.knowledgeBase = KnowledgeBase()


