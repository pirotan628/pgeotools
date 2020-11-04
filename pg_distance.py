import pyproj

grs80 = pyproj.Geod(ellps='GRS80')  # GRS80楕円体

lon1, lat1 = 135.292489, 34.717932  # 深江

#infile='mbes_survey_area_1.txt'
#infile='MCS_plan.xy'
infile='Line20201018_transit2.gmt'

point=0
total=0
eta=0
speed=8.5  #knot

f = open(infile)
line = f.readline()

token = [x.strip() for x in line.split(' ')]
lon1, lat1 = token[0], token[1]

while line:
      point=point+1
      token = [x.strip() for x in line.split(' ')]
      lon2, lat2 = token[0], token[1]

      azimuth, bkw_azimuth, distance = grs80.inv(lon1, lat1, lon2, lat2)
      nauticalmile = distance / 1852
      total=total+nauticalmile
      eta=total/speed

      print('{:03d}'.format(point), '{:6.01f}'.format(azimuth), '{:6.01f}'.format(bkw_azimuth),end="")
      print('{:10.02f}'.format(distance), '{:7.02f}'.format(nauticalmile),'{:10.02f}'.format(total),'{:7.02f}'.format(eta))

      lat1, lon1 = lat2, lon2
      line = f.readline()

f.close()
