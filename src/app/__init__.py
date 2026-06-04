import os
from flask import Flask
from config import get_config


def create_app(config_class=None):
    """
    Flask application factory.

    Initializes all extensions, registers all Blueprints, sets up Jinja2 filters,
    context processors, and error handlers.

    Returns:
        Flask: Configured Flask application instance.

    Note:
        Full initialization logic including currency formatting, barcode generation,
        feature flag injection, license checking, and notification context processors
        is proprietary and not included in this public version.
    """
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config.from_object(config_class or get_config())

    # Database connection management
    from .db import init_app as init_db
    init_db(app)

    # CSRF protection
    from flask_wtf.csrf import CSRFProtect
    CSRFProtect(app)

    # Tenant middleware
    from .middleware.tenant import init_tenant_middleware
    init_tenant_middleware(app)

    # Rate limiter
    from .limiter import limiter
    limiter.init_app(app)

    # Register all Blueprints
    _register_blueprints(app)

    # Error handlers, context processors, template filters
    _register_error_handlers(app)

    return app


def _register_blueprints(app: Flask):
    """Register all application Blueprints."""
    from .auth import bp as auth_bp
    from .dashboard import bp as dashboard_bp
    from .products import bp as products_bp
    from .customers import bp as customers_bp
    from .suppliers import bp as suppliers_bp
    from .sales import bp as sales_bp
    from .purchases import bp as purchases_bp
    from .returns import bp as returns_bp
    from .reports import bp as reports_bp
    from .employees import bp as employees_bp
    from .settings import bp as settings_bp
    from .expenses import bp as expenses_bp
    from .quotations import bp as quotations_bp
    from .profile import bp as profile_bp
    from .payment_methods import bp as payment_methods_bp
    from .purchase_orders import bp as purchase_orders_bp
    from .vouchers import bp as vouchers_bp
    from .production import bp as production_bp
    from .rebates import bp as rebates_bp
    from .audit import bp as audit_bp
    from .exports import bp as exports_bp
    from .shop_request import bp as shop_request_bp
    from .saas_admin import bp as saas_admin_bp
    from .offboard import bp as offboard_bp
    from .public import bp as public_bp
    from .ai_chat import bp as ai_chat_bp
    from .analytics import bp as analytics_bp
    from .mobile_api import bp as mobile_api_bp

    blueprints = [
        auth_bp, dashboard_bp, products_bp, customers_bp, suppliers_bp,
        sales_bp, purchases_bp, returns_bp, reports_bp, employees_bp,
        settings_bp, expenses_bp, quotations_bp, profile_bp, payment_methods_bp,
        purchase_orders_bp, vouchers_bp, production_bp, rebates_bp, audit_bp,
        exports_bp, shop_request_bp, saas_admin_bp, offboard_bp, public_bp,
        ai_chat_bp, analytics_bp,
    ]
    for bp in blueprints:
        app.register_blueprint(bp)

    app.register_blueprint(mobile_api_bp)
    # Mobile API does not use browser sessions; CSRF exemption required
    if 'csrf' in app.extensions:
        app.extensions['csrf'].exempt(mobile_api_bp)


def _register_error_handlers(app: Flask):
    """Register 404 and 500 error handlers."""
    from flask import render_template, jsonify, request

    def _wants_json():
        return (
            request.is_json
            or request.path.startswith('/api/')
            or request.headers.get('Accept', '').startswith('application/json')
        )

    @app.errorhandler(404)
    def not_found(e):
        if _wants_json():
            return jsonify({'error': 'Not found'}), 404
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def server_error(e):
        if _wants_json():
            return jsonify({'error': 'Internal server error'}), 500
        return render_template('errors/500.html'), 500

    @app.route('/health')
    def health():
        return jsonify({'status': 'ok'}), 200
