import click
from flask import current_app
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


def init_app(app):
    database.init_app(app)
    migrate.init_app(app, database)
    app.cli.add_command(init_database_command)


def init_database():
    with current_app.app_context():
        from flaskr.models import User, Post
        database.create_all()


@click.command('init-database')
def init_database_command():
    """Create tables if they don't exist."""
    init_database()
    click.echo('Initialized the database.')


database = SQLAlchemy(model_class=Base)
migrate = Migrate()
