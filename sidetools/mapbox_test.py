import requests
from io import BytesIO
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from PIL import Image
#%matplotlib inline

# min/max circle size of plot
min_size = 200
max_size = 2000

# Retrive static OpenStreetMap
def get_osm_img(minlat, minlon, maxlat, maxlon, scale=60000, img_format='png'):
    url = 'http://www.openstreetmap.org/export/finish'
    payload = {
        'mapnik_format': img_format, 
        'mapnik_scale': scale, 
        'minlon': minlon, 
        'minlat': minlat, 
        'maxlon': maxlon, 
        'maxlat': maxlat, 
        'format': 'mapnik'
    }
    response = requests.post(url, payload)
    return Image.open(BytesIO(response.content))

fig = plt.figure(figsize=(15, 15))

minlat, minlon, maxlat, maxlon = 35.61, 139.67, 35.75, 139.80
bmap = Basemap(projection='merc', llcrnrlat=minlat, urcrnrlat=maxlat, llcrnrlon=minlon, urcrnrlon=maxlon, lat_ts=0, resolution='l')

x, y = bmap(data['lon'].values, data['lat'].values)

file_name = 'osm.png'
bg_img = None
try:
    bg_img = Image.open(file_name)
except FileNotFoundError as fnfe:
    bg_img = get_osm_img(minlat=minlat, minlon=minlon, maxlat=maxlat, maxlon=maxlon, scale=60000)
    bg_img.save(file_name)
bmap.imshow(bg_img, origin='upper')
bmap.scatter(x, y, c=data['passenger'], cmap=plt.cm.get_cmap('seismic'), alpha=0.5, s=data['passenger'].map(lambda x: (x - data['passenger'].min()) / (data['passenger'].max() - data['passenger'].min()) * (max_size - min_size) + min_size))

# plt.colorbar()
plt.show()
# plt.savefig('out.png')
