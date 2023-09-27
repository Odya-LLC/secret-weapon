from flask import Flask, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_babel import Babel

db = SQLAlchemy()
babel = Babel()

def create_app():
    
    
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    
    def get_locale():
        if request.args.get('language'):
            session['language'] = request.args.get('language')
        return session.get('language', 'ru')
    
    babel.init_app(app,locale_selector=get_locale)
    
    @app.context_processor
    def inject_conf_var():
        return dict(AVAILABLE_LANGUAGES=app.config['LANGUAGES'], CURRENT_LANGUAGE=session.get('language', request.accept_languages.best_match(app.config['LANGUAGES'])))
    
    from app.bp import pages
    app.register_blueprint(pages, url_prefix='/')
    with app.app_context():
        db.create_all()
    return app
