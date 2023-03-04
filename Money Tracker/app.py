from flask import Flask,render_template,request,redirect, url_for
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///authorization.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Authorization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30),  nullable=False)
    password = db.Column(db.String(30),  nullable=False)
    
    def __repr__(self) -> str:
        return f"{self.id} -> {self.username} -> {self.password}"



@app.route('/', methods =["GET", "POST"])
def loginAuth():
    if request.method == "POST":
       usernameAuth = str(request.form.get("username"))
       passwordAuth = str(request.form.get("password"))
       print(usernameAuth)
       print(passwordAuth)
       data = Authorization.query.filter_by(username=usernameAuth, password=passwordAuth).first()
       if data is not None:
            return redirect(url_for('mainpage'))

    return render_template('index.html')

@app.route('/mainpage', methods =["GET", "POST"])
def mainpage():
    return render_template('mainpage.html')

@app.route("/signUP",methods =["GET", "POST"])
def signUP():
    if request.method == "POST":
        uname = request.form['username']
        passw = request.form['password']
        auth = Authorization(username=uname, password=passw)
        print(uname)
        print(passw)
        db.session.add(auth)
        db.session.commit()  
        return redirect(url_for('loginAuth'))
    
    return render_template('signUP.html')

if __name__ == '__main__': 
    app.run(debug=True,port =8000) 