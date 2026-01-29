"""A simplified module which reproduce the Kadet's dump() issue."""

from box import Box
from kadet import BaseObj
from pprint import pprint


class Disease(BaseObj):
    def new(self):
        self.need("name")

    def body(self):
        self.root.name = self.kwargs.name


class DiseasedTree(BaseObj):
    def new(self):
        self.need("diseases")

    def body(self):
        # If assigned to a key immediately under root, then the issue is not reproduced
        self.root.diseases = self.kwargs.diseases
        # Output: 'diseases': [{'name': 'Powdery Mildew'}],

        # If assigned to a root's inner key, then the issue is reproduced
        self.root.conditions.diseases = self.kwargs.diseases
        # Output: 'conditions': { 'diseases': [ <__main__.Disease object at 0x7c4081dd0050>]},

        # Variation of the above where the inner key is 1st initialized as a dict()
        self.root.constraints = dict()
        self.root.constraints["diseases"] = self.kwargs.diseases
        # Output: 'conditions': { 'diseases': [ <__main__.Disease object at 0x7c4081dd0050>]},

        # Variation of the above where the inner key is 1st initialized as a Box()/Dict()
        self.root.circumstances = Box()
        self.root.circumstances.diseases = self.kwargs.diseases
        # 'circumstances': { 'diseases': [ <__main__.Disease object at 0x7c4081dd0050>]}

        # Variations of all of the above but ruling out lists as a contributor to the issue.

        self.root.primary_condition = self.kwargs.diseases[0]
        # Expected output: 'primary_condition': {'name': 'Powdery Mildew'},

        self.root.primary_constraint = dict()
        self.root.primary_constraint["disease"] = self.kwargs.diseases[0]
        # Expected output: 'primary_constraint': { 'disease': <__main__.Disease object at 0x7c4081dd0050>}}}

        self.root.primary_circumstance = Box()
        self.root.primary_circumstance.disease = self.kwargs.diseases[0]
        # Expected output: 'primary_circumstance': { 'disease': <__main__.Disease object at 0x7c4081dd0050>},


def main():
    disease = Disease(name="Powdery Mildew")
    tree = DiseasedTree(diseases=[disease])
    pprint(tree.dump(), indent=2)
    # Output:
    #
    # { 'circumstances': {'diseases': [<__main__.Disease object at 0x7ed5e68ab860>]},
    #   'conditions': {'diseases': [<__main__.Disease object at 0x7ed5e68ab860>]},
    #   'constraints': {'diseases': [<__main__.Disease object at 0x7ed5e68ab860>]},
    #   'diseases': [{'name': 'Powdery Mildew'}],
    #   'primary_circumstance': { 'disease': <__main__.Disease object at 0x7ed5e68ab860>},
    #   'primary_condition': {'name': 'Powdery Mildew'},
    #   'primary_constraint': { 'disease': <__main__.Disease object at 0x7ed5e68ab860>}}

    # Expected output if the issue did not exist:
    # { 'circumstances': {'diseases': [{'name': 'Powdery Mildew'}]},
    #   'conditions': {'diseases': [{'name': 'Powdery Mildew'}]},
    #   'constraints': {'diseases': [{'name': 'Powdery Mildew'}]},
    #   'diseases': [{'name': 'Powdery Mildew'}],
    #   'primary_circumstance': {'name': 'Powdery Mildew'},
    #   'primary_condition': {'name': 'Powdery Mildew'},
    #   'primary_constraint': {'name': 'Powdery Mildew'}}


if __name__ == "__main__":
    main()
