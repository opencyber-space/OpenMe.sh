import uuid
from urllib.parse import urlparse
from typing import Dict, Any
from .k8s import NATSDeployer
from .db_client import BackboneDBClient 

def _extract_public_host_from_kubeconfig(kubeconfig: Dict[str, Any]) -> str:
    
    try:
        server_url = kubeconfig['clusters'][0]['cluster']['server']
        parsed = urlparse(server_url)
        return parsed.hostname or "unknown-cluster"
    except Exception as e:
        raise ValueError(f"Failed to extract server hostname from kubeconfig: {e}")


def deploy_exchange(
    kubeconfig: Dict[str, Any],
    helm_values: Dict[str, Any],
    release_name: str,
    namespace: str,
    db_client: BackboneDBClient,
    org_ids: str,
    cluster_id: str,
    name: str,
    metadata: Dict[str, Any] = {}
) -> Dict[str, Any]:
   
    deployer = NATSDeployer(kubeconfig)
    success = deployer.deploy(release_name, helm_values, namespace=namespace)

    if not success:
        return {"success": False, "error": "Helm deployment failed"}

    # Form the public URL
    public_host = _extract_public_host_from_kubeconfig(kubeconfig)
    public_url = f"https://{public_host}/nats/{release_name}"

    # Create DB record
    system_id = str(uuid.uuid4())
    payload = {
        "system_id": system_id,
        "org_ids": org_ids,
        "cluster_id": cluster_id,
        "public_url": public_url,
        "metadata": metadata,
        "name": name
    }

    inserted, response = db_client.create_backbone(payload)
    if not inserted:
        # Rollback Helm deployment if DB insert fails
        deployer.uninstall(release_name, namespace)
        return {"success": False, "error": "DB insert failed", "detail": response}

    return {
        "success": True,
        "system_id": system_id,
        "release_name": release_name,
        "namespace": namespace,
        "public_url": public_url
    }


def remove_exchange(
    kubeconfig: Dict[str, Any],
    release_name: str,
    namespace: str,
    db_client: BackboneDBClient,
    system_id: str
) -> Dict[str, Any]:
    
    deployer = NATSDeployer(kubeconfig)
    uninstall_success = deployer.uninstall(release_name, namespace=namespace)

    if not uninstall_success:
        return {"success": False, "error": "Helm uninstall failed"}

    deleted, response = db_client.delete_backbone(system_id)
    if not deleted:
        return {"success": False, "error": "DB delete failed", "detail": response}

    return {"success": True, "message": f"Exchange '{release_name}' removed from cluster and DB"}


def update_exchange(
    kubeconfig: Dict[str, Any],
    release_name: str,
    helm_values: Dict[str, Any],
    namespace: str = "communication"
) -> Dict[str, Any]:
    
    deployer = NATSDeployer(kubeconfig)
    success = deployer.upgrade(release_name, helm_values, namespace)

    if success:
        return {
            "success": True,
            "message": f"Exchange '{release_name}' updated successfully"
        }
    else:
        return {
            "success": False,
            "error": f"Helm upgrade failed for release '{release_name}'"
        }
