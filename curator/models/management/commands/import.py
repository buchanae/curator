from __future__ import print_function

from django.core.management.base import BaseCommand, CommandError

from lxml import etree
from lxml import objectify

from curator.models.models import Model, Product, Reaction, Reactant, Species

class Command(BaseCommand):
    args = '<sbml>'
    help = 'Import an SBML model'

    def handle(self, model_name, sbml_path, **options):

        xml = objectify.parse(sbml_path)

        # TODO try to detect SEED and Biocyc models, handle appropriately
        model = Model(name=model_name)
        model.save()

        # SBML species ID to Species object dictionary
        species_objects = {}

        for species_xml in xml.getroot().model.listOfSpecies.species:

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


        for reaction_xml in xml.getroot().model.listOfReactions.reaction:

            reaction_name = reaction_xml.get('name')
            reversible = bool(reaction_xml.get('reversible'))

            r = Reaction(name=reaction_name, reversible=reversible, model=model)
            r.save()

            try:
                for reactant_xml in reaction_xml.listOfReactants.speciesReference:

                    compartment = reactant_xml.get('compartment')
                    stoichiometry = float(reactant_xml.get('stoichiometry'))

                    try:
                        species = species_objects[reactant_xml.get('species')]
                    except KeyError:
                        # TODO print failure message
                        continue

                    r.reactants.create(compartment=compartment,
                                       stoichiometry=stoichiometry,
                                       species=species)
            except AttributeError:
                pass

            try:
                for product_xml in reaction_xml.listOfProducts.speciesReference:

                    compartment = product_xml.get('compartment')
                    stoichiometry = float(product_xml.get('stoichiometry'))

                    try:
                        species = species_objects[product_xml.get('species')]
                    except KeyError:
                        # TODO print failure message
                        continue

                    r.products.create(compartment=compartment,
                                       stoichiometry=stoichiometry,
                                       species=species)
            except AttributeError:
                pass
