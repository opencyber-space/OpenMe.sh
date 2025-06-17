from flask import Flask, request, jsonify
import logging
import os

from .db import SessionMessageDatabase
from .schema import SessionMessage
from .handler import SessionManagementService, NatsPublisher
from .channels import ChannelsClient
from .expiry import ExpiryScheduler

app = Flask(__name__)
logger = logging.getLogger(__name__)

session_db = SessionMessageDatabase()
db = SessionMessageDatabase()
session_service = SessionManagementService(db=session_db, channels_client=ChannelsClient(
    os.getenv("CHANNELS_API_CLIENT")
), nats_publisher=NatsPublisher([os.getenv("ORG_NATS_URL")]))

expiry_scheduler = ExpiryScheduler(session_service, interval_seconds=300)
expiry_scheduler.start()


@app.route('/session', methods=['POST'])
def create_session_message():
    try:
        message_data = request.json
        message = SessionMessage.from_dict(message_data)
        success, result = session_db.insert(message)
        if success:
            return jsonify({"success": True, "data": {"message": "Session message created", "id": str(result)}}), 201
        else:
            return jsonify({"success": False, "error": result}), 400
    except Exception as e:
        logger.error(f"Error in create_session_message: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/session/<string:session_id>', methods=['GET'])
def get_session_message(session_id):
    try:
        success, result = session_db.get_by_session_id(session_id)
        if success:
            return jsonify({"success": True, "data": result.to_dict()}), 200
        else:
            return jsonify({"success": False, "error": result}), 404
    except Exception as e:
        logger.error(f"Error in get_session_message: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/session/<string:session_id>', methods=['PUT'])
def update_session_message(session_id):
    try:
        update_data = request.json
        success, result = session_db.update(session_id, update_data)
        if success:
            return jsonify({"success": True, "data": {"message": "Session message updated"}}), 200
        else:
            return jsonify({"success": False, "error": result}), 404
    except Exception as e:
        logger.error(f"Error in update_session_message: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/session/<string:session_id>', methods=['DELETE'])
def delete_session_message(session_id):
    try:
        success, result = session_db.delete(session_id)
        if success:
            return jsonify({"success": True, "data": {"message": "Session message deleted"}}), 200
        else:
            return jsonify({"success": False, "error": result}), 404
    except Exception as e:
        logger.error(f"Error in delete_session_message: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/sessions', methods=['POST'])
def query_session_messages():
    try:
        query_filter = request.json
        success, results = session_db.query(query_filter)
        if success:
            return jsonify({"success": True, "data": results}), 200
        else:
            return jsonify({"success": False, "error": results}), 400
    except Exception as e:
        logger.error(f"Error in query_session_messages: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/channels/response', methods=['POST'])
def channels_response():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON payload"}), 400

    session_id = data.get('session_id')
    response_data = data.get('response_data')

    if not session_id or response_data is None:
        return jsonify({"error": "Missing 'session_id' or 'response_data'"}), 400

    success, result = session_service.process_channel_response(
        session_id, response_data)
    if success:
        return jsonify({"status": "success", "data": result}), 200
    else:
        logger.error(
            f"Failed to process response for session {session_id}: {result}")
        return jsonify({"status": "error", "message": str(result)}), 500


@app.route('/webhook/validate_response', methods=['POST'])
def validate_response():

    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON payload"}), 400

    session_id = data.get("session_id")
    response_data = data.get("response_data")

    if not session_id or response_data is None:
        return jsonify({"error": "Missing 'session_id' or 'response_data'"}), 400

    success, session_or_error = db.get_by_session_id(session_id)
    if not success:
        logger.error(f"Session {session_id} not found: {session_or_error}")
        return jsonify({"error": f"Session not found: {session_or_error}"}), 404

    session = session_or_error

    temp_message_data = dict(session.message_data)
    temp_message_data.update(response_data)

    session.message_data = temp_message_data

    validation_result = session_service.validate_message(session)

    if validation_result.is_valid:
        return jsonify({"status": "valid", "errors": {}}), 200
    else:
        return jsonify({
            "status": "invalid",
            "errors": validation_result.errors
        }), 422

@app.route('/sessions/<session_id>/send_message', methods=['POST'])
def send_message(session_id):
    data = request.get_json()
    if not data or "channel_id" not in data or "message" not in data:
        return jsonify({"error": "Missing 'channel_id' or 'message'"}), 400

    success, result = session_service.send_message_to_channel(session_id, data["channel_id"], data["message"])
    if success:
        return jsonify({"status": "message_sent", "details": result}), 200
    else:
        return jsonify({"error": result}), 500


@app.route('/sessions/expire', methods=['POST'])
def expire_sessions():
    try:
        expiry_scheduler.expire_sessions()
        return jsonify({"status": "expiry_triggered"}), 200
    except Exception as e:
        logger.error(f"Expiry process failed: {e}")
        return jsonify({"error": str(e)}), 500

import atexit

@atexit.register
def shutdown_scheduler():
    expiry_scheduler.stop()

def run_server():
    app.run(host='0.0.0.0', port=8000)
