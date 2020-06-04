from bottle import route, run, template, redirect, request

def get_param():
    reffile = 'param.txt'
    f = open(reffile)
    lines = f.read()
    f.close()

    line = lines.split('\n')
    coord = line[0].split(',')
    #lon_ref, lat_ref = 135.292489, 34.717932  # 深江
    lon, lat = float(coord[0]), float(coord[1])

    #declination = -7.5
    dec = float(line[1])

    return lon, lat, dec

def put_param(lon, lat, dec):
    reffile = 'param.txt'
    f = open(reffile, mode='w')
    f.write(lon + ', ' + lat + '\n')
    f.write(dec)
    f.close
    return 0

def get_info():
    inffile = 'info.txt'
    f = open(inffile)
    lines = f.read()
    f.close()

    line = lines.split('\n')
    time_n = line[0]
    coord = line[1].split(',')
    inf1 = line[2].split(',')
    inf2 = line[3].split(',')
    lon, lat = float(coord[0]), float(coord[1])
    azm, bkw_azm, distkm, distnm = inf1[0], inf1[1], inf1[2],inf1[3]
    azm_m, bkw_azm_m = inf2[0],inf2[1]
    return time_n, lon, lat, azm, bkw_azm, azm_m, bkw_azm_m, distkm, distnm

@route("/")
def index():
    global lat,lon,dec
    lon,lat,dec = get_param()
    time_n, lon_n, lat_n, azm, bkw_azm, azm_m, bkw_azm_m, distkm, distnm = get_info()
    context_data = {
        'time_n': time_n,
        'lon_n': lon_n,
        'lat_n': lat_n,
        'azm': azm,
        'bkw_azm': bkw_azm,
        'azm_m': azm_m,
        'bkw_azm_m': bkw_azm_m,
        'distkm': distkm,
        'distnm': distnm,
        'lat': lat,
        'lon': lon,
        'dec': dec,
    }
    
    return template("index", **context_data)

@route("/input", method="POST")
def input():
    global lat,lon,dec
    lat = request.forms.get('lat')
    lon = request.forms.get('lon')
    dec = request.forms.get('dec')
    dummy = put_param(lon,lat,dec)
    return redirect("/")

@route("/refresh", method="POST")
def refresh():
    return redirect("/")  

run(host="localhost", port=8080, debug=True, reloader=True)