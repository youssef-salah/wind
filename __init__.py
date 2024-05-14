from flask import Flask, request, jsonify, make_response
import joblib
import pandas as pd

regr_energy = joblib.load('wind_prediction.joblib')

def create_app():
  """Creates a Flask application instance.

  Returns:
      Flask: A configured Flask application instance.
  """

  app = Flask(__name__)

  # Register blueprints (example)
  from .wind_pred import wind  # Assuming a routes.py file exists

  # Assuming wind.py contains the `handle_data` function and potentially other routes
  app.register_blueprint(wind)

  return app

# If the script is executed directly, run the development server
if __name__ == '__main__':
  app = create_app()
  app.run(debug=True, host='0.0.0.0', port=3000)
