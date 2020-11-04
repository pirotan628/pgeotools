from segytools import *

basename = []

basename.append('OB2001')
#basename.append('OB2002')
#basename.append('OB2003')
#basename.append('OB2004')
#basename.append('OB2005_1-5440')
#basename.append('OB2005_5601-7381')
#basename.append('OB2006_1-2100')
#basename.append('OB2006_2201-5859')

s1 = makesufgrp(basename)

#read_segy(s1)
#testsu(s1)
create_sps_from_descrete(s1, WRKHOME+PATH_ASC+'202006_gpsdata'+EXT_TXT)