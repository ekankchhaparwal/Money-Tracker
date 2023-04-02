from flask import Flask,render_template,request,redirect, url_for,session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt 
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)
app.config['SESSION_TYPE'] = 'memcached'
app.secret_key = "super secret key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///authorization.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app) 

class Authorization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30),  nullable=False)
    password = db.Column(db.String(30),  nullable=False) 
    totalExpense = db.Column(db.Integer)
    balance = db.Column(db.Integer)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30),  nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now().replace(microsecond=0)) 
    type = db.Column(db.String(3))

db.create_all()  

@app.route('/', methods =["GET", "POST"])
def loginAuth():
    if request.method == "POST":
       usernameAuth = str(request.form.get("username"))  
       session['username'] = usernameAuth
       passwordAuth = str(request.form.get("password"))
       data = Authorization.query.filter_by(username=usernameAuth).first()       
       if data is not None or check_password_hash(user.password, passwordAuth):
            allExpense = Expense.query.filter_by(username=usernameAuth).all()
            # return redirect(url_for('add_expense',usernameAuth,data.totalExpense,data.balance))
            user = usernameAuth
            return redirect(url_for('add_expense',user=user))
       else :
           error = "Invalid Credentials !"
           return redirect(url_for('errorLogin',error=error))
    return render_template('index.html')

@app.route('/<error>')
def errorLogin(error):
    return render_template('index.html',error=error)

@app.route('/')
def logOut():
    session.pop('username', None)
    return redirect('/')

@app.route('/add_expense/<user>', methods =["GET", "POST"])
def add_expense(user):
    if 'username' not in session:
        return redirect('/login')
    allE = Expense.query.filter_by(username=user).all()
    authData = Authorization.query.filter_by(username=user).first()
    if request.method == 'POST':
        username = request.form['username']
        amount = request.form['expense']
        category = request.form['category']
        expense = Expense(username=username,amount=amount,category=category,type="0")
        db.session.add(expense)
        auth = Authorization.query.filter_by(username=username).first()
        auth.totalExpense += float(amount)
        auth.balance -= float(amount) 
        db.session.commit() 
        return redirect(url_for('add_expense',user=username))
    
    return render_template('add_expense.html',username=user,allExpense=allE,totalExpense=authData.totalExpense,balance=authData.balance)

@app.route("/signUP",methods =["GET", "POST"])
def signUP(): 
    if request.method == "POST":
        uname = request.form['username']
        passw = request.form['password'] 
        data = Authorization.query.filter_by(username=uname).first()
        if data is not None:
            error = "Username already exists!"
            return render_template('signUp.html', error=error)
        auth = Authorization(username=uname, password=generate_password_hash(
                passw, method='sha256'),totalExpense=0,balance=0)
        db.session.add(auth)
        db.session.commit()  
        return redirect(url_for('loginAuth'))
    return render_template('signUP.html') 

@app.route('/delete/<int:id>')
def delete(id):
    
    expense = Expense.query.filter_by(id=id).first()
    username = expense.username
    auth = Authorization.query.filter_by(username=username).first()
    if(expense.type=="0"):
        auth.totalExpense -= float(expense.amount)
        auth.balance += float(expense.amount)
    else:
        auth.balance -= float(expense.amount)   
    db.session.delete(expense)
    db.session.commit()
    return redirect(url_for('add_expense',user=username))

@app.route('/update/<int:id>',methods =["GET", "POST"])
def update(id):
    expense = Expense.query.filter_by(id=id).first()
    username = expense.username
    auth = Authorization.query.filter_by(username=username).first()
    if(expense.type=="0"):
            auth.totalExpense -= expense.amount
            auth.balance += float(expense.amount)
    else:
            auth.balance -= float(expense.amount)
            
    if request.method=='POST':
        amount = request.form['amount']
        category = request.form['category']
        newAmount =  float(amount)
        if(expense.type=="0"):
            auth.totalExpense += newAmount
            auth.balance -= newAmount
        else:
            auth.balance += newAmount
        expense.amount = newAmount
        expense.category = category
        db.session.add(expense)
        db.session.commit()
        return redirect(url_for('add_expense',user=username))
    return render_template('update.html', expense=expense)

@app.route('/add_money',methods =["GET", "POST"])
def add_money():
    if request.method == "POST":
        username = request.form['user']
        money = request.form['money']
        category = request.form['Description']
        expense = Expense(username=username,amount=money,category=category,type="1")
        db.session.add(expense)

        auth = Authorization.query.filter_by(username=username).first()
        auth.balance += float(money)
        db.session.commit()  
        # return redirect(url_for('add_expense',user=username))  
        return redirect(request.referrer)    
    return render_template('add_expense.html',user="")

@app.route('/graph/<user>')
def graph(user):
    amounts = []
    categories = []
    allExpense = Expense.query.filter_by(username=user).all()
    for expense in allExpense:
        print(expense)
        if(expense.type=="0"):
            categories.append(expense.category)
            amounts.append(expense.amount)
    totals = {}
    for i in range(len(categories)):
        category = categories[i]
        amount = amounts[i]
        if category in totals:
            totals[category] += amount
        else:
            totals[category] = amount

    categories = list(totals.keys())
    amounts = list(totals.values())

    plt.style.use('seaborn')

    # Create the figure and axes objects
    fig, ax = plt.subplots(figsize=(6.4, 3.8))

    # Customize the plot
    color = ['#EF6C00', '#FFB900', '#43A047', '#039BE5', '#7B1FA2', '#F57C00', '#CDDC39', '#009688', '#8E24AA', '#673AB7']
    ax.bar(categories, amounts, color =color)
    ax.set_xlabel('Category', fontsize=13)
    ax.set_ylabel('Amount', fontsize=13)
    ax.tick_params(axis='both', labelsize=10)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    # Add text labels to the bars
    for i, amount in enumerate(amounts):
        ax.text(i, amount, u'\u20B9' + str(amount), ha='center', fontsize=10)

    # Add a title to the plot
    ax.set_title('Expense Chart', fontsize=16)

    # Save the chart to a PNG file
    fig.savefig('static/graph.png', dpi=200, bbox_inches='tight')
    return render_template('graph.html',user=user,categories=categories,amounts=amounts)

@app.route('/news/<user>')
def news(user):
    return render_template('finance_news.html',user=user)

@app.route('/business/<user>')
def business(user):
    return render_template('business_news.html',user=user)

@app.route('/back/<user>')
def back(user):
    return  redirect(url_for('add_expense',user=user)) 
if __name__ == '__main__': 
    app.run(debug=True,port =8000) 
