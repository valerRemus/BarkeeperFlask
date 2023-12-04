from flask import Flask, request, session
from flask_babel import Babel
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config
from recommender import CocktailRecommender



bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
babel = Babel()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

cocktailRecommender = CocktailRecommender(taxonomy_file='data/taxonomy_taste.csv',
                                          cocktail_file='data/ccc_cocktails.xml',
                                          general_taxonomy_file='data/general_taxonomy.csv')

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    babel.init_app(app)
    login_manager.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .bar import bar as bar_blueprint
    app.register_blueprint(bar_blueprint, url_prefix='/bar')

    from .messagess import messagess as messagess_blueprint
    app.register_blueprint(messagess_blueprint)


    return app

"""def create_recommender():
    recommender = CocktailRecommender(
        taxonomy_file='data/taxonomy_taste.csv',
        cocktail_file='data/ccc_cocktails.xml',
        general_taxonomy_file='data/general_taxonomy.csv',
        taxonomy_file_es='data/taxonomy_taste_spanish.csv',
        cocktail_file_es='data/ccc_cocktails_spanish.xml',
        general_taxonomy_file_es='data/general_taxonomy_spanish.csv'
    )
    return recommender
"""
@babel.localeselector
def get_locale():
    user_language = session.get('lang')
    if user_language in ['en', 'es']:
        return user_language
    return request.accept_languages.best_match(['en', 'es'])

"""
app.config['DEBUG_TB_ENABLED'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False  # Opcional, evita interferencias con redireccionamientos
toolbar = DebugToolbarExtension(app)
pip install flask-debugtoolbar
"""