import connexion
from flask_cors import CORS

app = connexion.FlaskApp(__name__, specification_dir='openapi/')
app.add_api('questionnaire-poc-be.yaml')
CORS(app.app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
