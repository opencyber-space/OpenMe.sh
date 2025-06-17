from flask import Flask, jsonify, request
from .read_controller import ReadController

app = Flask(__name__)
read_controller = ReadController()

@app.route('/messages/<message_uuid>', methods=['GET'])
def get_message(message_uuid):
    message = read_controller.get_message_by_uuid(message_uuid)
    if message:
        return jsonify(message)
    return jsonify({'error': 'Message not found'}), 404

@app.route('/messages/subject/<subject_id>', methods=['GET'])
def get_messages_by_subject(subject_id):
    messages = read_controller.get_messages_by_subject(subject_id)
    return jsonify(messages)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
