import os

from flask import Flask, send_from_directory, send_file, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
app = Flask(__name__, static_folder='static/dist', static_url_path='')
app.secret_key = os.environ.get("SESSION_SECRET")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
db.init_app(app)

from routes.dashboard import dashboard_bp
from routes.academy import academy_bp
from routes.testing_dashboard import testing_bp

app.register_blueprint(dashboard_bp, url_prefix='/admin')
app.register_blueprint(academy_bp, url_prefix='/admin/academy')
app.register_blueprint(testing_bp, url_prefix='/admin/tests')

@app.route('/')
def serve_react_app():
    return send_file('static/dist/index.html')

@app.route('/assets/<path:path>')
def serve_assets(path):
    return send_from_directory('static/dist/assets', path)

@app.errorhandler(404)
def not_found(e):
    if not request.path.startswith('/api') and not request.path.startswith('/admin'):
        return send_file('static/dist/index.html')
    return {'error': 'Not found'}, 404

with app.app_context():
    import models
    db.create_all()