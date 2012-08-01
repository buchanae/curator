import os

from jingo import env, register


@register.function
def handlebars_source(name):
    t = env.loader.get_source(env, os.path.join('handlebars', name))
    return t[0]
