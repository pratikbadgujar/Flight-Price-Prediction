from flask import *
import pickle
import pandas as pd

app = Flask(__name__)
model = pickle.load(open("flight_price.pkl", "rb"))
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/predict", methods = ["POST"])
def predict():
    if request.method == "POST":
        parlne= int(request.form['parlne'])
        psrc = int(request.form['psrc'])
        pdest = int(request.form['pdest'])
        pstp = int(request.form['pstp'])
        date_dep = request.form["Dep_Time"]
        
        # Journey day
        Journey_day = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").day)
        Journey_month = int(pd.to_datetime(date_dep, format ="%Y-%m-%dT%H:%M").month)
        # print("Journey Date : ",Journey_day, Journey_month)

        # Departure
        Dep_hour = int(pd.to_datetime(date_dep, format ="%Y-%m-%dT%H:%M").hour)
        Dep_min = int(pd.to_datetime(date_dep, format ="%Y-%m-%dT%H:%M").minute)
        # print("Departure : ",Dep_hour, Dep_min)

        # Arrival
        date_arr = request.form["Arrival_Time"]
        Arrival_hour = int(pd.to_datetime(date_arr, format ="%Y-%m-%dT%H:%M").hour)
        Arrival_min = int(pd.to_datetime(date_arr, format ="%Y-%m-%dT%H:%M").minute)
        # print("Arrival : ", Arrival_hour, Arrival_min)
        
         # Duration
        dur_hour = abs(Arrival_hour - Dep_hour)
        dur_min = abs(Arrival_min - Dep_min)
        
        prediction = model.predict([[
            parlne,
            psrc,
            pdest,
            pstp,
            Journey_day,
            Journey_month,
            Dep_hour,
            Dep_min,
            Arrival_hour,
            Arrival_min,
            dur_hour,
            dur_min
        ]])
        
        output = round(prediction[0],2)
        
        return render_template('home.html',prediction_text="Your Flight Price is Rs {}".format(output))
    
    return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True)