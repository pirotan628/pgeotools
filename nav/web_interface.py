from bottle import route, run, template, redirect, request

lat = "0"

@route("/")
def index():
    global lat
    return template("index", testword=lat)

@route("/input", method="POST")
def input():
    global lat
    lat = request.forms.get('lat')
    lon = request.forms.get('lon')
    dec = request.forms.get('dec')
    return str(lat),str(lon),str(dec)
#    return redirect("/")

run(host="localhost", port=8080, debug=True, reloader=True)