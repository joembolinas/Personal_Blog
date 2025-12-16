import os
from flask import Flask
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def create_app(test_config=None):
    """Application factory for the Personal Blog."""
    app = Flask(__name__, instance_relative_config=True, 
                template_folder=os.path.join(os.path.dirname(__file__), 'templates'),
                static_folder=os.path.join(os.path.dirname(__file__), 'static'))
    
    # Default configuration
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev-key-change-this-in-prod'),
    )

    if test_config:
        app.config.update(test_config)

    # Register blueprints (using relative imports now that we are a package)
    from .routes.guest import bp as guest_bp
    from .routes.admin import bp as admin_bp
    
    app.register_blueprint(guest_bp)
    app.register_blueprint(admin_bp)
    
    return app
