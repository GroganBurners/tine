# Security Policy

## Supported Versions

Security fixes target the current `master` branch. Use the runtime and dependency
versions specified in the repository:

| Component | Current version | Source |
| --- | --- | --- |
| Python | 3.14 | `Dockerfile` and GitHub Actions workflows |
| Django | 6.1.1 | `requirements.txt` |
| Other Python dependencies | Exact pinned versions | `requirements.txt` |

Older versions of the application are not maintained separately. Dependency
updates must pass the application tests and compatibility checks before use.
The legacy PostgreSQL 10.4 configuration in `docker-compose.yml` requires an
upgrade before running the current application; preserve and migrate existing
data rather than reusing its data directory with a newer PostgreSQL image.

## Security Checks

GitHub Actions runs Bandit against application code, management commands, and
tests on pushes and pull requests, and uploads its JSON report as an artifact.
Findings fail the security job. Any `nosec` exception must identify the specific
check and explain why the operation is safe; broad exclusions should be avoided.

Run the same check locally with the Bandit version pinned in
`.github/workflows/main.yml`:

```sh
bandit -r gbs tine manage.py -f json -o report.json
```

A scheduled workflow checks for outdated Python dependencies. These checks and
the test suite help detect problems but do not guarantee the absence of
vulnerabilities.

## Reporting a Vulnerability

Do not post vulnerability details, credentials, or personal data in public issues.
If private vulnerability reporting is available, use the repository's
[Security tab](https://github.com/GroganBurners/tine/security) to report privately.
Otherwise, ask [dueyfinster](https://github.com/dueyfinster) for a private reporting
channel without disclosing sensitive details publicly.

Include the affected commit or version, reproduction steps, expected impact,
and any suggested mitigation. Remove credentials and personal data from logs
and examples. Allow the maintainer to investigate and coordinate a fix before
public disclosure.
