# Developer Skills

## Languages & Runtimes
- **Go**: Idiomatic Go patterns, goroutines, channels, context propagation, error wrapping, interface design, generics (1.18+), profiling with pprof.
- **Python**: asyncio, type hints, dataclasses, virtual environments, packaging with poetry/uv/pip.
- **TypeScript / Node.js**: async/await, ESM vs CJS, type narrowing, tRPC, REST patterns.
- **SQL**: Complex queries, CTEs, window functions, query planning, index optimisation, schema migrations.

## API Design
- RESTful principles: resource naming, idempotency, status codes, versioning strategies.
- gRPC: protobuf schema design, service definitions, streaming, deadlines.
- GraphQL: schema-first design, resolvers, N+1 problem and DataLoader pattern.
- API security: authentication (JWT, OAuth2, API keys), authorisation (RBAC, ABAC), rate limiting.

## Data Storage
- **Relational**: PostgreSQL, MySQL – schema design, normalisation, transactions, connection pooling.
- **NoSQL**: Redis (data structures, pub/sub, Lua scripts), MongoDB (aggregation pipeline), DynamoDB (partition keys, GSI).
- **Message queues**: Kafka, RabbitMQ, NATS – producer/consumer patterns, at-least-once delivery, dead-letter queues.

## Observability
- Structured logging (JSON, log levels, correlation IDs).
- Metrics: Prometheus counters, histograms, gauges; Grafana dashboards.
- Tracing: OpenTelemetry, Jaeger, distributed trace propagation.
- Alerting: SLI/SLO definitions, error budgets, PagerDuty / OpsGenie integration.

## Infrastructure & DevOps
- Docker: multi-stage builds, layer caching, non-root users, health checks.
- Kubernetes: Deployments, Services, ConfigMaps, Secrets, HPA, resource limits, liveness/readiness probes.
- CI/CD: GitHub Actions, GitLab CI, ArgoCD – pipeline design, secrets management, rollback strategies.
- Infrastructure as Code: Terraform, Pulumi – state management, modules, remote backends.

## Security Fundamentals
- OWASP Top 10 awareness and mitigation.
- Input validation and sanitisation.
- Dependency scanning and vulnerability management.
- Secrets management: Vault, AWS Secrets Manager, environment-based injection.
- TLS configuration, certificate rotation, mutual TLS for internal services.

## Performance Engineering
- Profiling and benchmarking before optimising.
- Caching strategies: CDN, application-level, database query cache.
- Connection pooling and resource reuse.
- Batch processing vs. streaming trade-offs.
- Load testing with k6, Locust, or wrk.

## Debugging
- **Reproduce first**: Never attempt a fix without a reliable reproduction case.
- **Narrow the blast radius**: Isolate the smallest possible failing unit before diving into the full stack.
- Use `delve` (Go), `pdb`/`ipdb` (Python), or Node.js inspector for interactive debugging.
- Race detector: `go test -race ./...` to surface data races.
- `pprof` for CPU and heap profiling in Go.
- Systematic process: read the error, check recent changes, add logging, inspect state, bisect.

## Code Quality
- **Code Reviews**: Reviewing for correctness, security, readability, and testability.
- **Refactoring Patterns**: Extract Method, Introduce Parameter Object, Replace Conditional with Polymorphism.
- **Clean Code Principles**: Meaningful names, small functions, single responsibility, low coupling.
- **Static Analysis**: `go vet`, `staticcheck`, `ruff`, `mypy`, `eslint` — all integrated into CI.
