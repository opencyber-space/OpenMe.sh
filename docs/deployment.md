# NATS Exchange Deployment

## 1. Introduction

This system allows teams to dynamically **deploy and manage NATS-based communication exchanges** across Kubernetes clusters in a federated environment. Each deployed NATS instance is:

* Installed using the official [nats/nats Helm chart](https://github.com/nats-io/k8s/tree/main/helm/charts/nats)
* Configured using a standard `values.yaml` (at `/app/values.yaml`) with overrides passed dynamically
* Deployed into a target cluster by passing its `kubeconfig` at runtime
* Registered in a **Backbone Registry** (MongoDB-backed or REST-exposed) for service discovery and metadata lookup

### Components Behind the Scenes:

| Component          | Description                                                   |
| ------------------ | ------------------------------------------------------------- |
| `NATSDeployer`     | Handles Helm-based deployment and deletion of NATS instances  |
| `BackboneDBClient` | REST client to create/delete records in the Backbone Registry |
| Flask API          | Exposes `/exchange` endpoints for deployment and teardown     |

---

## 2. REST API Documentation

### `POST /exchange`

Deploys a new NATS exchange on a remote Kubernetes cluster and registers it.

#### Request Body (JSON)

| Field          | Type   | Required                      | Description                                                           |
| -------------- | ------ | ----------------------------- | --------------------------------------------------------------------- |
| `kubeconfig`   | `Dict` | Yes                           | The kubeconfig of the target Kubernetes cluster                       |
| `helm_values`  | `Dict` | Yes                           | Key-value pairs for Helm overrides (e.g., enable JetStream, PVC size) |
| `release_name` | `str`  | Yes                           | Name for the Helm release                                             |
| `org_ids`      | `str`  | Yes                           | Organization IDs associated with the deployment                       |
| `cluster_id`   | `str`  | Yes                           | Logical ID representing the target cluster                            |
| `name`         | `str`  | Yes                           | Human-friendly name of the exchange                                   |
| `namespace`    | `str`  | No (default: `communication`) | Target namespace                                                      |
| `metadata`     | `Dict` | No                            | Optional metadata (team, region, tags)                                |

#### What Happens Internally

1. `NATSDeployer` creates a temporary kubeconfig and runs:

   ```bash
   helm upgrade --install <release_name> nats/nats -f /app/values.yaml --set key=value ...
   ```
2. It extracts the cluster's public IP from `kubeconfig.clusters[0].cluster.server`.
3. Constructs the `public_url` like:
   `https://<cluster-ip-or-dns>/nats/<release-name>`
4. Calls `BackboneDBClient.create_backbone()` to register the exchange.

#### Response

```json
{
  "success": true,
  "system_id": "uuid-generated",
  "release_name": "nats-ice-01",
  "namespace": "communication",
  "public_url": "https://34.68.99.13/nats/nats-ice-01"
}
```

---

### `DELETE /exchange/<system_id>`

Uninstalls a NATS release and removes its corresponding DB entry.

#### Request Body (JSON)

| Field          | Type   | Required | Description                                         |
| -------------- | ------ | -------- | --------------------------------------------------- |
| `kubeconfig`   | `Dict` | Yes      | Kubeconfig for the target cluster                   |
| `release_name` | `str`  | Yes      | Name of the Helm release to uninstall               |
| `namespace`    | `str`  | No       | Namespace of the release (default: `communication`) |

#### What Happens Internally

1. Calls:

   ```bash
   helm uninstall <release_name> --namespace <namespace>
   ```
2. Deletes the DB entry using `BackboneDBClient.delete_backbone(system_id)`

#### Response

```json
{
  "success": true,
  "message": "Exchange 'nats-ice-01' removed from cluster and DB"
}
```

---

## Helm Value Overrides

Your base values file lives at `/app/values.yaml`. You only pass specific overrides using the `helm_values` dict.

Example:

```json
{
  "config.jetstream.enabled": true,
  "config.jetstream.fileStore.pvc.size": "5Gi",
  "config.cluster.replicas": 3
}
```

---

## Example: Deploying via CURL

```bash
curl -X POST http://localhost:9000/exchange \
  -H "Content-Type: application/json" \
  -d '{
    "kubeconfig": { ... },
    "helm_values": {
      "config.jetstream.enabled": true,
      "config.jetstream.fileStore.pvc.size": "5Gi"
    },
    "release_name": "nats-global-exchange",
    "org_ids": "org001",
    "cluster_id": "us-east-cluster",
    "name": "Global Event Bus",
    "metadata": {"team": "infra"}
  }'
```

---

## Example: Removing via CURL

```bash
curl -X DELETE http://localhost:9000/exchange/89d4c61a-b35f-4fd0-8097-1aa58a77ec9f \
  -H "Content-Type: application/json" \
  -d '{
    "kubeconfig": { ... },
    "release_name": "nats-global-exchange"
  }'
```

---


Here is the **emoji-free version** of your Update Exchange API documentation:

---

### `PUT /exchange/<system_id>`

Updates an existing NATS exchange by performing a Helm upgrade with new override values.

#### Request Body (JSON)

| Field          | Type   | Required | Description                                                    |
| -------------- | ------ | -------- | -------------------------------------------------------------- |
| `kubeconfig`   | `Dict` | Yes      | Kubeconfig of the target Kubernetes cluster                    |
| `release_name` | `str`  | Yes      | Name of the Helm release to upgrade                            |
| `helm_values`  | `Dict` | Yes      | Dictionary of new override values to apply (via `--set`)       |
| `namespace`    | `str`  | No       | Kubernetes namespace of the release (default: `communication`) |

#### What Happens Internally

1. A temporary `kubeconfig` file is written.
2. `helm upgrade` is invoked with the release name and updated values:

   ```bash
   helm upgrade <release_name> nats/nats -f /app/values.yaml --set key=value ...
   ```
3. The existing release is updated in-place without touching the registry entry.

> **Note:** This API does not modify metadata in the BackboneDB. It only performs a Helm upgrade.

#### Response

**Success**

```json
{
  "success": true,
  "message": "Exchange 'nats-ice-01' updated successfully"
}
```

**Failure**

```json
{
  "success": false,
  "error": "Helm upgrade failed for release 'nats-ice-01'"
}
```

---

### Example Request

```bash
curl -X PUT http://localhost:9000/exchange/89d4c61a-b35f-4fd0-8097-1aa58a77ec9f \
  -H "Content-Type: application/json" \
  -d '{
    "kubeconfig": { ... },
    "release_name": "nats-ice-01",
    "helm_values": {
      "config.cluster.replicas": 5,
      "promExporter.enabled": true
    }
  }'
```

---

