from tastypie.api import Api
from tastypie import fields
from tastypie.resources import ModelResource

import models


class SpeciesResource(ModelResource):
    class Meta:
        queryset = models.Species.objects.all()


class BlueprintResource(ModelResource):

    reactions = fields.ToManyField('curator.blueprints.api.ReactionResource', 'reactions')

    class Meta:
        queryset = models.Blueprint.objects.all()


class ReactantResource(ModelResource):
    species = fields.ToOneField(SpeciesResource, 'species')

    class Meta:
        queryset = models.Reactant.objects.all()


# TODO remove this duplication
class ProductResource(ModelResource):
    species = fields.ToOneField(SpeciesResource, 'species')

    class Meta:
        queryset = models.Product.objects.all()


class ReactionResource(ModelResource):

    blueprint = fields.ToOneField(BlueprintResource, 'blueprint')
    reactants = fields.ToManyField(ReactantResource, 'reactants')
    products = fields.ToManyField(ProductResource, 'products')

    class Meta:
        queryset = models.Reaction.objects.all()


api = Api(api_name='v1')
api.register(BlueprintResource())
api.register(ReactionResource())
api.register(ReactantResource())
api.register(ProductResource())
api.register(SpeciesResource())
