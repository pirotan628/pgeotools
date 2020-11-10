from pgeotools import segytools

config_file_default = segytools.config_file('','','','','','','','','','','','','','','','')

config_file_default.WRKHOME = '../'

config_file_default.PATH_RAW = 'rawdata/'
config_file_default.PATH_HDR = 'headers/'
config_file_default.PATH_ASC = 'ascdata/'
config_file_default.PATH_WRK = 'working/'
config_file_default.PATH_PRC = 'processed/'

config_file_default.EXT_SGY = '.sgy'
config_file_default.EXT_SU = '.su'
config_file_default.EXT_TXT = '.txt'
config_file_default.EXT_BIN = '.bin'
config_file_default.EXT_SPS = '.sps'

config_file_default.PFX_HDR = 'hdr_'
config_file_default.PFX_BIN = 'bin_'
config_file_default.SFX_ = ''

NMILE = 1852
PROJECT_UTM = +53