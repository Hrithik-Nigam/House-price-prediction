from flask import Flask, render_template, request
import pandas as pd
import pickle
from fastapi.middleware.cors import CORSMiddleware

app = Flask(__name__)
data = pd.read_csv('Cleaned Data.csv')
pipe = pickle.load(open("Model.pkl", 'rb'))


@app.route('/')
def index():
    locations = sorted(data['location'].unique())
    return render_template('index.html', locations=locations)


@app.route('/predict', methods=['POST', 'GET'])
def predict():
    if request.method == 'POST':
        location = request.form.get('location')
        bhk = request.form.get('BHK')
        bath = request.form.get('bath')
        sqft = request.form.get('sqft')
        bhk = float(bhk)
        bath = float(bath)
        sqft = float(sqft)

        inp = pd.DataFrame([[location, sqft, bath, bhk]], columns=['location', 'total_sqft', 'bath', 'bhk'])
        prediction = pipe.predict(inp)[0]
        prediction=float(prediction)
        prediction = "The price of a "+str(int(bhk))+"BHK house in the area of "+str(location)+ " is Rs. " +"{:.3f}".format(prediction) + ' lakhs.'

        return prediction


if __name__ == '__main__':
    app.run(debug=True, port=5000)
