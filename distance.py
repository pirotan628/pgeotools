import pyproj

grs80 = pyproj.Geod(ellps='GRS80')  # GRS80楕円体


lon1, lat1 = 135.292489, 34.717932  # 深江

#infile='mbes_survey_area_1.txt'
infile='MCS_plan.xy'

f = open(infile)
line = f.readline()

while line:
      token = [x.strip() for x in line.split(' ')]
      lon2, lat2 = token[0], token[1]
      azimuth, bkw_azimuth, distance = grs80.inv(lon1, lat1, lon2, lat2)
      nauticalmile = distance / 1852
      
      print(azimuth, bkw_azimuth, distance, nauticalmile)

      lat1, lon1 = lat2, lon2
      line = f.readline()

f.close()
