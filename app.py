from flask import Flask,jsonify,redirect,request,url_for,render_template,flash, session
from flask_cors import CORS
from flask_pymongo import PyMongo
import bcrypt
import json
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'testing'

cors = CORS(app,resources={r"/*": {"origins":"*"}})

app.config['MONGO_URI']='mongodb://localhost:2717/Hola'

mongo=PyMongo(app)

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=='POST':
       users = mongo.db.Adios
       sign_user = users.find_one({'username': request.form['username']})

       da=bytes(request.form['password'], 'utf-8')

       if sign_user:
           if bcrypt.checkpw(da,sign_user['password']):
              session['name']=sign_user['name']
              return redirect(url_for('home'))

       flash('Username and password combination is wrong')
       titu="Login"
       return render_template('login.html',titu=titu)

    titu="Login"
    return render_template('login.html',titu=titu)

@app.route('/logout')
def cerrar():
    if 'name' in session:
        session.pop('name')
        return redirect(url_for('gett'))


@app.route('/index')
@app.route('/',methods=['GET'])
def gett():
    if 'name' in session:
        return redirect(url_for('home'))
    else:
        titu="Inicio"
        return render_template('index.html', titu=titu)

@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method=='POST':
        users = mongo.db.Adios
        signup_user = users.find_one({'username': request.form['username']})
        
        if signup_user:
            flash(request.form['username'] + ' username is already exist')
            return redirect(url_for('signup'))

        hashed = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt(14))
        users.insert({'username': request.form['username'], 'password': hashed, 'name': request.form['name']})
       
        return redirect(url_for('gett'))

    titu="Registro"
    return render_template('signp.html',titu=titu)    

@app.route('/home')
def home():
    if 'name' in session:
        support=call()
        titu="Home"
        dap=session['name']
        return render_template('home.html',titu=titu,support=support,name=dap)
    else:
        return redirect(url_for('gett'))

@app.route('/home/<string:cur>')
def change(cur):
    if 'name' in session:
        value=wall(cur)
        dap=session['name']
        return render_template('charts.html',value=value,cur=cur,name=dap)
    else:
        return redirect(url_for('gett'))

def wall(cur):
    link='https://api.coindesk.com/v1/bpi/currentprice/'
    cur=cur+'.json'
    link=link+cur
    support=requests.get(link)
    support=json.loads(support.content)
    return support
    
def call():
    support=requests.get('https://api.coindesk.com/v1/bpi/supported-currencies.json')
    support2=json.loads(support.content)
    return support2

if __name__ == '__main__':
     app.run(host="0.0.0.0",debug = True, port = 4000)
