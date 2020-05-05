from django.shortcuts import render
from birds.models import Routes, Weather, GeoStates
from .scripts import bird_sightings
from bokeh.embed import components
from bokeh.plotting import figure, output_file, show
from bokeh.resources import INLINE


def sightings(request):
  route_data = Routes.objects.filter(statenum=89)[:5]
  weather_data= Weather.objects.filter(statenum=2)[:5]
  geo_data = GeoStates.objects.filter(states='Alabama')
  test_graph = bird_sightings()
  #plots = {'state': test_graph.state_graph(),}
  resources = INLINE.render()
  # # script, div_all = components(plots)
  #script, div = components(plots)
  server_script = test_graph.state_graph()

  context = {'routes': route_data,
              'weather':weather_data,
              'geo_data':geo_data,
              'resources':resources,
              's_script':server_script,}
              # 'script':script,
              # 'div':div}
  return render(request,'sightings/sightings.html',context)
