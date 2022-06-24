from flask import Flask,render_template,request,url_for,redirect

from flaskext.mysql import MySQL


mysql=MySQL()
app = Flask(__name__)

app.config['MYSQL_DATABASE_USER']='admin'
app.config['MYSQL_DATABASE_PASSWORD']='12345678'
app.config['MYSQL_DATABASE_DB']='book_store'
app.config['MYSQL_DATABASE_HOST']='database-3.cujavq47oj5k.us-east-1.rds.amazonaws.com'
mysql.init_app(app)

username=""

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/register")
def registor():
    return render_template("form.html")

@app.route("/login")
def login():
    return render_template("form2.html")

@app.route('/login', methods=['POST'])
def Authenticate():
    username=request.form['mailid']
    password=request.form['pass']
    cursor=mysql.connect().cursor()
    cursor.execute("select * from Credentials where usernames='" + username + "' and passwords='" + password + "'")
    data=cursor.fetchone()
    if data is None:
        return "Username or Password is wrong"
    else:
        return redirect(url_for("bookdetails"))
    

@app.route("/register",methods=['POST'])
def adduser():
    fname=request.form['fname']
    lname=request.form['lname']
    email=request.form['mailid']
    passw=request.form['pass']
    ph=request.form['Pnmber']
    sname=request.form['sname']
    pcode=request.form['pcode']
    country=request.form['country']
    cursor=mysql.connect().cursor()
    sql = "INSERT INTO Customers (firstName, lastName, email, phoneNumber, streetName, postalCode, country) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = (fname,lname,email,ph,sname,pcode,country)
    cursor.execute(sql, val)
    mysql.connect().commit()
    cursor.close()
    if cursor.rowcount>1:
        return render_template("form2.html")
    else:
        return "fails"
      
@app.route('/profile')
def details():
    cursor=mysql.connect().cursor()
    cursor.execute("select * from Customers")
    res=cursor.fetchone()
    cursor.execute("select * from Orders")
    res1=cursor.fetchone()
    return render_template("userdetails.html",datas=res,datas1=res1)

@app.route('/books')
def bookdetails():
    cursor=mysql.connect().cursor()
    cursor.execute("select * from Books")
    bd=cursor.fetchall()
    return render_template("books.html",bdata=bd)
    

if __name__ == "__main__":
    app.run()
