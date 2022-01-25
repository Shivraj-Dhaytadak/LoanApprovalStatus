
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
    "mongodb+srv://flaskloan:flaskloan@cluster0.ogg9d.mongodb.net/login?ssl=true&ssl_cert_reqs=CERT_NONE")
db = client.get_database('login')
records = db.user
Adminrecord = db.admin
LoanApplication = db.LoanApplication

# converting numerical data to ordinal
Profession = {'Technology_specialist': 1,
              'Petroleum_Engineer': 2,
              'Industrial_Engineer': 3,
              'Economist': 4,
              'Financial_Analyst': 5,
              'Design_Engineer': 6,
              'Web_designer': 7,
              'Designer': 8,
              'Dentist': 9,
              'Mechanical_engineer': 10,
              'Chemical_engineer': 11,
              'Politician': 12,
              'Librarian': 13,
              'Drafter': 14,
              'Graphic_Designer': 15,
              'Fashion_Designer': 16,
              'Surgeon': 17,
              'Statistician': 18,
              'Civil_servant': 19,
              'Engineer': 20,
              'Physician': 21,
              'Comedian': 22,
              'Magistrate': 23,
              'Analyst': 24,
              'Chef': 25,
              'Psychologist': 26,
              'Artist': 27,
              'Flight_attendant': 28,
              'Computer_operator': 29,
              'Microbiologist': 30,
              'Consultant': 31,
              'Biomedical_Engineer': 32,
              'Technician': 33,
              'Computer_hardware_engineer': 34,
              'Lawyer': 35,
              'Secretary': 36,
              'Architect': 37,
              'Technical_writer': 38,
              'Aviator': 39,
              'Hotel_Manager': 40,
              'Air_traffic_controller': 41,
              'Firefighter': 42,
              'Official': 43,
              'Civil_engineer': 44,
              'Geologist': 45,
              'Scientist': 46,
              'Software_Developer': 47,
              'Surveyor': 48,
              'Army_officer': 49,
              'Chartered_Accountant': 50,
              'Police_officer': 51}

CITY = {'Gandhinagar': 1,
        'Dehradun': 2,
        'Sultan_Pur_Majra': 3,
        'Bijapur': 4,
        'Bangalore': 5,
        'Rajpur_Sonarpur': 6,
        'Mira-Bhayandar': 7,
        'Mehsana': 8,
        'Latur': 9,
        'Belgaum': 10,
        'Berhampur': 11,
        'Bareilly': 12,
        'Gangtok': 13,
        'Panihati': 14,
        'Katni': 15,
        'Tadipatri': 16,
        'Hosur': 17,
        'Noida': 18,
        'Bhagalpur': 19,
        'Warangal[11][12]': 20,
        'Raichur': 21,
        'Ahmednagar': 22,
        'Orai': 23,
        'South_Dumdum': 24,
        'Kumbakonam': 25,
        'Khora,_Ghaziabad': 26,
        'Lucknow': 27,
        'Arrah': 28,
        'Karaikudi': 29,
        'Tiruvottiyur': 30,
        'Farrukhabad': 31,
        'Kozhikode': 32,
        'Amaravati': 33,
        'Eluru[25]': 34,
        'Amritsar': 35,
        'Malegaon': 36,
        'Tirunelveli': 37,
        'Amroha': 38,
        'Pimpri-Chinchwad': 39,
        'New_Delhi': 40,
        'Bhalswa_Jahangir_Pur': 41,
        'Bellary': 42,
        'Shimoga': 43,
        'Bally': 44,
        'Chinsurah': 45,
        'Sasaram[30]': 46,
        'Tiruppur': 47,
        'Thane': 48,
        'Karnal': 49,
        'Unnao': 50,
        'Vellore': 51,
        'Kishanganj[35]': 52,
        'Gulbarga': 53,
        'Shivpuri': 54,
        'Medininagar': 55,
        'Jodhpur': 56,
        'Khammam': 57,
        'Rohtak': 58,
        'Agra': 59,
        'Srikakulam': 60,
        'Kolkata': 61,
        'Tumkur': 62,
        'Muzaffarpur': 63,
        'Patiala': 64,
        'Anantapur': 65,
        'Anantapuram[24]': 66,
        'Karimnagar': 67,
        'Loni': 68,
        'Bhiwani': 69,
        'Jamnagar': 70,
        'Nellore[14][15]': 71,
        'Kalyan-Dombivli': 72,
        'Bathinda': 73,
        'Hapur': 74,
        'Naihati': 75,
        'Aurangabad[39]': 76,
        'Korba': 77,
        'Aurangabad': 78,
        'Akola': 79,
        'Bhimavaram': 80,
        'Pondicherry': 81,
        'Kolhapur': 82,
        'Durgapur': 83,
        'Ramgarh': 84,
        'Bihar_Sharif': 85,
        'Pudukkottai': 86,
        'Nandyal': 87,
        'Mau': 88,
        'Sangli-Miraj_&_Kupwad': 89,
        'Jalandhar': 90,
        'Chandigarh_city': 91,
        'Bikaner': 92,
        'Guntakal': 93,
        'Pune': 94,
        'Satara': 95,
        'Saharsa[29]': 96,
        'Jalgaon': 97,
        'Bharatpur': 98,
        'Dharmavaram': 99,
        'Ludhiana': 100,
        'Thanjavur': 101,
        'Bongaigaon': 102,
        'Surat': 103,
        'Fatehpur': 104,
        'Rampur': 105,
        'Madanapalle': 106,
        'Hindupur': 107,
        'Meerut': 108,
        'Erode[17]': 109,
        'Anand': 110,
        'Dibrugarh': 111,
        'Jammu[16]': 112,
        'Bulandshahr': 113,
        'Asansol': 114,
        'Bidar': 115,
        'Siliguri': 116,
        'Ballia': 117,
        'Gurgaon': 118,
        'Tenali': 119,
        'Ongole': 120,
        'Jamshedpur': 121,
        'Rourkela': 122,
        'Panchkula': 123,
        'Pallavaram': 124,
        'Adoni': 125,
        'Nadiad': 126,
        'Jalna': 127,
        'Hospet': 128,
        'Dhanbad': 129,
        'Haridwar': 130,
        'Mahbubnagar': 131,
        'Phagwara': 132,
        'Baranagar': 133,
        'Thoothukudi': 134,
        'Aizawl': 135,
        'Motihari[34]': 136,
        'Jamalpur[36]': 137,
        'Siwan[32]': 138,
        'Malda': 139,
        'Sirsa': 140,
        'Mangalore': 141,
        'Guwahati': 142,
        'Mirzapur': 143,
        'Rajkot': 144,
        'Uluberia': 145,
        'Chittoor[28]': 146,
        'Kharagpur': 147,
        'Singrauli': 148,
        'Bokaro': 149,
        'Machilipatnam': 150,
        'Vijayanagaram': 151,
        'Nashik': 152,
        'Silchar': 153,
        'Begusarai': 154,
        'Raebareli': 155,
        'Bhatpara': 156,
        'Sambalpur': 157,
        'Ambattur': 158,
        'Deoghar': 159,
        'Tiruchirappalli[10]': 160,
        'Ambarnath': 161,
        'Aligarh': 162,
        'Tirupati[21][22]': 163,
        'Proddatur': 164,
        'Madurai': 165,
        'Rewa': 166,
        'Solapur': 167,
        'Madhyamgram': 168,
        'Sagar': 169,
        'Parbhani': 170,
        'Kirari_Suleman_Nagar': 171,
        'Guna': 172,
        'Nagercoil': 173,
        'Vijayawada': 174,
        'Bhilwara': 175,
        'Secunderabad': 176,
        'Giridih': 177,
        'Kadapa[23]': 178,
        'Durg': 179,
        'Junagadh': 180,
        'Hajipur[31]': 181,
        'Vasai-Virar': 182,
        'Nanded': 183,
        'Kulti': 184,
        'Katihar': 185,
        'Serampore': 186,
        'Vadodara': 187,
        'Kanpur': 188,
        'Surendranagar_Dudhrej': 189,
        'Allahabad': 190,
        'Tadepalligudem': 191,
        'Coimbatore': 192,
        'Alappuzha': 193,
        'Kollam': 194,
        'Kurnool[18]': 195,
        'Alwar': 196,
        'Bilaspur': 197,
        'Thrissur': 198,
        'Gopalpur': 199,
        'Karawal_Nagar': 200,
        'Jorhat': 201,
        'Morbi': 202,
        'Chennai': 203,
        'Shimla': 204,
        'Patna': 205,
        'Navi_Mumbai': 206,
        'Firozabad': 207,
        'Mumbai': 208,
        'Bhopal': 209,
        'Darbhanga': 210,
        'Ajmer': 211,
        'Raurkela_Industrial_Township': 212,
        'Cuttack': 213,
        'Jhansi': 214,
        'Hubliâ€“Dharwad': 215,
        'Kota[6]': 216,
        'Tezpur': 217,
        'Chapra': 218,
        'Bhilai': 219,
        'Salem': 220,
        'Jaipur': 221,
        'Jaunpur': 222,
        'Bahraich': 223,
        'Faridabad': 224,
        'Ranchi': 225,
        'Saharanpur': 226,
        'Bhavnagar': 227,
        'Avadi': 228,
        'Panvel': 229,
        'Jabalpur': 230,
        'Visakhapatnam[4]': 231,
        'Yamunanagar': 232,
        'Morena': 233,
        'Ulhasnagar': 234,
        'Phusro': 235,
        'Burhanpur': 236,
        'Miryalaguda': 237,
        'Bhiwandi': 238,
        'Kakinada': 239,
        'Berhampore': 240,
        'Etawah': 241,
        'Gudivada': 242,
        'Ambala': 243,
        'Delhi_city': 244,
        'Narasaraopet': 245,
        'Nagaon': 246,
        'Hyderabad': 247,
        'Sonipat': 248,
        'Pali': 249,
        'Khandwa': 250,
        'Jehanabad[38]': 251,
        'Danapur': 252,
        'Dhule': 253,
        'Amravati': 254,
        'Ozhukarai': 255,
        'Dindigul': 256,
        'Suryapet': 257,
        'Ichalkaranji': 258,
        'Dehri[30]': 259,
        'Howrah': 260,
        'Rajahmundry[19][20]': 261,
        'Udupi': 262,
        'Maheshtala': 263,
        'Raipur': 264,
        'Agartala': 265,
        'Sambhal': 266,
        'Dewas': 267,
        'Nangloi_Jat': 268,
        'Gorakhpur': 269,
        'Bhusawal': 270,
        'Chandrapur': 271,
        'Gaya': 272,
        'Nizamabad': 273,
        'Ujjain': 274,
        'Nagpur': 275,
        'Haldia': 276,
        'Kamarhati': 277,
        'Panipat': 278,
        'Bidhannagar': 279,
        'Bhind': 280,
        'Varanasi': 281,
        'Tinsukia': 282,
        'North_Dumdum': 283,
        'Davanagere': 284,
        'Indore': 285,
        'Srinagar': 286,
        'Sri_Ganganagar': 287,
        'Shahjahanpur': 288,
        'Moradabad': 289,
        'Ratlam': 290,
        'Udaipur': 291,
        'Mango': 292,
        'Guntur[13]': 293,
        'Hazaribagh': 294,
        'Thiruvananthapuram': 295,
        'Mathura': 296,
        'Munger': 297,
        'Ahmedabad': 298,
        'Muzaffarnagar': 299,
        'Ramagundam[27]': 300,
        'Ghaziabad': 301,
        'Imphal': 302,
        'Gandhidham': 303,
        'Bardhaman': 304,
        'Mysore[7][8][9]': 305,
        'Kavali': 306,
        'Kottayam': 307,
        'Satna': 308,
        'Buxar[37]': 309,
        'Sikar': 310,
        'Barasat': 311,
        'Purnia[26]': 312,
        'Raiganj': 313,
        'Kochi': 314,
        'Bettiah[33]': 315,
        'Gwalior': 316,
        'Bhubaneswar': 317}
STATE = {'Sikkim': 1,
         'Uttarakhand': 2,
         'Punjab': 3,
         'Chandigarh': 4,
         'Karnataka': 5,
         'Tamil_Nadu': 6,
         'Delhi': 7,
         'Mizoram': 8,
         'Maharashtra': 9,
         'Andhra_Pradesh': 10,
         'Puducherry': 11,
         'Uttar_Pradesh': 12,
         'Gujarat': 13,
         'Haryana': 14,
         'West_Bengal': 15,
         'Telangana': 16,
         'Uttar_Pradesh[5]': 17,
         'Bihar': 18,
         'Assam': 19,
         'Himachal_Pradesh': 20,
         'Chhattisgarh': 21,
         'Jharkhand': 22,
         'Rajasthan': 23,
         'Odisha': 24,
         'Madhya_Pradesh': 25,
         'Jammu_and_Kashmir': 26,
         'Kerala': 27,
         'Tripura': 28,
         'Manipur': 29}
Married = {'Married': 0, 'Single': 1}
House = {'Neither Rented Nor Owned': 0, 'Owned': 1, 'rented': 2}
Car = {'no': 0, 'yes': 1}


def GetMarried(val):
    for key, value in Married.items():
        if int(val) == value:
            return key


def GetHouse(val):
    for key, value in House.items():
        if int(val) == value:
            return key


def GetCar(val):
    for key, value in Car.items():
        if int(val) == value:
            return key


def GetState(val):
    for key, value in STATE.items():
        if int(val) == value:
            return key


def GetCity(val):
    for key, value in CITY.items():
        if int(val) == value:
            return key


def GetProfession(val):
    for key, value in Profession.items():
        if int(val) == value:
            return key

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


@app.route('/loanapply', methods=['POST', 'GET'])
def loanapply():
    if "email" in session:
        email = session["email"]
        return render_template('LoanApply.html')


@app.route('/checkstatus', methods=['POST', 'GET'])
def checkstatus():
    if "email" in session:
        email = session["email"]
        email_found = LoanApplication.find_one({"Email": email})
        Loandetails = {
            "Fullname": email_found['Fullname'],
            "Email": email_found['Email'],
            "Income":  email_found['Income'],
            "LoanAmount": email_found['LoanAmount'],
            "Status": email_found['Status']
        }
        return render_template('checkstatus.html', Loan=Loandetails)


@app.route('/applyforloan', methods=['POST', 'GET'])
def predict():

    int_features = [request.form.get("Income"), request.form.get("age"), request.form.get("Experience"), request.form.get("Married/Single"), request.form.get("House_Ownership"), request.form.get(
        "Car_Ownership"), request.form.get("Profession"), request.form.get("City"), request.form.get("STATE"), request.form.get("Current_Job_yrs"), request.form.get("Current_House_yrs")]
    final_features = [np.array(int_features)]
    prediction = model.predict(final_features)
    output = round(prediction[0], 2)
    Marrital = GetMarried(request.form.get("Married/Single"))
    House = GetHouse(request.form.get("House_Ownership"))
    Car = GetCar(request.form.get("Car_Ownership"))
    Profession = GetProfession(request.form.get("Profession"))
    City = GetCity(request.form.get("City"))
    State = GetState(request.form.get("STATE"))
    if(output == 0):
        result = "Approved"
    else:
        result = "Rejected"
    ApplicationForCloud = {
        "Fullname": request.form.get("fullname"),
        "Email": request.form.get("email"),
        "LoanAmount": request.form.get("LoanAmount"),
        "Income": request.form.get("Income"),
        "Age": request.form.get("age"),
        "Experience": request.form.get("Experience"),
        "Married/Single": Marrital,
        "House_Ownership": House,
        "Car_Ownership": Car,
        "Profession": Profession,
        "City": City,
        "STATE": State,
        "Current_Job_yrs": request.form.get("Current_Job_yrs"),
        "Current_House_yrs": request.form.get("Current_House_yrs"),
        "Status": result
    }
    LoanApplication.insert_one(ApplicationForCloud)
    return render_template('LoanApply.html', prediction_text='Your Loan Appication is {}'.format(result))


@app.route("/userlogin", methods=["POST", "GET"])
def userlogin():
    message = 'Please login to your account'
    if "email" in session:
        return redirect(url_for("userDashboard"))

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
        email = request.form.get("admin[username]")
        password = request.form.get("admin[password]")
        admin_found = Adminrecord.find_one({"email": email})
        if admin_found:
            email_val = admin_found['email']
            passwordcheck = admin_found['password']

            if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
                session["email"] = email_val
                return render_template('adminDashboard.html')
            else:
                if "email" in session:
                    return render_template('adminDashboard.html')
                message = 'Wrong password'
                return render_template('adminlogin.html', message=message)


@app.route('/adminDashboard')
def adminDashboard():
    if "email" in session:
        email = session["email"]
        return render_template('adminDashboard.html', email=email)
    else:
        return redirect(url_for("adminLogin"))


if __name__ == "__main__":
    app.run(debug=True)
