# Testing Standards

1. **Test-First Discipline**: For every task, Test Author writes failing unit tests covering all task acceptance criteria before Builder implements code.
2. **Deterministic & Hermetic**: Unit tests must execute quickly (< 1s per test) and must not require internet access.
3. **No Mocks of Unit Under Test**: Unit under test must be executed directly; only external dependencies or long-running downloads may be mocked.
4. **Coverage Floor**: Minimum 80% line coverage required on core modules in `src/namethellm/`.
5. **Forbidden Practices**:
   - Never skip tests or add xfail markers to achieve a green build.
   - Never use blanket try/except blocks to swallow test assertions.
   - Never weaken assertions to fit incorrect implementations.
