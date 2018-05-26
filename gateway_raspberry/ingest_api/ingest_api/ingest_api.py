"""
This program is heavily based on flask tutorial flaskr. 
http://flask.pocoo.org/docs/1.0/tutorial/
"""
import os
import sqlite3
from functools import wraps
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, jsonify
from jsonschema import validate, ValidationError

app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__) # load config from this file

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'ingest_api.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default',
    SAUNA_SCHEMA={
        "type": "object",
        "properties": {
            "temperature": {"type": "number"},
            "humidity": {"type": "number"},
            "mac_address": {"type": "string"}
        },
        "required": ["temperature", "humidity", "mac_address"]
    },
    BAJAMAJA_SCHEMA={
        "type": "object",
        "properties": {
            "US0_DIST": {"type": "number"},
            "US1_DIST": {"type": "number"},
            "US2_DIST": {"type": "number"}
        },
        "required": ["US0_DIST", "US1_DIST", "US2_DIST"]
    
    }
))
app.config.from_envvar('INGEST_API_SETTINGS', silent=True)

def validate_json(f):
    @wraps(f)
    def wrapper(*args, **kw):
        try:
            request.get_json(force=True)
        except TypeError:
            msg = "payload must be a valid json"
            return jsonify({"error": msg}), 400
        return f(*args, **kw)
    return wrapper

def validate_schema(schema_name):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kw):
            try:
                validate(request.get_json(), app.config[schema_name])
            except ValidationError as e:
                return jsonify({"error": e.message}), 400
            return f(*args, **kw)
        return wrapper
    return decorator

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/sauna', methods=['POST'])
@validate_json
@validate_schema('SAUNA_SCHEMA')
def add_sauna():
    db = get_db()
    data = request.get_json()
    db.execute('insert into sauna (temperature, humidity, mac_address) values (?, ?, ?)',
    [data['temperature'], data['humidity'], data['mac_address']])
    db.commit()
    return '', 204