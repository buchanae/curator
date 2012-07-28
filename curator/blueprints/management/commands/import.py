from __future__ import print_function

from django.core.management.base import BaseCommand, CommandError

from lxml import etree
from lxml import objectify

from curator.blueprints.models import Blueprint, Product, Reaction, Reactant, Species


def multi_getattr(obj, attr, default = None):
    """
    Get a named attribute from an object; multi_getattr(x, 'a.b.c.d') is
    equivalent to x.a.b.c.d. When a default argument is given, it is
    returned when any attribute in the chain doesn't exist; without
    it, an exception is raised when a missing attribute is encountered.

    """
    attributes = attr.split(".")
    for i in attributes:
        try:
            obj = getattr(obj, i)
        except AttributeError:
            if default != None:
                return default
            else:
                raise
    return obj


class Command(BaseCommand):
    args = '<sbml>'
    help = 'Import an SBML model'

    def message(self, msg):
        print(msg, file=self.stderr)

    def handle(self, blueprint_name, sbml_path, **options):

        xml = objectify.parse(sbml_path).getroot().model

        # TODO try to detect SEED and Biocyc models, handle appropriately
        # TODO actual parameter parsing
        # TODO change command name 'import_sbml', 'import_blueprint', or something
        #      to avoid name collisions and ambiguity

        blueprint = Blueprint(name=blueprint_name)
        blueprint.save()

        # SBML species ID to Species object dictionary
        species_objects = {}

        for species_xml in multi_getattr(xml, 'listOfSpecies.species', []):

            SID = species_xml.get('id')
            raw_name = species_xml.get('name')

            name = ''
            formula = ''

            i = raw_name.rfind('_')
            if i != -1:
                name = raw_name[:i]
                formula = raw_name[i + 1:]
            else:
                name = raw_name

            if formula == 'noformula':
                formula = ''

            try:
                s = Species.objects.get(name=name)
            except Species.DoesNotExist:
                s = Species(name=name, formula=formula)
                s.save()

            species_objects[SID] = s


        def save_reaction_species(cls, reaction, refs):
            '''
            Parse reaction species xml, then create and save a ReactionSpecies model
            using this data.

            e.g.
            >>> save_reaction_species(Reactant, reaction_obj, reactants_xml_iterable)

            This little helper saves some code duplication, since Reactants and Products
            are so similar.
            '''

            # a whitelist of ReactionSpecies field names
            # that are allowed to be set from xml-attribute-getting-magic below
            valid_fields = ('compartment', 'stoichiometry', 'species')

            for species in refs:
                try:
                    d = dict(species.items())

                    # use our whitelist to remove any attributes we don't want to set
                    # e.g. 'id'
                    d = dict((k, v) for k, v in d.items() if k in valid_fields)

                    d['species'] = species_objects[d['species']]
                    cls(reaction=reaction, **d).save()

                except KeyError:
                    self.message('Missing species.  Was looking for ' + d['species'])

                except AttributeError as e:
                    self.message(e)


        # a whitelist of Reaction field names
        # that are allowed to be set from xml-attribute-getting-magic below
        valid_fields = ('name', 'lower_bound', 'upper_bound', 'objective_coefficient',
                        'reversible', 'flux_value')

        for reaction_xml in multi_getattr(xml, 'listOfReactions.reaction', []):

            # a little magic to easily get a bunch of xml parameters.
            # getting them one-by-one is too verbose
            # (check for existence, get attribute, set default)
            d = dict(reaction_xml.items())

            parameters_xml = multi_getattr(reaction_xml,
                                           'kineticLaw.listOfParameters.parameter')
            d.update(dict((x.get('id').lower(), x.get('value')) for x in parameters_xml))

            # use our whitelist to remove any attributes we don't want to set
            # e.g. 'id'
            d = dict((k, v) for k, v in d.items() if k in valid_fields)

            reaction = Reaction(blueprint=blueprint, **d)
            reaction.save()

            reactants_xml = multi_getattr(reaction_xml,
                                          'listOfReactants.speciesReference', [])
            products_xml = multi_getattr(reaction_xml,
                                         'listOfProducts.speciesReference', [])

            save_reaction_species(Reactant, reaction, reactants_xml)
            save_reaction_species(Product, reaction, products_xml)

            reaction.save()
