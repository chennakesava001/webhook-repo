from flask import Flask

from app.webhook.routes import webhook_blueprint


# Creating our flask app
def create_app():

    app = Flask(__name__,template_folder='templates')
    
    # registering all the blueprints
    app.register_blueprint(webhook_blueprint)
    
    return app
