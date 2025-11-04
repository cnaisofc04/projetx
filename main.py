from app import app
import logging

logging.basicConfig(level=logging.DEBUG)

from routes.dashboard import dashboard_bp

app.register_blueprint(dashboard_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
