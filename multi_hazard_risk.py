
#from osgeo import gdal
from config import *
import rasterio
from rasterio.features import shapes
import fiona
from rasterstats import zonal_stats
import fiona.crs

#h1 = gdal.Open(h1_path)
#h2 = gdal.Open(h2_path)
bands = [h1_intensity, h1_time, h1_duration]
stat_bands = ['max', 'mean', 'max']
n=0
initial_shape = e1_path
for b in bands:
    stats = zonal_stats(e1_path, h1_path, band=b, stats = ['max', 'mean', 'median'])
    means = [stat[stat_bands[n]] for stat in stats]
    if n>0:
        initial_shape = 'outputs/results.shp'
    with fiona.open(initial_shape) as input:
    # add the mean field to the schema of the resulting shapefile
        schema = input.schema
        schema['properties'][str(b)] = 'float:10.4'
        crs= input.crs
        with fiona.open('outputs/results.shp', 'w', 'ESRI Shapefile', schema,crs) as output:
            for i, feature in enumerate(input):
                feature['properties'][str(b)]= means[i]
                output.write(feature)
	n=n+1	

