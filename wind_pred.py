from flask import Flask, request, jsonify, make_response
import joblib
import pandas as pd

app = Flask(__name__)
regr_energy = joblib.load('wind_prediction.joblib')

@app.route('/wind', methods=['POST', 'GET'])
def handle_data():
   if request.method == 'POST':
      jdata = request.json
   elif request.method == 'GET':
# Get parameters from query string
      wind_speed = float(request.args.get('wind_speed_m_s'))
      wind_direction = float(request.args.get('wind_direction_deg'))
      pressure = float(request.args.get('pressure_atm'))
      air_temperature = float(request.args.get('air_temperature_c'))
      month= int(request.args.get('Month'))


# Create DataFrame with the received data
      input_data = {
      "wind_speed_m_s": wind_speed,
      "pressure_atm": pressure,
      "wind_direction_deg": wind_direction,
      "air_temperature_c": air_temperature,
      "Month": month
      }
      input_df = pd.DataFrame([input_data])

      predicted_wind_energy = regr_energy.predict(input_df)
      predicted_wind_energy = predicted_wind_energy.tolist()

# Create response with CORS headers
      response = make_response(jsonify({'predicted_wind_energy': predicted_wind_energy[0]}))
      response.headers['Access-Control-Allow-Origin'] = '*'
      response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
      response.headers['Access-Control-Allow-Methods'] = 'GET, POST'

   return response

if __name__ == '__main__':
 app.run(debug=True, host='0.0.0.0', port=3000)



