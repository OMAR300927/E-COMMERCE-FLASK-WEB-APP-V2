from flask import Flask, redirect, url_for
import stripe


def create_app():
    
    app = Flask(__name__)
    app.config.from_object("myapp.config.Config")

    stripe.api_key = app.config["STRIPE_SECRET_KEY"]

    from .extension import db, migrate, jwt, cache, oauth
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cache.init_app(app, config={
    'CACHE_TYPE': 'RedisCache',
    'CACHE_REDIS_HOST': '127.0.0.1',
    'CACHE_REDIS_PORT': 6379
    })
    oauth.register(
        name='google',
        client_id=app.config['FLASK_CLIENT_ID'],
        client_secret=app.config['FLASK_CLIENT_SECRET'],
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={'scope': 'openid email profile'},
    )
    oauth.init_app(app)

    from .modules import jwt_callbacks

    from .modules import model

    from .Admin.routes import admin_bp
    app.register_blueprint(admin_bp)
    from .Users.routes import users_bp
    app.register_blueprint(users_bp)

    @app.route('/')
    def index():
        return redirect(url_for('users_bp.home'))
    

    return app