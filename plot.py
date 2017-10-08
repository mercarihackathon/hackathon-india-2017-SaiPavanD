import gdal
import numpy as np
import itertools
import xml.etree.ElementTree as ET
import os
import sys
import gmplot
import subprocess, os

def local_minima(array2d, lim):
    return ((np.roll(array2d,  1, 0) - array2d > lim) &
            (np.roll(array2d, -1, 0) - array2d > lim) &
            (np.roll(array2d,  1, 1) - array2d > lim) &
            (np.roll(array2d, -1, 1) - array2d > lim))

# dirname = sys.argv[1]
dirname = 'cdne44m_v3r1'
fname = dirname.split('_')[0]

root = ET.parse(os.path.join(dirname, fname+'.xml')).getroot()

# up_left = root.find('.//Upper_left').text.split(' ')
# low_right = root.find('.//Lower_right').text.split(' ')
#
# lat_min = int(''.join(x for x in low_right[5] if x.isdigit()))
# lat_max = int(''.join(x for x in up_left[5] if x.isdigit()))
# long_min = int(''.join(x for x in up_left[2] if x.isdigit()))
# long_max = int(''.join(x for x in low_right[2] if x.isdigit()))
lat_min = 17.2
lat_max = 17.6
long_min = 78.2
long_max = 78.7

ds = gdal.Open(os.path.join(dirname, fname+'.tif'))
dat = ds.ReadAsArray()
is_min = local_minima(dat, 0)

lat_list = []
long_list = []
lat_size = dat.shape[0]
long_size = dat.shape[1]
lat_res = 1.0 / lat_size
long_res = 1.0 / long_size
dat = dat[int(0.2*lat_size):int(0.6*lat_size),int(0.2*long_size):int(0.7*long_size)]

for i, j in itertools.product(xrange(dat.shape[0]), xrange(dat.shape[1])):
    if is_min[i,j]:
        lat_list.append(lat_min + i * lat_res)
        long_list.append(long_min + j * long_res)

# print dat.shape[0], dat.shape[1]
# print len(lat_list), len(long_list)

gmap = gmplot.GoogleMapPlotter((lat_min+lat_max)/2.0,(long_min+long_max)/2.0, 14)
gmap.heatmap(lat_list, long_list)
gmap.draw('map.html')

if sys.platform.startswith('darwin'):
    subprocess.call(('open', 'map.html'))
elif os.name == 'nt':
    os.startfile('map.html')
elif os.name == 'posix':
    subprocess.call(('xdg-open', 'map.html'))
