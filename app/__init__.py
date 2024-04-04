from flask import Flask

from app.webhook.routes import my_webhook_blueprint


# Creating our flask app
def create_app():

    app = Flask(__name__,template_folder="template")
    
    # registering all the blueprints
    app.register_blueprint(my_webhook_blueprint)
    
    return app
