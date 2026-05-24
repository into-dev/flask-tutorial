import os
from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI=f'sqlite:///{app.instance_path}/flaskr.sqlite'
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
    
    # ensure the instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)

    # a simple page that saya hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    
    from . import database
    database.init_app(app)

    from . import auth
    app.register_blueprint(auth.blueprint)

    from . import blog
    app.register_blueprint(blog.blueprint)
    app.add_url_rule('/', endpoint='index')

    return app
