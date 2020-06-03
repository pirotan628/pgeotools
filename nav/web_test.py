from bottle import get, post, request, run 

@get('/') 
def circle_area():
    return '''
        <form action="/calc" method="post">
            半径は何cm？ <input name="radius" type="text" />
            <input value="計算" type="submit" />
        </form>
    '''

@post('/calc')
def circle_area():
    r = request.forms.get('radius')
    print(type(r))
    calc = int(r) * int(r) * 3.14
    return "円の面積：" + str(calc) + "cm2"

run(host='localhost', port=8080, debug=True)

server.stop()
