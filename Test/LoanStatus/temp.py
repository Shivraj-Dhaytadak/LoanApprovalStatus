from flask import Flask, render_template, request, url_for, redirect, session
import pymongo
import bcrypt
import pickle
import Converter
import numpy as np
app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

app.secret_key = "6042d70a-20c4-4049-a6dc-e9a244903532"

client = pymongo.MongoClient(
    "mongodb+srv://flaskloan:flaskloan@cluster0.ogg9d.mongodb.net/login?retryWrites=true&w=majority")
db = client.get_database('login')
records = db.user
Adminrecord = db.admin
LoanApplication = db.LoanApplication


@app.route("/", methods=['post', 'get'])
def userLog():
    message = ''
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
            session['Logged_in'] = email_found['email']
            message = 'Logged In As ' + new_email
            return render_template('userDashboard.html', email=new_email, message=message)
    return render_template('userLogin.html')


@app.route('/userDashboard')
def userDashboard():
    if "email" in session:
        email = session["email"]
        user_data = records.find_one({"email": email})
        if user_data['email'] == session["email"]:
            message = 'Logged In As ' + user_data['email']
            return render_template('userDashboard.html', email=email, message=message)
        else:
            return redirect(url_for("userLogin"))
    else:
        return redirect(url_for("userLogin"))


@app.route('/loanapply', methods=['POST', 'GET'])
def loanapply():
    if "email" in session:
        email = session["email"]
        email_found = list(LoanApplication.find({"Email": email}))
        if email_found:
            message = "Alert: Already Application exist Please Delete before Applying For New Application"
            return render_template('checkstatus.html', Loans=email_found, message=message)
        else:
            return render_template('LoanApply.html')
    return render_template('LoanApply.html')


@app.route('/checkstatus', methods=['POST', 'GET'])
def checkstatus():
    if "email" in session:
        email = session["email"]
        email_found = LoanApplication.find({"Email": email})
        if request.method == "POST":
            Delete_Application = LoanApplication.delete_one({"Email": email})
            return render_template('checkstatus.html', Loans=email_found)
        # Loandetails = {
        #     "Fullname": email_found['Fullname'],
        #     "Email": email_found['Email'],
        #     "Income":  email_found['Income'],
        #     "LoanAmount": email_found['LoanAmount'],
        #     "Status": email_found['Status']
        # }
    return render_template('checkstatus.html', Loans=email_found)


@app.route('/applyforloan', methods=['POST', 'GET'])
def predict():
    IncomeEntered = request.form.get("Income", type=int)
    AgeEntered = request.form.get("age", type=int)
    ExperinceEntered = request.form.get("Experience", type=int)
    MarritalEntered = request.form.get("Married/Single", type=int)
    HouseEntered = request.form.get("House_Ownership", type=int)
    CarEntered = request.form.get("Car_Ownership", type=int)
    ProEntered = request.form.get("Profession", type=int)
    CityEntered = request.form.get("City", type=int)
    StateEntered = request.form.get("STATE", type=int)
    CJYEntered = request.form.get("Current_Job_yrs", type=int)
    CHYEntered = request.form.get("Current_House_yrs", type=int)
    # int_features = [request.form.get("Income", type=int), request.form.get("age", type=int), request.form.get("Experience", type=int), request.form.get("Married/Single", type=int), request.form.get("House_Ownership", type=int), request.form.get(
    #     "Car_Ownership", type=int), request.form.get("Profession", type=int), request.form.get("City", type=int), request.form.get("STATE", type=int), request.form.get("Current_Job_yrs", type=int), request.form.get("Current_House_yrs", type=int)]

    # final_features = [np.array(int_features)]
    # print(final_features)
    prediction = model.predict([[IncomeEntered, AgeEntered, ExperinceEntered, MarritalEntered,
                               HouseEntered, CarEntered, ProEntered, CityEntered, StateEntered, CJYEntered, CHYEntered]])
    print(prediction)
    output = round(prediction[0], 2)
    print(output)
    Marrital = Converter.GetMarried(request.form.get("Married/Single"))
    House = Converter.GetHouse(request.form.get("House_Ownership"))
    Car = Converter.GetCar(request.form.get("Car_Ownership"))
    Profession = Converter.GetProfession(request.form.get("Profession"))
    City = Converter.GetCity(request.form.get("City"))
    State = Converter.GetState(request.form.get("STATE"))

    if(output == 0):
        result = "Approved"
    else:
        result = "Rejected"
    ApplicationForCloud = {
        "Fullname": request.form.get("fullname"),
        "Email": request.form.get("email"),
        "LoanAmount": request.form.get("LoanAmount", type=int),
        "Income": request.form.get("Income", type=int),
        "Age": request.form.get("age", type=int),
        "Experience": request.form.get("Experience", type=int),
        "Married/Single": Marrital,
        "House_Ownership": House,
        "Car_Ownership": Car,
        "Profession": Profession,
        "City": City,
        "STATE": State,
        "Current_Job_yrs": request.form.get("Current_Job_yrs", type=int),
        "Current_House_yrs": request.form.get("Current_House_yrs", type=int),
        "Status": result
    }
    LoanApplication.insert_one(ApplicationForCloud)
    return render_template('LoanApply.html', prediction_text='Your Loan Appication is {}'.format(result))


@app.route("/userlogin", methods=["POST", "GET"])
def userlogin():
    message = 'Please login to your account'
    if request.method == "POST":
        email = request.form.get("user[email]")
        password = request.form.get("user[password]")

        admin_found = Adminrecord.find_one({"email": email})
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
        return render_template('userLogin.html')


@app.route("/loadAdmin", methods=['POST'])
def loadAdmin():
    return render_template("adminLogin.html")


@app.route('/adminlogin', methods=['POST', 'GET'])
def adminlogin():
    if request.method == "POST":
        loanapp = LoanApplication.find()
        loanapps = list(loanapp)
        email = request.form.get("admin[username]")
        password = request.form.get("admin[password]")
        admin_found = Adminrecord.find_one({"email": email})
        if admin_found:
            email_val = admin_found['email']
            passwordcheck = admin_found['password']

            if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
                session["email"] = email_val
                return render_template('adminDashboard.html', loanapps=loanapps)
            else:
                if "email" in session:
                    return render_template('adminDashboard.html')
                message = 'Wrong password'
                return render_template('adminlogin.html', message=message)


@app.route('/adminDashboard', methods=['GET', 'POST'])
def adminDashboard():
    loanapp = LoanApplication.find()
    loanapps = list(loanapp)
    return render_template('adminDashboard.html', loanapps=loanapps)


@app.route('/applicationsearch', methods=['POST', 'GET'])
def applicationsearch():
    Loandetails1 = {}
    if request.method == "POST":
        email = request.form.get("email")
        session['searched'] = email
        email_found = list(LoanApplication.find({"Email": email}))
        return render_template('adminSearch.html', Loan=email_found)
    else:
        return render_template('adminSearch.html', Loan=Loandetails1)


@app.route('/applicationconfirm', methods=['POST', 'GET'])
def applicationconfirm():
    Loandetails1 = {}
    if request.method == 'POST':
        email = session['searched']
        LoanApplication.update_one(
            {"Email": email}, {"$set": {"Status": "Confirm"}}, upsert=False)
        email_found = list(LoanApplication.find({"Email": email}))
        return render_template('adminSearch.html', Loan=email_found)
    else:
        return render_template('adminSearch.html', Loan=Loandetails1)


@app.route('/applicationreject', methods=['POST', 'GET'])
def applicationreject():
    Loandetails1 = {}
    if request.method == 'POST':
        email = session['searched']
        LoanApplication.update_one(
            {"Email": email}, {"$set": {"Status": "Rejected By Bank Admin"}}, upsert=False)
        email_found = list(LoanApplication.find({"Email": email}))
        print(email_found)
        return render_template('adminSearch.html', Loan=email_found)
    else:
        return render_template('adminSearch.html', Loan=Loandetails1)


if __name__ == "__main__":
    app.run(debug=True)
