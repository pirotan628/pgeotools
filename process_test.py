from segytools import *

PROJECT_UTM = +53

basename = []

#basename.append('OB2001')
#basename.append('OB2002')
basename.append('OB2003')
#basename.append('OB2004')
#basename.append('OB2005_1-5440')
#basename.append('OB2005_5601-7381')
#basename.append('OB2006_1-2100')
#basename.append('OB2006_2201-5859')

s1 = makesufgrp(basename)

#su_segyread(s1)
#testsu(s1)
#create_sps_from_descrete(s1, WRKHOME+PATH_ASC+'202006_gpsdata'+EXT_TXT)

spsfile = WRKHOME + PATH_ASC + basename[0] + EXT_SPS
config = ship_configuration(17.0, -0.8, 27.0, 2.7)
sps2sugeom(spsfile, config)