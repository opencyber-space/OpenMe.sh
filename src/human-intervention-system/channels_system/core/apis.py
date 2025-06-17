from flask import Flask, request, jsonify
import logging
from .crud import ChannelStoreDatabase
from .schema import ChannelStoreObject
from .webhook_processor import ChannelMessenger
from .webhook_processor import ResponseProcessor

app = Flask(__name__)
logger = logging.getLogger(__name__)

channel_db = ChannelStoreDatabase()
messenger = ChannelMessenger()
response_processor = ResponseProcessor()

@app.route('/channel', methods=['POST'])
def create_channel():
    try:
        channel_data = request.json
        channel = ChannelStoreObject.from_dict(channel_data)
        success, result = channel_db.insert(channel)
        if success:
            return jsonify({"success": True, "data": {"message": "Channel created", "id": str(result)}}), 201
        else:
            return jsonify({"success": False, "error": result}), 400
    except Exception as e:
        logger.error(f"Error in create_channel: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/channel/<string:channel_id>', methods=['GET'])
def get_channel(channel_id):
    try:
        success, result = channel_db.get_by_channel_id(channel_id)
        if success:
            return jsonify({"success": True, "data": result.to_dict()}), 200
        else:
            return jsonify({"success": False, "error": result}), 404
    except Exception as e:
        logger.error(f"Error in get_channel: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/channel/<string:channel_id>', methods=['PUT'])
def update_channel(channel_id):
    try:
        update_data = request.json
        success, result = channel_db.update(channel_id, update_data)
        if success:
            return jsonify({"success": True, "data": {"message": "Channel updated"}}), 200
        else:
            return jsonify({"success": False, "error": result}), 404
    except Exception as e:
        logger.error(f"Error in update_channel: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/channel/<string:channel_id>', methods=['DELETE'])
def delete_channel(channel_id):
    try:
        success, result = channel_db.delete(channel_id)
        if success:
            return jsonify({"success": True, "data": {"message": "Channel deleted"}}), 200
        else:
            return jsonify({"success": False, "error": result}), 404
    except Exception as e:
        logger.error(f"Error in delete_channel: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/channels', methods=['POST'])
def query_channels():
    try:
        query_filter = request.json
        success, results = channel_db.query(query_filter)
        if success:
            return jsonify({"success": True, "data": results}), 200
        else:
            return jsonify({"success": False, "error": results}), 400
    except Exception as e:
        logger.error(f"Error in query_channels: {e}")
        return jsonify({"success": False, "error": str(e)}), 500



@app.route('/webhook-response', methods=['POST'])
def receive_webhook_response():
    try:
        data = request.json
        session_id = data.get('session_id')
        response_data = data.get('response_data')

        if not session_id or not response_data:
            return jsonify({"success": False, "error": "Missing session_id or response_data"}), 400

        # Forward to SESSIONS_SERVER
        success, result = response_processor.process(session_id, response_data)
        if success:
            return jsonify({"success": True, "message": "Response processed"}), 200
        else:
            return jsonify({"success": False, "error": result}), 500

    except Exception as e:
        logger.error(f"Error in receive_webhook_response: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/channel/message', methods=['POST'])
def send_channel_message():
    
    try:
        data = request.json
        required_fields = ["channel_id", "session_id", "message", "response_url"]

        for field in required_fields:
            if field not in data:
                return jsonify({"success": False, "error": f"Missing field: {field}"}), 400

        success, result = messenger.send_message_to_channel(
            channel_id=data["channel_id"],
            session_id=data["session_id"],
            message=data["message"],
            response_url=data["response_url"]
        )

        if success:
            return jsonify({"success": True, "data": result}), 200
        else:
            return jsonify({"success": False, "error": result}), 400

    except Exception as e:
        logger.error(f"Error in /channel/message: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

def run_server():
    app.run(host='0.0.0.0', port=8000)
