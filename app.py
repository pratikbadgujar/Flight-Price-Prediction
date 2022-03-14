from flask import *
import pickle

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
        jrnyday = int(request.form['jrnyday'])
        jrnymnth = int(request.form['jrnymnth'])
        depthrs = int(request.form['depthrs'])
        deptmin = int(request.form['deptmin'])
        arvhrs = int(request.form['arvhrs'])
        arvmin = int(request.form['arvmin'])
        durhrs = abs(arvhrs - depthrs)
        durmin = abs(arvmin - deptmin)
        
        prediction = model.predict([[
            parlne,
            psrc,
            pdest,
            pstp,
            jrnyday,
            jrnymnth,
            depthrs,
            deptmin,
            arvhrs,
            arvmin,
            durhrs,
            durmin
        ]])
        
        output = round(prediction[0],2)
        
        return render_template('home.html',prediction_text="Your Flight Price is Rs {}".format(output))
    
    return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True)