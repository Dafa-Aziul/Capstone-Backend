import os
import logging
from logging.handlers import RotatingFileHandler

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from sqlalchemy import text

from app.extensions import db, jwt, migrate

load_dotenv()


# Buat folder 'logs' jika belum ada
if not os.path.exists('logs'):
    os.makedirs('logs')

# Setup konfigurasi logger ke terminal dan file
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    handlers=[
        RotatingFileHandler('logs/app.log', maxBytes=5*1024*1024, backupCount=5),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def register_blueprints(app):
    from app.routes.root_routes import root_bp
    from app.routes.merek_routes import merek_bp
    from app.routes.model_kendaraan_routes import model_kendaraan_bp
    from app.routes.auth_routes import auth_bp
    from app.routes.ml_models_routes import ml_models_bp
    from app.routes.predict_routes import predict_bp
    from app.routes.user_routes import user_bp

    app.register_blueprint(root_bp)
    app.register_blueprint(merek_bp)
    app.register_blueprint(model_kendaraan_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(ml_models_bp)
    app.register_blueprint(predict_bp)
    app.register_blueprint(user_bp)


def log_database_connection(app):
    try:
        with app.app_context():
            db.session.execute(text("SELECT 1"))
        logger.info("Database connection successful.")
    except Exception as exc:
        logger.exception("Database connection failed: %s", exc)


def create_app(config_name=None):
    from app.config import config_by_name

    app = Flask(__name__)

    selected_config = config_name or os.getenv("FLASK_ENV", "development")
    app.config.from_object(config_by_name.get(selected_config, config_by_name["development"]))
    app.json.sort_keys = False

    CORS(app, supports_credentials=True, origins=app.config.get("CORS_ORIGINS"))

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    register_blueprints(app)
    log_database_connection(app)

    return app
