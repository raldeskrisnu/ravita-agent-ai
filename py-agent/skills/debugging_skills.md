# Debugging Skills

## Debugging Mindset
- **Reproduce first**: Never attempt a fix without a reliable reproduction case.
- **Narrow the blast radius**: Isolate the smallest possible failing unit before diving into the full stack.
- **Hypothesise, then verify**: Form a specific hypothesis about the root cause, then gather evidence to confirm or refute it. Avoid random changes.
- **Understand before fixing**: Know *why* the bug exists before writing the fix, or you risk introducing new bugs.

## Go-Specific Debugging
- Use `fmt.Println` / `log` for quick sanity checks; remove before committing.
- Use `delve` (`dlv`) for interactive step-through debugging: `dlv debug`, breakpoints, variable inspection.
- Race detector: `go test -race ./...` to surface data races.
- `pprof` for CPU and heap profiling: `import _ "net/http/pprof"` + `go tool pprof`.
- `go vet` and `staticcheck` for static analysis.
- `goleak` for goroutine leak detection in tests.

## Systematic Debugging Process
1. **Read the error message carefully** – most bugs announce themselves.
2. **Check recent changes** – `git log --oneline -20`, `git diff HEAD~1`.
3. **Add structured logging** – log inputs, outputs, and key decision points.
4. **Inspect state** – check database records, cache contents, queue depth.
5. **Bisect** – use `git bisect` to pinpoint when a regression was introduced.
6. **Reduce the problem** – write a minimal reproducer; this often reveals the root cause.

## Common Bug Categories & Signals

### Concurrency Bugs
- Symptoms: intermittent failures, race conditions, deadlocks.
- Tools: `-race` flag, `sync.Mutex` audits, channel direction review.
- Patterns: missing locks, double-checked locking, goroutine leaks.

### Memory Issues
- Symptoms: OOM crashes, unexpectedly high memory usage.
- Tools: `pprof` heap profiles, `runtime.ReadMemStats`.
- Patterns: unbounded slices/maps, forgotten goroutines holding references.

### Network / Timeout Issues
- Symptoms: intermittent 504s, request pile-up, connection pool exhaustion.
- Tools: `tcpdump`, `netstat`, distributed tracing.
- Patterns: missing context deadlines, no timeout on HTTP clients, connection leak.

### Logic Bugs
- Symptoms: wrong output, off-by-one errors, incorrect state transitions.
- Tools: unit tests, property-based testing.
- Patterns: integer overflow, nil pointer dereference, incorrect boundary conditions.

### Configuration & Environment Bugs
- Symptoms: "works on my machine", environment-specific failures.
- Tools: compare env vars, Docker inspect, `strace` / `ltrace`.
- Patterns: missing env variables, wrong file paths, clock skew.

## Production Debugging
- Use structured log queries (Loki, CloudWatch Insights, Datadog Logs).
- Correlate traces with logs via trace ID / request ID.
- Take heap / goroutine dumps from live processes: `kill -SIGUSR1` (Go runtime dumps goroutines to stderr).
- Feature flags to disable suspect code paths without a deploy.
- Never run `DELETE` or `UPDATE` without a `SELECT` first to verify scope.

## Post-Mortem Practice
- Write a blameless post-mortem after every significant incident.
- Document: timeline, root cause, contributing factors, action items.
- Track action items to completion; revisit in the next retrospective.
