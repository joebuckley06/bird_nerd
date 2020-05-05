from birds.models import GeoStates,Species,Routes,StateCodes,UsStates,Weather
import pandas as pd
#import geopandas as gpd
import numpy as np
import json
from bokeh.models import (
    Range1d,
    GeoJSONDataSource,
    HoverTool,
    ColorBar,
    LinearColorMapper,
    GMapPlot, GMapOptions, ColumnDataSource, 
    Circle, DataRange1d, PanTool, WheelZoomTool, BoxSelectTool, Div,
    CDSView, BooleanFilter
)
from bokeh.models import Select, Slider
from bokeh.layouts import widgetbox, row, column
from bokeh.plotting import figure, output_file, show, curdoc
from bokeh.palettes import brewer
from bokeh.resources import INLINE
from django.core.serializers import serialize
from django_pandas.io import read_frame
import sys
from djgeojson.serializers import Serializer as GeoJSONSerializer
import wikipedia
from string import capwords
from bokeh.client import pull_session
from bokeh.embed import server_session

def species_sizer(number):
    try:
        if int(number) == 0:
            return(0)
        elif(int(number)<5):
            return(2)
        elif(int(number)>=5 & int(number)<10):
            return(4)
        elif(int(number)>=10 & int(number)<20):
            return(6)
        elif(int(number)>=20 & int(number)<50):
            return(8)
        elif(int(number)>=50 & int(number)<70):
            return(10)
        elif(int(number)>=70 & int(number)<100):
            return(12)
        elif(int(number)>=100 & int(number)<500):
            return(15)
        elif(int(number)>=500 & int(number)<1000):
            return(20)
        elif(int(number)>=1000):
            return(25)
        else:
            return(0)
    except:
        return(0)

def bird_lookup(bird_type):
    """Combine datasets for given bird and year"""
    # Retrieve datasets
    routes = read_frame(Routes.objects.values('countrynum', 'statenum', 'route', 'routename', 'active', 'latitude', 'longitude'))
    weather = read_frame(Weather.objects.values('countrynum', 'statenum', 'route', 'year', 'routedataid', 'rpid'))
    species = read_frame(Species.objects.values('aou', 'english_common_name'))
    total_state_df = read_frame(UsStates.objects.filter(aou=bird_type).values('countrynum', 'statenum', 'route', 'year','routedataid','rpid','aou', 'stoptotal', 'speciestotal'))

    # Merge into one dataframe
    all_df = pd.merge(weather, routes,  
                 how='left', left_on=['countrynum','statenum','route'], 
                 right_on = ['countrynum','statenum','route'])
    all_df = pd.merge(all_df,total_state_df,how='right', 
                      left_on=['countrynum','statenum','route','routedataid','rpid','year'], 
                     right_on = ['countrynum','statenum','route','routedataid','rpid','year'])
    all_df = pd.merge(all_df,species,how='left',on='aou')
    # Get sizes of dots per number of sightings
    all_df['species_size'] = all_df['speciestotal'].apply(species_sizer)
    all_df['routename'] = [capwords(state) for state in all_df['routename']]
    return(all_df)

def bird_cleaner(bird_list):
    new_list=[]
    for i in bird_list:
        if 'unid' in i:
            pass
        elif 'hybrid' in i:
            pass
        else:
            new_list.append(i)
    return(sorted(set(new_list)))


class bird_sightings:
  """Graphs and tables for bird sightings in the US"""
  def __init__(self,bird='Bald Eagle'):
    self.bird=bird
    self.aou_number = Species.objects.filter(english_common_name=bird).values('aou')[0]['aou']
    self.df_bird = bird_lookup(self.aou_number)[['countrynum','statenum','route','longitude',
                  'latitude',
                  'speciestotal',
                  'routename',
                  'english_common_name',
                  'year',
                  'species_size']].copy()
    # Import data
    #gdf_us = read_frame(GeoStates.objects.all())
    geo_data = GeoJSONSerializer().serialize(GeoStates.objects.all().exclude(states='Alaska').exclude(states='Hawaii'), use_natural_keys=True, geometry_field='geo')
    # Input GeoJSON source that contains features for plotting.
    geosource = GeoJSONDataSource(geojson = geo_data)
    # json_data did not work because of overflow

    # Data source of bird sightings, with view filter 
    self.bird_source = ColumnDataSource(data=self.df_bird)
    self.booleans = [True if int(x) == 2018 else False for x in self.bird_source.data['year']]
    self.view1 = CDSView(source = self.bird_source, filters=[BooleanFilter(self.booleans)])

    # Graphing
    TOOLS = "pan,wheel_zoom,box_zoom,reset" 
    species_list = read_frame(Species.objects.values('english_common_name'))
    print(type(list(species_list['english_common_name'])))
    bird_list = bird_cleaner(list(species_list['english_common_name']))
    print(bird_list[5:25])
    

    # #Define a sequential multi-hue color palette.
    palette = brewer['YlGnBu'][5]

    # #Reverse color order so that dark blue is highest number.
    palette = palette[::-1]

    # #Instantiate LinearColorMapper that maps numbers in a range linearly into a sequence of colors. Input nan_color.
    color_mapper = LinearColorMapper(palette = palette, low = 0, high = 25, nan_color = '#d9d9d9')

    # #Define custom tick labels for color bar.
    tick_labels = {'0': '0%', '5': '5%', '10':'10%', '15':'15%', '20':'20%', '25':'>25%'}

    # #Create color bar. 
    color_bar = ColorBar(color_mapper=color_mapper, label_standoff=5,width = 500, height = 20,
    border_line_color=None,location = (0,0), orientation = 'horizontal', major_label_overrides = tick_labels)

    # #Create figure object.
    #Create figure object.
    self.Elevated = figure(title = 'Birds in the states, 2018', 
                      plot_height = 500 , 
                      plot_width = 750, 
                      tools = TOOLS,
                      sizing_mode="stretch_both",)
    self.Elevated.xgrid.grid_line_color = None
    self.Elevated.ygrid.grid_line_color = None
    self.Elevated.yaxis.visible = False
    self.Elevated.xaxis.visible = False

    #Add patch renderer to figure. 
    a = self.Elevated.patches('xs','ys', source = geosource, fill_color = '#aaaaaa',
              line_color = 'black', line_width = 0.25, fill_alpha = 1)

    #Specify figure layout.
    #Elevated.add_layout(color_bar, 'below')

    # Add bird data for washington
    b = self.Elevated.circle('longitude', 
                    'latitude', 
                    source=self.bird_source, 
                    size='species_size',
                    view = self.view1,
                    color='#052e67',
                    name='bird_dots')

    
    # Define the callback function: update_plot
    def update_bird(attr, old, new):
        bird = self.select.value
        bird_aou = int(species[species['english_common_name']==bird]['aou'])
        yr = self.slider.value
        new_bird_df = bird_lookup(bird_aou)[['countrynum','statenum','route','longitude',
                                      'latitude',
                                      'speciestotal',
                                      'routename',
                                      'english_common_name',
                                      'year',
                                      'species_size']]
        print(bird, yr)
        self.bird_source.data = ColumnDataSource(new_bird_df).data
        self.booleans = [True if int(x) == yr else False for x in self.bird_source.data['year']]
        self.view1.filters = [BooleanFilter(booleans)]
        try:
            #table_source.data = ColumnDataSource(bird_table_data(yr)).data
            #wiki_page = wikipedia.page(bird)
            #image_summary.text = wiki_page.html()
            self.Elevated.title.text = 'Sightings of ' + str(bird) +', %d' %yr
            #data_table.visible = True
        except: 
            #wiki_page = wikipedia.page(bird)
            #image_summary.text = wiki_page.html()
            self.Elevated.title.text = 'Sightings of ' + str(bird) +', %d' %yr
            #data_table.visible = False

    
    # Define the callback function: update_plot
    def update_year(attr, old, new):
        yr = self.slider.value
        print(yr)
        self.booleans = [True if int(x) == yr else False for x in bird_source.data['year']]
        self.view1.filters = [BooleanFilter(self.booleans)]
        try:
            #table_source.data = ColumnDataSource(bird_table_data(yr)).data
        # view = CDSView(source = all_source, filters=[BooleanFilter(booleans)])
            self.Elevated.title.text = 'Sightings of ' + str(select.value) +', %d' %yr
            #data_table.visible = True
        except:
            #table_source.data = ColumnDataSource(None).data
            self.Elevated.title.text = 'No Sightings of ' + str(select.value) +', %d' %yr
            #data_table.visible = False

    # Select tool for bird selection
    self.select = Select(title="Bird:", value='Bald Eagle', options=bird_list)
    self.select.on_change('value', update_bird)

    # Make a slider object: slider 
    self.slider = Slider(title = 'Year',start = 1966, end = 2018, step = 1, value = 2018)
    self.slider.on_change('value', update_year)

    # Hover
    self.Elevated.add_tools(HoverTool(renderers=[b],
                      tooltips=[("Bird", "@english_common_name"),
                                  ("Count", "@speciestotal"),
                                  ("Route", "@routename"),
                                  ("Year", "@year")],
                      names = ['bird_dots']))               
    #self.layout = column(row(widgetbox(self.select),widgetbox(self.slider)),self.Elevated)
    #self.statechart = Elevated

  def state_graph(self):
      session = pull_session(curdoc())
      script_server = server_session(self.Elevated,session_id=session.id)
      return(script_server)

  def bird_table_data(self,year):
    data = bird_source.data
    df = pd.DataFrame(data)
    df_states = pd.merge(df,state_codes,how='left', 
                          left_on=['countrynum','statenum'], 
                         right_on = ['countrynum','statenum'])
    df_states['State'] = [capwords(state) for state in df_states['state_name']]
    df_states = df_states.groupby(['State','year'],
                                  as_index=False)['speciestotal'].sum().sort_values('speciestotal',ascending=False)
    df_states = df_states.rename(columns={'speciestotal':'BirdCount','year':'Year'})
    df_states = df_states[df_states['Year']==year]
    return(df_states)
    

