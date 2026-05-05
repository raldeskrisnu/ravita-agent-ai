# Testing Skills

## Testing Philosophy
- **Tests are living documentation**: A good test describes the intended behaviour of the system, not just its current implementation.
- **Test behaviour, not implementation**: Tests should survive refactoring. Avoid testing private functions; test the public contract.
- **Fast feedback loops**: Prioritise unit tests for speed; use integration/e2e tests for confidence at the boundaries.
- **The Testing Trophy** (in order of ROI): Static analysis → Unit → Integration → E2E.

## Go Testing Fundamentals
- Standard library: `testing.T`, `t.Run` for sub-tests, `t.Parallel()` for concurrent test execution.
- Table-driven tests: define `[]struct{ name, input, expected }` and range over them.
- `t.Helper()` in assertion helpers to point to the failing call site.
- `testing.B` for benchmarks: `b.ResetTimer()`, `b.ReportAllocs()`.
- `testing.F` for fuzz testing (Go 1.18+): seed corpus, `f.Add`, `f.Fuzz`.
- `-count=N` flag to run tests N times (useful for detecting flakiness).
- `-timeout` flag to catch infinite loops in tests.

## Test Organisation
- File naming: `foo_test.go` for white-box tests in the same package; `foo_test` package suffix for black-box tests.
- Group related tests with `t.Run` sub-tests for clear failure messages.
- Keep test data in `testdata/` directory; use `golden files` for complex expected outputs.
- Use `TestMain` for setup/teardown that spans the whole test binary.

## Mocking & Faking
- Prefer interfaces over concrete types so dependencies can be swapped in tests.
- Generate mocks with `mockery` or write simple hand-rolled fakes for small interfaces.
- Use `httptest.NewServer` / `httptest.NewRecorder` for HTTP handler tests.
- Use `database/sql/driver` fakes or `testcontainers-go` for database tests.
- Avoid mocking what you don't own – wrap third-party clients behind your own interface.

## Integration & End-to-End Testing
- `testcontainers-go`: spin up real PostgreSQL, Redis, Kafka containers in tests.
- Docker Compose for full-stack local test environments.
- Use separate test databases; always clean up or use transactions that are rolled back.
- Contract testing with Pact for microservice boundaries.

## Test Quality
- **Arrange, Act, Assert** (AAA): clearly separate setup, execution, and verification.
- One logical assertion per test where practical.
- Descriptive test names: `TestCreateUser_WhenEmailAlreadyExists_ReturnsDuplicateError`.
- Avoid test interdependence – each test must be independently runnable.
- No sleeps (`time.Sleep`) in tests; use channels, polling, or `testify/assert.Eventually`.

## Coverage & Mutation Testing
- Aim for meaningful coverage, not 100% line coverage for its own sake.
- `go test -cover ./...` and `go tool cover -html=coverage.out` for visual reports.
- Focus coverage efforts on business logic and error paths.
- Mutation testing (e.g. `go-mutesting`) to validate that tests actually catch bugs.

## Test Utilities
- `github.com/stretchr/testify`: `assert`, `require`, `suite` packages.
- `github.com/google/go-cmp`: deep equality with custom comparers.
- `github.com/DATA-DOG/go-sqlmock`: SQL query mocking.
- `net/http/httptest`: HTTP client/server test helpers.
- `github.com/testcontainers/testcontainers-go`: real containers in tests.

## CI/CD Integration
- Run `go test -race -count=1 ./...` in CI to catch data races.
- Cache test binaries and module downloads between CI runs.
- Fail fast on first error in CI; run full suite before merging.
- Report test results in JUnit XML format for CI dashboards.
- Parallelise slow integration tests with `-parallel N`.
