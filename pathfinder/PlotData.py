from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource, GMapOptions
from bokeh.plotting import gmap
from .model import CrimeScene
from bokeh.io import output_file, output_notebook, show, save
from bokeh.models import (
  GMapPlot, GMapOptions, ColumnDataSource, Circle, LogColorMapper, BasicTicker, ColorBar,
    Range1d, PanTool, WheelZoomTool, BoxSelectTool
)
from bokeh.models.mappers import ColorMapper, LinearColorMapper
from bokeh.palettes import Viridis5
import os


def get_co_ordinates():
	crimes_scenes = CrimeScene.query.all()
	longitudes = [ crimescene.longitude for crimescene in crimes_scenes ]
	latitudes = [ crimescene.latitude for crimescene in crimes_scenes ]
	return latitudes,longitudes




def showmap():
    map_options = GMapOptions(lat=0.3132008, lng=32.5290843, map_type="roadmap", zoom=11)
    GOOGLE_API_KEY = "AIzaSyAFCR-n7VxtftzPKR4gCje1T-cAxQXn7S8"
    plot = gmap(GOOGLE_API_KEY, map_options, title="Crimes visualizing center")
    latitude_list,longitude_list = get_co_ordinates()
    source = ColumnDataSource(
           data=dict(
	       lat=latitude_list,
               lon=longitude_list
           )
    )
    plot.circle(x="lat", y="lon", size=15, fill_color="blue", fill_alpha=0.8, source=source)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    storage_path = os.path.join(BASE_DIR, 'pathfinder/templates/pages')
    map_path = os.path.join(storage_path, 'gmap_plot.html')
    output_file(map_path)
    print("saved...")
    save(plot)

