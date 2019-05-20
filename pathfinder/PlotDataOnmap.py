DATASETS_URL = "https://github.com/elroypeter/handson-ml/raw/master/datasets"
import os
import tarfile
from six.moves import urllib

HOUSING_PATH = "datasets/housing"
HOUSING_URL = DATASETS_URL + "/housing/housing.tar.gz"

def fetch_housing_data(housing_url=HOUSING_URL, housing_path=HOUSING_PATH):
    if not os.path.exists(housing_path):
        os.makedirs(housing_path)
    tgz_path = os.path.join(housing_path, "housing.tar.gz")
    urllib.request.urlretrieve(housing_url, tgz_path)
    housing_tgz = tarfile.open(tgz_path)
    housing_tgz.extractall(path=housing_path)
    housing_tgz.close()

#fetch_housing_data()
import pandas as pd

def load_housing_data(housing_path=HOUSING_PATH):
    csv_path = os.path.join(housing_path, "housing.csv")
    return pd.read_csv(csv_path)
housing = load_housing_data()
# housing.head()
housingv2 = housing[(housing['median_income'] <= 10)]
#housing['median_income'] = housing['median_income'].apply(lambda x: x * x)
# print(housing.size)
# print(housingv2.size)
# type(housing.latitude.tolist())

from bokeh.io import output_file, output_notebook, show, save
from bokeh.models import (
  GMapPlot, GMapOptions, ColumnDataSource, Circle, LogColorMapper, BasicTicker, ColorBar,
    Range1d, PanTool, WheelZoomTool, BoxSelectTool
)
from bokeh.models.mappers import ColorMapper, LinearColorMapper
from bokeh.palettes import Viridis5


map_options = GMapOptions(lat=0.3132008, lng=32.5290843, map_type="roadmap", zoom=12)

plot = GMapPlot(x_range=Range1d(), y_range=Range1d(), map_options=map_options)

plot.title.text = "Crimes visualizing center"

# For GMaps to function, Google requires you obtain and enable an API key:
#
#     https://developers.google.com/maps/documentation/javascript/get-api-key
#
# Replace the value below with your personal API key:
plot.api_key = "AIzaSyAFCR-n7VxtftzPKR4gCje1T-cAxQXn7S8"

source = ColumnDataSource(
    data=dict(
        lat=housing.latitude.tolist(),
        lon=housing.longitude.tolist(),
        size=housing.median_income.tolist(),
        color=housing.median_house_value.tolist()
    )
)
max_median_house_value = housing.loc[housing['median_house_value'].idxmax()]['median_house_value']
min_median_house_value = housing.loc[housing['median_house_value'].idxmin()]['median_house_value']

#color_mapper = CategoricalColorMapper(factors=['hi', 'lo'], palette=[RdBu3[2], RdBu3[0]])
#color_mapper = LogColorMapper(palette="Viridis5", low=min_median_house_value, high=max_median_house_value)
color_mapper = LinearColorMapper(palette=Viridis5)

circle = Circle(x="lon", y="lat", size="size", fill_color={'field': 'color', 'transform': color_mapper}, fill_alpha=0.5, line_color=None)
plot.add_glyph(source, circle)

color_bar = ColorBar(color_mapper=color_mapper, ticker=BasicTicker(),
                     label_standoff=12, border_line_color=None, location=(0,0))
plot.add_layout(color_bar, 'right')

plot.add_tools(PanTool(), WheelZoomTool(), BoxSelectTool())

def showmap():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    storage_path = os.path.join(BASE_DIR, 'pathfinder/templates/pages')
    map_path = os.path.join(storage_path, 'gmap_plot.html')
    output_file(map_path)
    print("saved...")
    save(plot)

# output_notebook()
