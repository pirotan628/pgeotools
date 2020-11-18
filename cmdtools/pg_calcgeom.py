import sys
import pgeotools as pg

utm_zone = pg.param_config.PROJECT_UTM

lines = sys.stdin

gps_pos = []
append = gps_pos.append
for l in lines:
    x,y = pg.readxy(l)
    lon, lat = pg.utm2gmt(x,y,utm_zone)
    pos = [lon, lat]
    append(pos)

#print(gps_pos)

ship_conf = pg.ship_configuration(17,-0.8,27,2.7)
coords = pg.calc_geom_from_ship_conf(ship_conf, gps_pos, utm_zone)

for i in range(len(coords)):
    sys.stdout.write("{0:8.1f} {1:9.1f} {2:8.1f} {3:9.1f} {4:5.1f}\n".format(coords[i][0],coords[i][1],coords[i][2],coords[i][3],coords[i][4]))
