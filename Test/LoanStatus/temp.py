from flask import Flask, render_template, request, url_for, redirect, session
import pymongo
import bcrypt
import pickle
import numpy as np
app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))
app.secret_key = "6042d70a-20c4-4049-a6dc-e9a244903532"
client = pymongo.MongoClient("mongodb+srv://flaskloan:flaskloan@cluster0.ogg9d.mongodb.net/login?ssl=true&ssl_cert_reqs=CERT_NONE")
db = client.get_database('login')
records = db.user
Adminrecord = db.admin

@app.route("/", methods=['post', 'get'])
def userLog():
    message = ''
    if "email" in session:
        return redirect(url_for("userDashboard"))
    if request.method == "POST":
        user = request.form.get("user[username]")
        email = request.form.get("user[email]")
        
        password1 = request.form.get("user[password]")
        password2 = request.form.get("user[cpassword]")
        user_found = records.find_one({"name": user})
        email_found = records.find_one({"email": email})
        if user_found:
            message = 'There already is a user by that name'
            return render_template('userLogin.html', message=message)
        if email_found:
            message = 'This email already exists in database'
            return render_template('userLogin.html', message=message)
        if password1 != password2:
            message = 'Passwords should match!'
            return render_template('userLogin.html', message=message)
        else:
            hashed = bcrypt.hashpw(password2.encode('utf-8'), bcrypt.gensalt())
            user_input = {'name': user, 'email': email, 'password': hashed}
            records.insert_one(user_input)
            
            user_data = records.find_one({"email": email})
            new_email = user_data['email']
   
            return render_template('userDashboard.html', email=new_email)
    return render_template('userLogin.html')


@app.route('/userDashboard')
def userDashboard():
    if "email" in session:
        email = session["email"]
        return render_template('userDashboard.html', email=email)
    else:
        return redirect(url_for("userLogin"))

@app.route('/loanapply')
def loanapply():
    if "email" in session:
        email = session["email"]
        return render_template('LoanApply.html')

@app.route('/applyforloan',methods=['POST','GET'])
def predict():

    int_features = [int(x) for x in request.form.values()]
    final_features = [np.array(int_features)]
    prediction = model.predict(final_features)

    output = round(prediction[0], 2)

    return render_template('LoanApply.html', prediction_text='PROBABILITY THAT YOUR LOAN WILL GET APPROVED IS ; {}'.format(output))


@app.route("/userlogin", methods=["POST", "GET"])
def userlogin():
    message = 'Please login to your account'
    if "email" in session:
        return redirect(url_for("userDashboard"))

    if request.method == "POST":
        email = request.form.get("user[email]")
        password = request.form.get("user[password]")

        admin_found = Adminrecord.find_one({"email":email})
        email_found = records.find_one({"email": email})
        if admin_found:
            return render_template('adminLogin.html')
        if email_found:
            email_val = email_found['email']
            passwordcheck = email_found['password']
            
            if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
                session["email"] = email_val
                return redirect(url_for('userDashboard'))
            else:
                if "email" in session:
                    return redirect(url_for("userDashboard"))
                message = 'Wrong password'
                return render_template('userLogin.html', message=message)
        else:
            message = 'Email not found'
            return render_template('userLogin.html', message=message)
    return render_template('userLogin.html', message=message)

@app.route("/logout", methods=["POST", "GET"])
def logout():
    if "email" in session:
        session.pop("email", None)
        return render_template("userLogin.html")
    else:
        return render_template('index.html')
      
if __name__ == "__main__":
    app.run(debug=True)