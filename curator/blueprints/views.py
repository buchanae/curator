from django.shortcuts import render, render_to_response

from models import Blueprint, ReactionSpecies, Species

def test(request):
    return render_to_response('test.html')

def export(request, ID):
    b = Blueprint.objects.get(id=ID)
    s = Species.objects.filter(blueprint=b)

    response = render(request, 'export.html', {
      'blueprint': b,
      'compartments': ReactionSpecies.COMPARTMENTS,
      'species': s,
    }, content_type="application/xhtml+xml")

    filename = 'export_{0}.sbml'.format(b.name)
    response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)

    return response
