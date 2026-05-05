# Architect Skills

## System Design Principles
- **SOLID principles**: Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion.
- **DRY, KISS, YAGNI**: Avoid premature abstraction; solve the problem at hand.
- **Separation of Concerns**: Clearly defined layers (presentation, business logic, data access).
- **Dependency Injection**: Loose coupling via interfaces; testability through constructor injection.

## Architectural Patterns
- **Layered / N-Tier**: Clear separation between HTTP handlers, service layer, repository layer.
- **Hexagonal (Ports & Adapters)**: Business logic at the core; external dependencies behind interfaces.
- **Event-Driven**: Producers, consumers, event sourcing, CQRS (Command Query Responsibility Segregation).
- **Microservices**: Service decomposition strategies, inter-service communication (sync vs. async), service mesh.
- **Monolith-first**: When to start monolithic and how to extract services when boundaries become clear.

## Domain-Driven Design (DDD)
- Bounded contexts and context maps.
- Aggregates, entities, value objects, domain events.
- Repository pattern and unit of work.
- Anti-corruption layers when integrating legacy systems.

## Scalability & Reliability
- Horizontal vs. vertical scaling trade-offs.
- Stateless services and externalised state.
- Circuit breakers, bulkheads, retry with exponential backoff and jitter.
- Idempotency keys for at-most-once / at-least-once semantics.
- Data partitioning and sharding strategies.
- Read replicas and eventual consistency trade-offs.

## Security Architecture
- **Zero-Trust Networking**: Authenticate and authorise every service-to-service call.
- **Defence in Depth**: Multiple security layers so a single breach does not compromise the whole system.
- **Threat Modelling**: STRIDE analysis (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege).
- **Secrets Management**: Vault, AWS Secrets Manager, sealed Kubernetes secrets — never hardcoded credentials.
- **TLS Everywhere**: Enforce mTLS for internal service communication; TLS 1.3 for external traffic.

## API Gateway & Service Mesh
- API gateway responsibilities: auth, rate limiting, SSL termination, routing.
- Service mesh (Istio, Linkerd): mTLS, traffic management, observability.

## Database Architecture
- Choosing the right database for the access pattern (OLTP vs. OLAP, relational vs. document vs. graph).
- Multi-tenancy strategies: shared schema, separate schema, separate database.
- Migration strategies: zero-downtime schema changes, expand-contract pattern.
- Read/write splitting and query routing.

## Observability Architecture
- **Three Pillars**: Structured logs, distributed traces (OpenTelemetry), and metrics (Prometheus).
- **SLI/SLO Design**: Defining latency, availability, and error-rate SLOs before production launch.
- **Alerting Strategy**: Symptom-based alerts (high error rate) over cause-based alerts (CPU high).
- **Runbook Design**: Every alert links to a runbook with clear remediation steps.

## Decision-Making Frameworks
- **Architecture Decision Records (ADRs)**: Title, Status, Context, Decision, Consequences.
- **C4 Model**: Context, Container, Component, Code — choosing the right level of detail for the audience.
- **Trade-off Analysis**: Explicitly documenting what is gained and lost with each architectural choice.
- **Fitness Functions**: Automated checks that verify architectural constraints over time (e.g., no direct DB access from the API layer).
