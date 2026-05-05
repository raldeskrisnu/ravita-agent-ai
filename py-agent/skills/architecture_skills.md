# Architecture Skills

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
- Stateless services and externalized state.
- Circuit breakers, bulkheads, retry with exponential backoff and jitter.
- Idempotency keys for at-most-once / at-least-once semantics.
- Data partitioning and sharding strategies.
- Read replicas and eventual consistency trade-offs.

## API Gateway & Service Mesh
- API gateway responsibilities: auth, rate limiting, SSL termination, routing.
- Service mesh (Istio, Linkerd): mTLS, traffic management, observability.

## Caching Architecture
- Cache-aside vs. read-through vs. write-through.
- Cache invalidation strategies: TTL, event-based, versioned keys.
- Avoiding cache stampede with probabilistic early expiration or locking.

## Database Architecture
- Choosing the right database for the access pattern (OLTP vs. OLAP).
- Multi-tenancy: shared schema vs. separate schema vs. separate database.
- Migration strategies: zero-downtime schema changes, expand-contract pattern.
- Read/write splitting and query routing.

## Documentation & Communication
- Architecture Decision Records (ADRs) for significant choices.
- C4 model (Context, Container, Component, Code) diagrams.
- Runbooks and on-call documentation.
- Technical RFC process for cross-team changes.
