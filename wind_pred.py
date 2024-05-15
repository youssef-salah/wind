from flask import Flask, request, jsonify, make_response
import joblib
import pandas as pd

app = Flask(__name__)
regr_energy = joblib.load('wind_prediction.joblib')

@app.route('/wind', methods=['POST', 'GET'])
def handle_data():
   try :

      if request.method == 'POST':
         jdata = request.json
         jdata_df = pd.DataFrame([jdata])
         
      elif request.method == 'GET':
   # Get parameters from query string
         params = ["wind_speed_m_s", "wind_direction_deg","pressure_atm"
                   ,"air_temperature_c" , "month"]
         jdata = {param : float (request.args.get(param , 0)) for param in params}
         jdata_df = pd.DataFrame([jdata])
# Create DataFrame with the received data
      
      predicted_wind_energy = regr_energy.predict(jdata_df)
      predicted_wind_energy = predicted_wind_energy.tolist()

# Create response with CORS headers
      response = make_response(jsonify({'predicted_wind_energy': predicted_wind_energy[0]}))
      response.headers['Access-Control-Allow-Origin'] = '*'
      response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
      response.headers['Access-Control-Allow-Methods'] = 'GET, POST'

      return response

   except Exception as e :
      response = make_response(jsonify({'error' : str(e)}), 400)

      return response

if __name__ == '__main__':
 app.run(debug=True, host='0.0.0.0', port=3000)



