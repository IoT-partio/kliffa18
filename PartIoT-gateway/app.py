"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""

from flask import Flask, jsonify, request, abort
from publish import init_connection, publish_temperature, cleanup

app = Flask(__name__)

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]

connection, channel = init_connection()


@app.route('/api/1/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

@app.route('/api/1/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)

    return jsonify({'task': task}), 201

@app.route('/api/1/temperature', methods=['POST'])
def digest_temperature():
    if not request.json or not 'temperature' in request.json or not 'id' in request.json:
        abort(400)

    temperature = request.json['temperature']
    id = request.json['id']

    if temperature < 10 or temperature > 100:
        abort(400)

    print("Starting to send message")
    publish_temperature(channel, temperature, id)

    return jsonify({'result':'success'}), 201

@app.route('/')
def hello():
    """Renders a sample page."""
    return "Hello World!"


if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
    print("Terminating app")
    cleanup(connection)

