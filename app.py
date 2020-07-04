from flask_mysqldb import MySQL

from flask import Flask, request, jsonify, url_for, redirect, session,render_template, g

app = Flask(__name__)

app.config['SECRET_KEY'] = "seckey"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root1'
app.config['MYSQL_PASSWORD'] = 'root1@pass'
app.config['MYSQL_DB'] = 'todo_app'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)


@app.route('/')
def index():
    return "<h1> Hello </h1>"


@app.route('/home/<name>', methods=['POST', 'GET'], defaults={'name': 'user'})
@app.route('/home/<name>', methods=['POST', 'GET'])
def home(name):
    logged = False
    if 'name' in session:
        name = session['name']
        logged = True
    mylist = [1,2,3,4]
    return render_template('home.html',name=name,logged = logged , mylist = mylist)
    #return "<h1> Hi {} , Welcome".format(name)

@app.route('/logout')
def logout():
    session.pop('name',None)
    return redirect(url_for('home'))

@app.route('/json')
def json():
    return jsonify({'name': 'User', 'marks': [1, 2, 3]})


@app.route('/query')
def query():
    name = request.args.get('name')
    location = request.args.get('location')
    return "<h1> Hi {} , Your location is {} </h1>".format(name, location)


@app.route('/form')
def form():
    return ''' <form action="/process" method="POST">
            <input type="text" name="name">
            <input type="text" name="location">
            <input type="Submit" value="Submit">
            </form>
            '''


@app.route('/process', methods=["POST"])
def process():
    name = request.form['name']
    location = request.form['location']
    session['name'] = name
    return redirect(url_for('home'))
    #return redirect(url_for('home', name=name, location=location))
    # return "{} sumitted form.".format(name)



@app.route('/json', methods=["POST"])
def process_json():
    data = request.get_json()
    name = data['name']
    location = data['location']
    return "<h1> Hi {} , you are from {}".format(name, location)

@app.route('/view')
def get_result():
    cur = mysql.connection.cursor()
    #cur.text_factory = str
    cur.execute("select * from user")
    result = cur.fetchall()
    #print(result)
    return render_template('home.html', name = "default", logged = False , mylist = result)



if __name__ == "__main__":
    app.run(debug=True)
