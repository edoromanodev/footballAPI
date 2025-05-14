from flask import Flask, jsonify
from flask_cors import CORS
from flasgger import Swagger
from werkzeug.exceptions import HTTPException

def create_app():
    app = Flask(
        __name__,
        static_url_path='/static',
        static_folder='static'
    )

    # --- SWAGGER CONFIGURATION ---
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec_1',
                "route": '/apispec_1.json',
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/static",
        "swagger_ui": True,
        "specs_route": "/apidocs/"
    }

    swagger_template = {
        "info": {
            "title": "Football API",
            "description": "REST API to fetch European Football data (web scraping)",
            "version": "1.0.0",
            "termsOfService": "https://yourdomain.com/terms",
            "contact": {
                "name": "Edoardo Romano",
                "url": "https://yourdomain.com/contact",
                "email": "edoromano04@icloud.com",
            },
            "license": {
                "name": "MIT",
                "url": "https://opensource.org/licenses/MIT",
            }
        },
        "host": "localhost:5000",
        "basePath": "/",
        "schemes": ["http"]
    }

    Swagger(app, config=swagger_config, template=swagger_template)

    # --- ERROR HANDLING ---

    # Handle HTTP errors (e.g. 404, 400, 405) as JSON
    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        response = {
            "success": False,
            "error": {
                "code": e.code,
                "name": e.name,
                "description": e.description
            }
        }
        return jsonify(response), e.code

    # Handle generic uncaught exceptions as JSON
    @app.errorhandler(Exception)
    def handle_exception(e):
        response = {
            "success": False,
            "error": {
                "code": 500,
                "name": "Internal Server Error",
                "description": "An unexpected error occurred. Please contact support."
            }
        }
        return jsonify(response), 500

    # Example: custom error for input validation (extend as needed)
    class InputValidationError(Exception):
        def __init__(self, message):
            self.message = message

    @app.errorhandler(InputValidationError)
    def handle_input_validation_error(e):
        response = {
            "success": False,
            "error": {
                "code": 400,
                "name": "Bad Request",
                "description": e.message
            }
        }
        return jsonify(response), 400

    # --- BLUEPRINT REGISTRATION ---
    from app.routes import bp
    app.register_blueprint(bp, url_prefix='/api')

    CORS(app) 

    return app
