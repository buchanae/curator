from tastypie.api import Api
from tastypie.authorization import Authorization
from tastypie import fields
from tastypie.resources import ModelResource

import models


class BlueprintResource(ModelResource):

    reactions = fields.ToManyField('curator.blueprints.api.ReactionResource', 'reactions')

# TODO something for getting set of reactions for blueprint at once
    class Meta:
        queryset = models.Blueprint.objects.all()
        authorization = Authorization()


class SpeciesResource(ModelResource):
    blueprint = fields.ToOneField(BlueprintResource, 'blueprint')

    class Meta:
        queryset = models.Species.objects.all()
        authorization = Authorization()


class ReactantResource(ModelResource):
    species = fields.ToOneField(SpeciesResource, 'species', full=True)

    class Meta:
        queryset = models.Reactant.objects.all()
        authorization = Authorization()


# TODO remove this duplication
class ProductResource(ModelResource):
    species = fields.ToOneField(SpeciesResource, 'species', full=True)

    class Meta:
        queryset = models.Product.objects.all()
        authorization = Authorization()


class ReactionResource(ModelResource):

    blueprint = fields.ToOneField(BlueprintResource, 'blueprint')
    reactants = fields.ToManyField(ReactantResource, 'reactants', full=True)
    products = fields.ToManyField(ProductResource, 'products', full=True)

    class Meta:
        queryset = models.Reaction.objects.all()
        authorization = Authorization()


api = Api(api_name='v1')
api.register(BlueprintResource())
api.register(ReactionResource())
api.register(SpeciesResource())
api.register(ReactantResource())
api.register(ProductResource())
