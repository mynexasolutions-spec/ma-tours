import os

from flask import Flask

from app.config import config
from app.extensions import db, migrate, login_manager


def create_app(config_name=None):
    """Application factory."""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Import models so Alembic can detect them
    from app import models  # noqa: F401

    # Register blueprints
    from app.auth import auth_bp
    app.register_blueprint(auth_bp)

    from app.admin import admin_bp
    app.register_blueprint(admin_bp)

    from app.public import public_bp
    app.register_blueprint(public_bp)

    # Register CLI commands
    register_commands(app)

    # Context processor for admin templates
    @app.context_processor
    def inject_admin_context():
        from flask_login import current_user
        if current_user.is_authenticated:
            from app.models.inquiry import Inquiry
            return {
                'new_inquiry_count': Inquiry.query.filter_by(status='new').count()
            }
        return {}

    # Auto-initialize and seed database if empty
    with app.app_context():
        try:
            db.create_all()
            from app.models.admin import Admin
            if not Admin.query.first():
                from seeds.seed_data import run_seeds
                run_seeds()
        except Exception as e:
            print(f"Error during auto-initialization: {e}")

    return app


def register_commands(app):
    """Register custom Flask CLI commands."""

    @app.cli.command('seed')
    def seed():
        """Seed the database with initial data."""
        from seeds.seed_data import run_seeds
        run_seeds()
