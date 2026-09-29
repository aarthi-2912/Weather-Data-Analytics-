<<<<<<< HEAD
#Weather Data Analytics

This is the third stage of the handwritten project flow:

OpenWeather -> CSV -> Supervised ML -> Random Forest -> Super_ML.joblib -> Browser

## What the ML model does

A `RandomForestRegressor` from scikit-learn is trained using `weather_data.csv`.

Input features:
- humidity
- pressure
- visibility
- wind speed
- cloudiness
- latitude
- longitude

Target:
- temperature_c

The model is saved as:

`Super_ML.joblib`

The Flask website then gets the current weather from OpenWeather and feeds the current input features into the trained model. The browser displays both:
- Actual current temperature from OpenWeather
- ML-predicted temperature from the Random Forest model

This is supervised learning because the CSV contains input features and a known target (`temperature_c`) used during training.

## Run

1. Put your valid OpenWeather API key in `.env`:

OPENWEATHER_API_KEY=YOUR_KEY
DEFAULT_CITY=Chennai

2. Install:

py -m pip install -r requirements.txt

3. If you replace or add data to `weather_data.csv`, retrain:

py Super_ML.py

This regenerates `Super_ML.joblib`.

4. Start the website:

py app.py

5. Open:

http://127.0.0.1:5000

## Important data note

The ZIP contains a small starter CSV so the ML model can run immediately for demonstration. For a stronger real-world model, keep collecting actual OpenWeather observations into the CSV and rerun `py Super_ML.py`.

Do not describe the starter rows as historical measurements if asked; describe them as starter/demo training data. For the real project dataset, collect observations through the OpenWeather API.

## Interview explanation

"First, I collect weather observations from the OpenWeather API and store them in a CSV dataset. Then I use supervised learning, where temperature is the target variable and humidity, pressure, wind speed, visibility, cloudiness and location are input features. I train a Random Forest Regressor using Scikit-learn and save the trained model as Super_ML.joblib. The Flask website fetches current weather and shows the actual OpenWeather temperature alongside the ML prediction."
=======
# Weather Data Analytics Using Machine Learning

## Project Overview
A web-based weather analytics application developed using Python and Flask. It fetches weather information using the OpenWeather API, stores weather records in a CSV dataset, and uses a Scikit-learn Random Forest machine learning model for weather data analysis and prediction.

## Features
- Fetch weather data from the OpenWeather API.
- View weather information through a Flask web application.
- Store weather records in a CSV file for analysis.
- Use a trained Random Forest model for machine learning predictions.
- Display results through a browser-based interface.

## Technologies Used
- Python
- Flask
- Scikit-learn
- Random Forest
- Pandas
- HTML
- OpenWeather API
- CSV

## Project Structure
- app.py – Flask application and backend logic.
- Super.ML – Saved machine learning model, if applicable.
- weather_data.csv – Weather dataset.
- templates/ – HTML templates for the web interface.
- requirements.txt – Python dependencies.

## How to Run
1. Clone this repository.
2. Install dependencies using `pip install -r requirements.txt`.
3. Set your OpenWeather API key as an environment variable named `OPENWEATHER_API_KEY`.
4. Run `python app.py`.
5. Open the local URL displayed in the terminal.

## Author
Aarthi R
>>>>>>> bf7f348dc2bdac74fbaf377cf0dd2c47b03d24db
