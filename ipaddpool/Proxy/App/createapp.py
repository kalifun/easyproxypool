from flask import Flask
from Proxy.config.config import Config
from Proxy.model.models import db
from Proxy.apiblueprint.api import api
from Proxy.tools.todos import scheduler

def CreateApp():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.register_blueprint(blueprint=api)
    db.init_app(app=app)
    scheduler.init_app(app=app)
    scheduler.start()
    return app