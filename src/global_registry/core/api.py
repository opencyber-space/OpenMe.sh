from flask import Flask, request, jsonify
import logging
from .crud import BackboneDataDatabase
from .schema import BackboneDataObject

app = Flask(__name__)
logger = logging.getLogger(__name__)

# Initialize the BackboneData database instance
backbone_db = BackboneDataDatabase()


@app.route('/backbone', methods=['POST'])
def create_backbone():
    try:
        data = request.json
        record = BackboneDataObject.from_dict(data)
        success, result = backbone_db.insert(record)
        if success:
            return jsonify({"success": True, "data": {"message": "BackboneData created", "id": str(result)}}), 201
        else:
            return jsonify({"success": False, "error": result}), 400
    except Exception as e:
        logger.error(f"Error in create_backbone: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/backbone/<string:system_id>', methods=['GET'])
def get_backbone(system_id):
    try:
        success, result = backbone_db.get_by_system_id(system_id)
        if success:
            return jsonify({"success": True, "data": result.to_dict()}), 200
        else:
            return jsonify({"success": False, "error": result}), 404
    except Exception as e:
        logger.error(f"Error in get_backbone: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/backbone/<string:system_id>', methods=['PUT'])
def update_backbone(system_id):
    try:
        update_data = request.json
        success, result = backbone_db.update(system_id, update_data)
        if success:
            return jsonify({"success": True, "data": {"message": "BackboneData updated"}}), 200
        else:
            return jsonify({"success": False, "error": result}), 404
    except Exception as e:
        logger.error(f"Error in update_backbone: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/backbone/<string:system_id>', methods=['DELETE'])
def delete_backbone(system_id):
    try:
        success, result = backbone_db.delete(system_id)
        if success:
            return jsonify({"success": True, "data": {"message": "BackboneData deleted"}}), 200
        else:
            return jsonify({"success": False, "error": result}), 404
    except Exception as e:
        logger.error(f"Error in delete_backbone: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/backbones', methods=['POST'])
def query_backbones():
    try:
        query_filter = request.json
        success, results = backbone_db.query(query_filter)
        if success:
            return jsonify({"success": True, "data": results}), 200
        else:
            return jsonify({"success": False, "error": results}), 400
    except Exception as e:
        logger.error(f"Error in query_backbones: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


def run_server():
    app.run(host='0.0.0.0', port=8000)
