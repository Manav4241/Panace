from flask import Flask, render_template,request,redirect,url_for,session
import requests
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import datetime
import pandas as pd
from flask_mysqldb import MySQL,MySQLdb
import bcrypt
# data=pd.read_csv('panace_ingridients.csv')
# data2=pd.read_csv('panace_fooditems.csv')
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/panace'
# app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
app.secret_key = "caircocoders-ednalan-2020"
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'panace'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)






db = SQLAlchemy(app)
class Dishes(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    ingridients = db.Column(db.String(12), nullable=False)
    cuisine= db.Column(db.String(120), nullable=False)
class Display(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(150), nullable=False)
class Dashes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email= db.Column(db.String(150), unique=True)
    item =db.Column(db.String(550), unique=True)



@app.route('/')
def homee():
    return render_template("home.html")
    

@app.route('/register', methods=["GET", "POST"]) 
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())
        a="gowathm"
        cur = mysql.connection.cursor()
       
        cur.execute("INSERT INTO users (name, email, password) VALUES (%s,%s,%s)",(name,email,hash_password,))
        
        mysql.connection.commit()
        curr=mysql.connection.cursor()
        curr.execute("INSERT INTO dashes (email,items) VALUES (%s,%s)",(email,a,))
        mysql.connection.commit()
        session['name'] = request.form['name']
        session['email'] = request.form['email']
        return redirect(url_for('home'))
@app.route('/login',methods=["GET","POST"])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
 
        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM users WHERE email=%s",(email,))
        user = curl.fetchone()
        curl.close()
        if len(user) > 0:
            if bcrypt.hashpw(password, user["password"].encode('utf-8')) == user["password"].encode('utf-8'):
                session['name'] = user['name']
                session['email'] = user['email']
                return redirect(url_for('home'))
               
            else:
                return "Error password and email not match"
        else:
            return "Error user not found"
    else:
         return render_template("login.html")
          

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('homee'))












@app.route("/food")
def home():
    data=Display.query.all()
    return render_template('index.html',data=data)

@app.route("/south.html")
def home4():  
    return render_template('south.html')

@app.route("/about.html")
def home1():
    return render_template('about.html')


@app.route("/contact.html")
def home2():
    return render_template('contact.html')

@app.route("/addd",methods=["GET", "POST"])
def store():
     if request.method == 'POST':
        dish=request.form['item']
        sample=Dashes.query.filter_by(email=session['email']).first()
        a=sample.item
        print(a)
        a+=','
        a+=dish
        sample.item=a
        db.session.commit()
        samplee=[]
        s="gowathm"
        f=""
        for i in a:
            if(i==','):
                if(f!=s):
                    samplee.append(f)
                f=""
            else:
                f+=i
        
        energy=0
        protein=0
        cholestrol=0
        ca=0
        mg=0
        k=0
        iron=0
        zinc=0
        print(samplee)
        for i in samplee:
             post = Dishes.query.filter_by(name=i).first()
             ing=post.ingridients
             l2=[]
             d={}
             b=list(ing.split(","))
             for b1 in b:
                b1=b1.replace(" ",'%20')
                #print(b1)
                response_API = requests.get('https://api.edamam.com/api/nutrition-data?app_id=9fcaeeea&app_key=842290d81d5c6752f51a346f60bfe550&nutrition-type=cooking&ingr='+b1)
                data = response_API.text
                parse_json = json.loads(data)
                active_case = parse_json
                #print(active_case["totalNutrientsKCal"])
                l=[]
                l1=[]
                l.append(list(active_case["totalNutrients"].values()))
                l1.append(active_case["totalNutrients"].keys())
                #print(l)
                for i in l[0]:
                    if i['label'] not in list(d.keys()):
                        d[i['label']]=['a',0,0]
                for i in l[0]:
                    d[i['label']][0]=i['label']
                    d[i['label']][1]+=int(i['quantity'])
                    d[i['label']][2]=i['unit']
             l3=list(d.values())
             l2.append(l3)
             anss=l2[0]
             print(anss)
             count=0
             for user in anss:
                if(count==0):
                    energy+=user[1]
                elif(count==9):
                    protein+=user[1]
                elif(count==10):
                    cholestrol+=user[1]
                elif(count==12):
                    ca+=user[1]
                elif(count==13):
                    mg+=user[1]
                elif(count==14):
                    k+=user[1]
                elif(count==15):
                    iron+=user[1]
                elif(count==16):
                    zinc+=user[1]
                count+=1
        return render_template('items.html',energy=energy,protein=protein,cholestrol=cholestrol,ca=ca,mg=mg,k=k,iron=iron,zinc=zinc)

               
        

    





l2=[]
d={}
@app.route("/first/<string:post_slug>/", methods=['GET'])
def sep(post_slug):
    post = Dishes.query.filter_by(name=post_slug).first()
    ing=post.ingridients
    #name=request.args.get('value')
    #print(ing[name].split(","))
    b=list(ing.split(","))
    for b1 in b:
        b1=b1.replace(" ",'%20')
        #print(b1)
        response_API = requests.get('https://api.edamam.com/api/nutrition-data?app_id=9fcaeeea&app_key=842290d81d5c6752f51a346f60bfe550&nutrition-type=cooking&ingr='+b1)
        data = response_API.text
        parse_json = json.loads(data)
        active_case = parse_json
        #print(active_case["totalNutrientsKCal"])
        l=[]
        l1=[]
        l.append(list(active_case["totalNutrients"].values()))
        l1.append(active_case["totalNutrients"].keys())
        #print(l)
        for i in l[0]:
            if i['label'] not in list(d.keys()):
                d[i['label']]=['a',0,0]
        for i in l[0]:
            d[i['label']][0]=i['label']
            d[i['label']][1]+=int(i['quantity'])
            d[i['label']][2]=i['unit']

    l3=list(d.values())
        # for i in l:
        #     sn=[i['label'],i['quantity'],i['unit']]
        #     l2.append(sn)
        
    l2.append(l3)
    return render_template('sample.html',param=post_slug,anss=l2[0])
    

    