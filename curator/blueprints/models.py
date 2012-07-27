from django.db import models


class Blueprint(models.Model):
    name = models.CharField(max_length=100)


class Species(models.Model):
    name = models.CharField(max_length=100)
    formula = models.CharField(max_length=50)
    charge = models.IntegerField(default=0)


class ReactionSpecies(models.Model):
    class Meta:
        abstract = True

    COMPARTMENTS = (
        ('e', 'Extra Cellular'),
        ('c', 'Cytosol'),
    )
    compartment = models.CharField(max_length=1, choices=COMPARTMENTS)
    stiochiometry = models.FloatField(default=0.0)
    species = models.ForeignKey('Species')
    reaction = models.ForeignKey('Reaction')


class Reactant(ReactionSpecies): pass
class Product(ReactionSpecies): pass
    

class Reaction(models.Model):
    blueprint = models.ForeignKey('Blueprint')

    name = models.CharField(max_length=100)
    reversible = models.BooleanField(default=False)

    reactants = models.ManyToManyField('Species', related_name='reactants',
                                       through='Reactant')
    products = models.ManyToManyField('Species', related_name='products',
                                      through='Product')

    lower_bound = models.IntegerField(default=0)
    upper_bound = models.IntegerField(default=0)
    objective_coefficent = models.FloatField(default=0.0)
    flux_value = models.FloatField(default=0.0)