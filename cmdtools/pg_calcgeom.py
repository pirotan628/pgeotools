import sys
import pgeotools as pg

utm_zone = pg.param_config.PROJECT_UTM

lines = sys.stdin

gps_pos = []
for l in lines:
    x,y = pg.readxy(l)
    lon, lat = pg.utm2gmt(x,y,utm_zone)
    pos = [lon, lat]
    gps_pos.append(pos)

ship_conf = pg.ship_configuration(17,-0.8,27,2.7)
coords = pg.calc_geom_from_ship_conf(ship_conf, gps_pos, utm_zone)