from flask import Flask, request, jsonify
import logging
import os
from .process import deploy_exchange, remove_exchange, update_exchange
from .db_client import BackboneDBClient

app = Flask(__name__)
logger = logging.getLogger(__name__)
db_client = BackboneDBClient(base_url=os.getenv("EXCHANGES_REGISTRY_DB"))


@app.route('/exchange', methods=['POST'])
def create_exchange():
    try:
        data = request.get_json()

        # Required fields
        kubeconfig = data['kubeconfig']
        helm_values = data['helm_values']
        release_name = data['release_name']
        org_ids = data['org_ids']
        cluster_id = data['cluster_id']
        name = data['name']

        # Optional fields
        namespace = data.get('namespace', 'communication')
        metadata = data.get('metadata', {})

        result = deploy_exchange(
            kubeconfig=kubeconfig,
            helm_values=helm_values,
            release_name=release_name,
            namespace=namespace,
            db_client=db_client,
            org_ids=org_ids,
            cluster_id=cluster_id,
            name=name,
            metadata=metadata
        )

        status = 201 if result.get("success") else 400
        return jsonify(result), status

    except Exception as e:
        logger.exception("Error in create_exchange")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/exchange/<string:system_id>', methods=['DELETE'])
def delete_exchange(system_id):
    try:
        data = request.get_json()

        kubeconfig = data['kubeconfig']
        release_name = data['release_name']
        namespace = data.get('namespace', 'communication')

        result = remove_exchange(
            kubeconfig=kubeconfig,
            release_name=release_name,
            namespace=namespace,
            db_client=db_client,
            system_id=system_id
        )

        status = 200 if result.get("success") else 400
        return jsonify(result), status

    except Exception as e:
        logger.exception("Error in delete_exchange")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/exchange/<string:system_id>', methods=['PUT'])
def update_exchange_api(system_id):
    try:
        data = request.get_json()

        kubeconfig = data['kubeconfig']
        release_name = data['release_name']
        helm_values = data['helm_values']
        namespace = data.get('namespace', 'communication')

        result = update_exchange(
            kubeconfig=kubeconfig,
            release_name=release_name,
            helm_values=helm_values,
            namespace=namespace
        )

        status = 200 if result.get("success") else 400
        return jsonify(result), status

    except Exception as e:
        logger.exception("Error in update_exchange")
        return jsonify({"success": False, "error": str(e)}), 500

def run():
    app.run(host='0.0.0.0', port=9000)
