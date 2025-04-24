"""
Error handling routes
"""
from flask import render_template
import logging

# Configure logger
logger = logging.getLogger(__name__)

def register_error_handlers(app):
    """Register error handlers with the Flask app"""
    
    @app.errorhandler(404)
    def not_found_error(error):
        """Handle 404 errors"""
        logger.warning(f"404 error: {error}")
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors"""
        logger.error(f"500 error: {error}")
        return render_template('errors/500.html'), 500
    
    @app.errorhandler(403)
    def forbidden_error(error):
        """Handle 403 errors"""
        logger.warning(f"403 error: {error}")
        return render_template('errors/403.html'), 403
    
    @app.errorhandler(401)
    def unauthorized_error(error):
        """Handle 401 errors"""
        logger.warning(f"401 error: {error}")
        return render_template('errors/401.html'), 401 