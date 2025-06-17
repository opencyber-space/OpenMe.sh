from flask import Flask, jsonify, request
from sqlalchemy.exc import SQLAlchemyError
from .writer import (
    add_topic_data, update_topic_data, add_messaging_config, update_messaging_config,
    add_global_config, update_global_config
)

from .get import (
    get_topics_data_by_subject_id, get_all_topics_data,
    get_messaging_config_by_topic_id, get_messaging_config_by_config_name,
    get_global_config_by_name, get_all_global_configs
)

from .db import db_session, init_db, shutdown_session

app = Flask(__name__)

# Initialize the database
@app.before_first_request
def setup():
    init_db()

# Teardown to close the session
@app.teardown_appcontext
def shutdown_session_on_teardown(exception=None):
    shutdown_session(exception)



@app.route('/topics_data', methods=['POST'])
def create_topic_data():
    data = request.json
    subject_id = data.get('subject_id')
    topic_ids = data.get('topic_ids')
    
    try:
        add_topic_data(subject_id, topic_ids)
        return jsonify({"message": "Topic data added successfully"}), 201
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/topics_data/<subject_id>', methods=['PUT'])
def update_topic_data_route(subject_id):
    data = request.json
    topic_ids = data.get('topic_ids')
    
    try:
        update_topic_data(subject_id, topic_ids)
        return jsonify({"message": "Topic data updated successfully"}), 200
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/topics_data/<subject_id>', methods=['GET'])
def get_topic_data(subject_id):
    try:
        topic_data = get_topics_data_by_subject_id(subject_id)
        if topic_data:
            return jsonify(topic_data.serialize()), 200
        else:
            return jsonify({"error": "Topic data not found"}), 404
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/topics_data', methods=['GET'])
def get_all_topics_data_route():
    try:
        topics_data = get_all_topics_data()
        return jsonify([t.serialize() for t in topics_data]), 200
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 400



@app.route('/messaging_config', methods=['POST'])
def create_messaging_config():
    data = request.json
    topic_id = data.get('topic_id')
    config_name = data.get('config_name')
    config_value = data.get('config_value')
    
    try:
        add_messaging_config(topic_id, config_name, config_value)
        return jsonify({"message": "Messaging config added successfully"}), 201
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/messaging_config/<topic_id>', methods=['PUT'])
def update_messaging_config_route(topic_id):
    data = request.json
    config_name = data.get('config_name')
    config_value = data.get('config_value')
    
    try:
        update_messaging_config(topic_id, config_name, config_value)
        return jsonify({"message": "Messaging config updated successfully"}), 200
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/messaging_config/<topic_id>', methods=['GET'])
def get_messaging_config_by_topic_id_route(topic_id):
    try:
        configs = get_messaging_config_by_topic_id(topic_id)
        if configs:
            return jsonify([c.serialize() for c in configs]), 200
        else:
            return jsonify({"error": "No configs found"}), 404
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/messaging_config/<topic_id>/<config_name>', methods=['GET'])
def get_messaging_config_by_name_route(topic_id, config_name):
    try:
        config = get_messaging_config_by_config_name(topic_id, config_name)
        if config:
            return jsonify(config.serialize()), 200
        else:
            return jsonify({"error": "Config not found"}), 404
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 400



@app.route('/global_config', methods=['POST'])
def create_global_config():
    data = request.json
    config_name = data.get('config_name')
    config_value = data.get('config_value')
    
    try:
        add_global_config(config_name, config_value)
        return jsonify({"message": "Global config added successfully"}), 201
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/global_config/<config_name>', methods=['PUT'])
def update_global_config_route(config_name):
    data = request.json
    config_value = data.get('config_value')
    
    try:
        update_global_config(config_name, config_value)
        return jsonify({"message": "Global config updated successfully"}), 200
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/global_config/<config_name>', methods=['GET'])
def get_global_config_by_name_route(config_name):
    try:
        config = get_global_config_by_name(config_name)
        if config:
            return jsonify(config.serialize()), 200
        else:
            return jsonify({"error": "Config not found"}), 404
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/global_config', methods=['GET'])
def get_all_global_configs_route():
    try:
        configs = get_all_global_configs()
        return jsonify([c.serialize() for c in configs]), 200
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 400

# Running the Flask App
if __name__ == '__main__':
    app.run(debug=True)
