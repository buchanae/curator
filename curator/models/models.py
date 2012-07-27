from django.db import models


class Model(models.Model):
    name = models.CharField(max_length=100)


class Species(models.Model):
    name = models.CharField(max_length=100)
    formula = models.CharField(max_length=50)
    charge = models.IntegerField(default=0)


class ReactionSpecies(models.Model):
    COMPARTMENTS = (
        ('e', 'Extra Cellular'),
        ('c', 'Cytosol'),
    )
    compartment = models.CharField(max_length=1, choices=COMPARTMENTS)
    stiochiometry = models.FloatField()
    species = models.ForeignKey('Species')
    reaction = models.ForeignKey('Reaction')


class Reactant(ReactionSpecies): pass
class Product(ReactionSpecies): pass
    

class Reaction(models.Model):
    name = models.CharField(max_length=100)
    reactants = models.ManyToManyField('Species', related_name='reactants',
                                       through='Reactant')
    products = models.ManyToManyField('Species', related_name='products',
                                      through='Product')
    reversible = models.BooleanField()
    model = models.ForeignKey('Model')
