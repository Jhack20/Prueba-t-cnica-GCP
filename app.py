from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

model = joblib.load("model.pkl")

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        try:
            data = request.get_json()
            if 'features' not in data:
                raise ValueError("No se proporcionaron características en los datos de entrada")
            features = np.array(data['features'])
            prediction = model.predict(features.reshape(1, -1))

            return jsonify({'prediction': prediction.tolist()})
        except ValueError as ve:
            return jsonify({'error': str(ve)}), 400  # respuesta HTTP 400 para datos
        except Exception as e:
            return jsonify({'error': str(e)}), 500  # respuesta HTTP 500 para errores internos

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
