from flask import Flask, request, jsonify
import logging
from werkzeug.utils import secure_filename
from .chat_assets import ChatAssetUploader
from .sessions import ChatSession, ChatSessionDatabase, ChatMessagesDatabase

app = Flask(__name__)
logger = logging.getLogger(__name__)
chat_session_db = ChatSessionDatabase()
chat_db = ChatMessagesDatabase()


@app.route('/chat/session', methods=['POST'])
def create_chat_session():
    try:
        session_data = request.json
        session = ChatSession.from_dict(session_data)
        success, result = chat_session_db.insert(session)
        if success:
            return jsonify({"success": True, "data": {"message": "Chat session created", "id": str(result)}}), 201
        else:
            return jsonify({"success": False, "error": result}), 400
    except Exception as e:
        logger.error(f"Error in create_chat_session: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/chat/session/<string:session_id>', methods=['GET'])
def get_chat_session(session_id):
    try:
        success, result = chat_session_db.get_by_session_id(session_id)
        if success:
            return jsonify({"success": True, "data": result.to_dict()}), 200
        else:
            return jsonify({"success": False, "error": result}), 404
    except Exception as e:
        logger.error(f"Error in get_chat_session: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/chat/session/<string:session_id>', methods=['PUT'])
def update_chat_session(session_id):
    try:
        update_data = request.json
        success, result = chat_session_db.update(session_id, update_data)
        if success:
            return jsonify({"success": True, "data": {"message": "Chat session updated"}}), 200
        else:
            return jsonify({"success": False, "error": result}), 404
    except Exception as e:
        logger.error(f"Error in update_chat_session: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/chat/session/<string:session_id>', methods=['DELETE'])
def delete_chat_session(session_id):
    try:
        success, result = chat_session_db.delete(session_id)
        if success:
            return jsonify({"success": True, "data": {"message": "Chat session deleted"}}), 200
        else:
            return jsonify({"success": False, "error": result}), 404
    except Exception as e:
        logger.error(f"Error in delete_chat_session: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/chat/session/query', methods=['POST'])
def query_chat_sessions():
    try:
        query_filter = request.json or {}
        success, result = chat_session_db.query(query_filter)
        if success:
            return jsonify({"success": True, "data": result}), 200
        else:
            return jsonify({"success": False, "error": result}), 400
    except Exception as e:
        logger.error(f"Error in query_chat_sessions: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/chat/session/<string:session_id>/upload', methods=['POST'])
def upload_chat_file(session_id):
    try:

        uploader = ChatAssetUploader()
        if 'file' not in request.files:
            return jsonify({"success": False, "error": "Missing file part"}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({"success": False, "error": "No selected file"}), 400

        filename = secure_filename(file.filename)
        file_bytes = file.read()
        content_type = file.content_type or "application/octet-stream"

        success, result = uploader.upload_file(file_bytes, session_id, content_type)

        if success:
            return jsonify({
                "success": True,
                "data": {
                    "message": "File uploaded successfully",
                    "file_path": result,
                    "original_filename": filename
                }
            }), 200
        else:
            return jsonify({"success": False, "error": result}), 500

    except Exception as e:
        logger.error(f"Error in upload_chat_file: {e}")
        return jsonify({"success": False, "error": str(e)}), 500




@app.route('/chat/message/session/<string:session_id>', methods=['GET'])
def query_messages_by_session(session_id):
    try:
        success, result = chat_db.query_by_session(session_id)
        if success:
            return jsonify({"success": True, "data": result}), 200
        else:
            return jsonify({"success": False, "error": result}), 404
    except Exception as e:
        logger.error(f"Error in query_messages_by_session: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/chat/message/<string:chat_id>', methods=['GET'])
def get_message_by_chat_id(chat_id):
    try:
        success, result = chat_db.get_by_chat_id(chat_id)
        if success:
            return jsonify({"success": True, "data": result.to_dict()}), 200
        else:
            return jsonify({"success": False, "error": result}), 404
    except Exception as e:
        logger.error(f"Error in get_message_by_chat_id: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/chat/message/<string:chat_id>', methods=['DELETE'])
def delete_message_by_chat_id(chat_id):
    try:
        success, result = chat_db.delete_by_chat_id(chat_id)
        if success:
            return jsonify({"success": True, "data": {"message": "Message deleted"}}), 200
        else:
            return jsonify({"success": False, "error": result}), 404
    except Exception as e:
        logger.error(f"Error in delete_message_by_chat_id: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

def run_server():
    app.run(host='0.0.0.0', port=7000)