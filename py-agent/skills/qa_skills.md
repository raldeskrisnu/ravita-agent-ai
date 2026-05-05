# QA Skills

## Testing Philosophy
- **Tests are living documentation**: A good test describes the intended behaviour of the system, not just its current implementation.
- **Test behaviour, not implementation**: Tests should survive refactoring. Avoid testing private functions; test the public contract.
- **Fast feedback loops**: Prioritise unit tests for speed; use integration/e2e tests for confidence at the boundaries.
- **The Testing Pyramid**: Many fast unit tests → fewer integration tests → fewest e2e tests.

## Test Design Techniques
- **Equivalence Partitioning**: Dividing input ranges into classes that behave identically to minimise redundant test cases.
- **Boundary Value Analysis**: Testing values at and just beyond the edges of valid ranges (e.g. 0, 1, max-1, max).
- **Decision Table Testing**: Mapping combinations of conditions to expected outcomes for complex business rules.
- **State Transition Testing**: Verifying that a system moves correctly through its valid states and rejects invalid transitions.
- **Exploratory Testing**: Unscripted, hypothesis-driven testing to discover unexpected failures outside the planned test suite.

## Unit Testing
- **Arrange/Act/Assert (AAA)**: Clearly separate setup, execution, and verification in every test.
- **Table-driven tests**: `[]struct{ name, input, expected }` — cover multiple scenarios without code duplication.
- **Test Doubles**: Mocks, stubs, fakes, and spies — choosing the right double for each situation.
- **One logical assertion per test**: Focused tests produce clearer failure messages.
- **Descriptive naming**: `TestCreateUser_WhenEmailAlreadyExists_ReturnsDuplicateError`.

## Integration & End-to-End Testing
- `testcontainers-go` / `testcontainers-python`: Spinning up real PostgreSQL, Redis, Kafka containers in tests.
- Docker Compose for full-stack local test environments.
- Contract testing with Pact for microservice API boundaries.
- Playwright / Cypress / Selenium for browser-based e2e tests.
- Use separate test databases; clean up with transactions or truncation between tests.

## Performance & Load Testing
- **k6 / Locust / wrk**: Scripting realistic load scenarios with ramp-up, steady-state, and spike phases.
- **Baseline Benchmarks**: Establishing p50/p95/p99 latency and throughput baselines before optimisation.
- **Regression Detection**: Automated performance tests in CI that fail when latency exceeds defined thresholds.
- **Profiling Under Load**: Using `pprof`, `py-spy`, or `async-profiler` to identify hot paths during load tests.

## Security Testing
- **OWASP Top 10 Checklist**: Systematically checking for injection, broken auth, XSS, IDOR, and misconfiguration.
- **Fuzzing**: Using Go's `testing.F`, `atheris` (Python), or `AFL` to discover input-handling bugs automatically.
- **Dependency Scanning**: `govulncheck`, `pip-audit`, `npm audit`, `trivy` for known CVEs in dependencies.
- **SAST / DAST**: Static analysis (CodeQL, Semgrep) and dynamic analysis (OWASP ZAP) integrated into CI.

## Code Review
- **Correctness**: Does the code do what the spec says? Are all acceptance criteria covered?
- **Edge Cases**: What happens with empty input, nulls, boundary values, concurrent access?
- **Security**: Are inputs validated? Are secrets handled safely? Are SQL queries parameterised?
- **Testability**: Can this code be unit-tested without a real database or network call?
- **Readability**: Will a new team member understand this code in six months?

## CI/CD Integration
- Run `go test -race -count=1 ./...` (or equivalent) in CI to catch data races.
- Cache test binaries and module downloads between CI runs.
- Report test results in JUnit XML for CI dashboards.
- Block merges on failing tests; never bypass the quality gate.
- Parallelise slow integration tests with `-parallel N` or matrix builds.
