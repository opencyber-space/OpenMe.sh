# 🌐 OpenMesh: Open Communication Mesh for AI

**OpenMesh** is a **decentralized, federated communication mesh** for large-scale, open **multi-agent systems (MAS)** such as the **Internet of Agents (IoA)** and the **Society of Agents (SoA)**.  

It provides **topic-routing, pub/sub eventing, per-agent inboxes, typed communication schemas, extensible communication protocols, membership and discovery, and a social-graph overlay** that supports higher-order interaction.  

OpenMesh is **operator-neutral**, **permissionless to join**, and **protocol-extensible**, enabling independent domains to federate while preserving local policy.

---

## Why OpenMesh?

In large-scale open MAS, **communication is the key substrate of intelligence**. Without expressive, reliable, and adaptive communication, agents remain isolated silos, unable to coordinate or form collective behaviors.  

OpenMesh addresses this by ensuring:

- **Coordination of Distributed Action**  
- **Negotiation and Social Contract Formation**  
- **State Sharing and Situation Awareness**  
- **Interoperability and Semantic Alignment**  
- **Emergence of Social Structures**

Unlike centralized, ad hoc, or application-specific systems, OpenMesh **combines resilience, semantic richness, and social awareness** into a single communication fabric.

---

## Core Principles & Features

- **Federated, Operator-Neutral Backbone**  
  Independent relay and directory nodes interoperate via open protocols, preventing lock-in and ensuring resilience.

- **Self-Describing, Schema-Linked Messages**  
  Messages embed schema URIs and semantic identifiers to **validate content, negotiate meaning, and evolve protocols without breakage**.

- **Extensible Protocol Semantics**  
  A minimal set of **performative verbs** (inform, request, propose, agree, etc.) forms a common language, while **protocol packages define richer workflows**

- **Policy-Aware by Design**  
  Enforces domain rules & constraints (access, rate limits, residency, compliance) without fragmenting the network.

- **Partition-Tolerant Survivability Layer**  
  Gossip membership, clustering, and multi-path routing maintain coordination during failures or adversarial conditions.

- **Multi-Pattern Communication Primitives**  
  Unified support for **pub/sub, request–reply, streaming, inbox/mailbox, gossip, shared state boards**, and **social-graph routing**.

- **Social-Graph Overlay**  
  Trust-weighted relationships and attention-routing enable **noise reduction, prioritization, and trust-based communication**.

- **Cross-Protocol Interoperability**  
  Bridges to **HTTP, MQTT, AMQP, Kafka, ROS2**, and others make OpenMesh a universal substrate.

---

## Communication Patterns

OpenMesh supports **multi-pattern communication** suited to different tasks and trust contexts:

- **Publish–Subscribe (Pub/Sub)** - Market data, telemetry, collective perception.  
- **Request–Reply** - Resource discovery, queries, contract negotiation.  
- **Streaming Channels** - Continuous feeds, real-time inference, simulation.  
- **Inbox/Mailbox** - Reliable delivery for offline/intermittent agents.  
- **Gossip & Epidemic Dissemination** - Membership, reputation, rapid alerts.  
- **Shared State Boards** - Collaborative state across agents.  
- **Social-Graph–Aware Routing** - Trust/role-weighted routing and filtering.  
- **Pattern Interoperability** - Composite workflows mixing multiple patterns.

---

## Semantic Layer & Schemas

OpenMesh ensures **meaning preservation** across heterogeneous agents through:

- **Self-Describing Messages**  
  Each message embeds schema URI, protocol URI, versioning, and security annotations.

- **Distributed Schema Registry**  
  Federated, content-addressable, and replicated across operators to avoid chokepoints. Stores **schemas, protocol definitions, compatibility rules**.

- **Protocol Definitions & State Machines**  
  Support for performative verbs and structured, auditable multi-step workflows that dictate the sequence, conditions, and branching logic of an interaction.

- **Schema & Protocol Negotiation / Translation**  
  On-demand protocol resolution via registries, negotiation, or translator agents. Prevents fragmentation into dialect “islands.”

- **Validation at Ingress & Egress**  
  Enforces schema compliance, protocol safety, and policy adherence for messages at every boundary.

- **Semantic Security**  
  Schema-bound ACLs, protocol enforcement, and type-level controls the meaning and permissible use of messages based on their declared structure, type, and protocol context.
---

## Signaling, Session Management & Routing

Signaling is the bridge between semantic intent and active communication 

- **Signaling Layer**  
	Used for meta-communication - exchanging information about how to communicate before any actual data is sent. 
  Handles **capability discovery, transport negotiation, security exchange, protocol alignment, and session contracts**.

- **Session Management**  
  Represents a logical communication channel between two or more agents. Establishes and tracks **ephemeral or persistent sessions**, monitors health, enforces policies, and supports graceful or forced termination.

- **Routing Layer**  
  Decides how messages traverse the mesh between agents, balancing performance, security, and compliance. Routing is Policy-aware, trust-sensitive, and adaptive:
  - Direct routing
  - Relay-based routing
  - Multi-path redundancy
  - Trust-weighted path selection
  - Policy-constrained routing (jurisdiction, compliance, SLAs)

- **Routing Metadata**  
  Encodes QoS, trust anchors, geo/policy constraints, and fallback orders.

---

## Example: Market Coordination Protocol

1. **Buyer publishes RFP** – `market/rfp@v1.0.0`  
2. **Seller responds with proposal** – `market/proposal@v1.0.0`  
3. **Negotiation** – Proposal protocol enforces valid transitions.  
4. **Contract finalization** – `market/contract@v2.0.1` with signatures and clauses.  
5. **Audit & Replay** – All interactions validated, versioned, logged for compliance.  

---


**A unified, scalable platform for managing and routing messages across distributed services and human interfaces.**  
Modular, policy-driven, and designed for modern cloud-native AI infrastructure.

🚧 **Project Status: Alpha**  
_Not production-ready. See [Project Status](#project-status-) for details._

---

## 📚 Contents 

* [Architecture](https://openmesh-internal.pages.dev/communication/architecture)
* [Deployment](https://openmesh-internal.pages.dev/communication/deployment)
* [Fanout](https://openmesh-internal.pages.dev/communication/fanout)
* [Registry](https://openmesh-internal.pages.dev/communication/registry)
* [Config](https://openmesh-internal.pages.dev/communication/config)
* [Logging](https://openmesh-internal.pages.dev/communication/logging)
* [Overview](https://openmesh-internal.pages.dev/communication/human-interface/architecture)
* [Channels](https://openmesh-internal.pages.dev/communication/human-interface/channels)
* [Chat Interface](https://openmesh-internal.pages.dev/communication/human-interface/chat)
* [Client SDK](https://openmesh-internal.pages.dev/communication/human-interface/client.md)
* [Sessions Management](https://openmesh-internal.pages.dev/communication/human-interface/sessions)
* [Interrupts Database](https://openmesh-internal.pages.dev/interrupts/interrupts_db)
* [Observe Trigger Library](https://openmesh-internal.pages.dev/interrupts/observe_trigger_lib)


---

## 🔗 Links

* 🌐 [Website](https://contracts-grid-internal.pages.dev/)
* 📄 [Vision Paper](https://resources.aigr.id/)
* 📚 [Documentation](https://openmesh-internal.pages.dev)
* 💻 [GitHub](https://github.com/opencyber-space/OpenMe.sh)

---

## 🏗 Architecture Diagrams

* 📡 [Communication Architecture](https://openmesh-internal.pages.dev/images/communication.png)
* ⚙ [Communication Configuration](https://openmesh-internal.pages.dev/images/communication-config.png)
* 🔀 [Communication Fanout](https://openmesh-internal.pages.dev/images/communication-fanout.png)
* 🗂 [Communication Logging / Queue](https://openmesh-internal.pages.dev/images/communication-queue.png)
* 🗄 [Communication Registry](https://openmesh-internal.pages.dev/images/communication-registry.png)
* 🧑‍💻 [Human Interface](https://openmesh-internal.pages.dev/images/communication-human-interface.png)
* 💬 [Chat System](https://openmesh-internal.pages.dev/images/communication-chat.png)

---

## 🌟 Highlights

### 🧱 Modular Communication Framework
- 📡 Multi-protocol message ingestion (HTTP, WebSocket, Redis, NATS)
- ⚙️ Configurable message routing and policy enforcement
- 💾 Persistent message logging with queryable storage (TimescaleDB)
- 🔄 Real-time message streaming via WebSockets

### 🧠 Intelligent Registry Layer
- 🗂️ Dynamic discovery of communication backbones (ICEs)
- 🌐 Management of deployed systems across multi-cluster networks
- 🩺 Health-aware routing using registry metadata
- 🛡️ Constraint checking for secure and compliant communication

### 🔍 Seamless Observability & Control
- 🔑 Centralized configuration management for topics and systems
- 🧾 Structured queries by message UUID or subject ID
- 🕸️ Comprehensive REST APIs for management and access
- 🛠️ Pluggable human intervention workflows for AI systems
- 🛡️ Dynamic data validation with customizable templates and webhook notifications[1]

---

## 📦 Use Cases

| Use Case                        | What It Solves                                                                      |
| ------------------------------- | ----------------------------------------------------------------------------------- |
| **Multi-Agent Communication**   | Reliable message exchange between autonomous services in federated environments         |
| **AI Orchestration**            | Configurable routing and policy enforcement for complex AI workflows                   |
| **Human-in-the-Loop Systems**   | Structured communication between automation and human participants                     |
| **Audit Logging & Compliance**  | Persistent storage and queryable access to all message exchanges                     |
| **Real-Time Monitoring**        | Live introspection into communication streams for debugging and performance analysis |
| **Dynamic Data Validation**    | Ensuring data integrity and consistency across all communication channels[1]         |

---

## 🧩 Integrations

| Component           | Purpose                                                     |
| ------------------- | ----------------------------------------------------------- |
| **NATS**            | Core messaging backbone for message distribution              |
| **Redis**           | Ingestion buffering, caching, and pub/sub                     |
| **TimescaleDB**     | Persistent storage for message logs                         |
| **Flask**           | REST API and WebSocket server implementation                |
| **SQLAlchemy**      | Database interaction layer                                  |
| **Kubernetes**      | Dynamic deployment and management of communication backbones |
| **Webhook System**   | Real-time notifications on data validation events[1]          |

---

## 💡 Why Use This?

| Problem                                         | Our Solution                                                        |
| ----------------------------------------------- | ------------------------------------------------------------------- |
| 🔹 Inconsistent communication protocols          | Multi-protocol ingestion with unified message format                |
| 🔹 Lack of traceability in distributed systems   | Persistent logging with queryable storage                           |
| 🔹 Difficulty managing communication infrastructure | Dynamic deployment and registry-based discovery                       |
| 🔹 Security and compliance concerns              | Policy enforcement via constraint checking                          |
| 🔹 Difficulty integrating human feedback       | Structured session management and channel abstraction                |
| 🔹 Data corruption or inconsistency           | Dynamic data validation with customizable templates[1]                |

---

# Project Status 🚧

> ⚠️ **Development Status**  
> The project is nearing full completion of version 1.0.0, with minor updates & optimization still being delivered.
> 
> ⚠️ **Alpha Release**  
> Early access version. Use for testing only. Breaking changes may occur.  
>
> 🧪 **Testing Phase**  
> Features are under active validation. Expect occasional issues and ongoing refinements.  
>
> ⛔ **Not Production-Ready**  
> We do not recommend using this in production (or relying on it) right now. 
> 
> 🔄 **Compatibility**  
> APIs, schemas, and configuration may change without notice.  
>
> 💬 **Feedback Welcome**  
> Early feedback helps us stabilize future releases.  


---

## 📢 Communications

1. 📧 Email: [community@opencyberspace.org](mailto:community@opencyberspace.org)  
2. 💬 Discord: [OpenCyberspace](https://discord.gg/W24vZFNB)  
3. 🐦 X (Twitter): [@opencyberspace](https://x.com/opencyberspace)

---

## 🤝 Join Us!

This project is **community-driven**. Theory, Protocol, implementations - All contributions are welcome.

### Get Involved

- 💬 [Join our Discord](https://discord.gg/W24vZFNB)  
- 📧 Email us: [community@opencyberspace.org](mailto:community@opencyberspace.org)

