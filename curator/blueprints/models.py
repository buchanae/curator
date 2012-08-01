from django.db import models
from django.core.urlresolvers import reverse


class Blueprint(models.Model):
    name = models.CharField(max_length=100)

    def export_uri(self):
        return reverse('export', args=[self.id])

# TODO better name is Compound or Molecule?
class Species(models.Model):
    blueprint = models.ForeignKey('Blueprint')

    name = models.CharField(max_length=100)
    formula = models.CharField(max_length=50)
    charge = models.IntegerField(default=0)


class ReactionSpecies(models.Model):
    class Meta:
        abstract = True

    COMPARTMENTS = (
        ('extra_cellular', 'Extra Cellular'),
        ('cytosol', 'Cytosol'),
    )
    compartment = models.CharField(max_length=50, default='cytosol',
                                   choices=COMPARTMENTS)
    stoichiometry = models.FloatField(default=0.0)
    species = models.ForeignKey('Species')


class Reactant(ReactionSpecies):
    reaction = models.ForeignKey('Reaction', related_name='reactants')

class Product(ReactionSpecies):
    reaction = models.ForeignKey('Reaction', related_name='products')
    

class Reaction(models.Model):
    blueprint = models.ForeignKey('Blueprint', related_name='reactions')

    name = models.CharField(max_length=100)
    reversible = models.BooleanField(default=False)
    lower_bound = models.IntegerField(default=0)
    upper_bound = models.IntegerField(default=0)
    objective_coefficient = models.FloatField(default=0.0)
    flux_value = models.FloatField(default=0.0)
