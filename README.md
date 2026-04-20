# zelighted

Python client for the [Zelighted](https://github.com/luuna-tech/ZeLighted) NPS/CSAT survey API.

[![CI](https://github.com/luuna-tech/Zelighted-python/actions/workflows/ci.yml/badge.svg)](https://github.com/luuna-tech/Zelighted-python/actions/workflows/ci.yml)
[![PyPI version](https://img.shields.io/pypi/v/zelighted)](https://pypi.org/project/zelighted/)
[![Python versions](https://img.shields.io/pypi/pyversions/zelighted)](https://pypi.org/project/zelighted/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

---

## Installation

```bash
pip install zelighted
```

With optional `.env` file support:

```bash
pip install "zelighted[dotenv]"
```

---

## Configuration

### Option 1: Environment variables

```bash
export ZELIGHTED_API_URL=https://api.zeb.mx/api/v1/   # production
# export ZELIGHTED_API_URL=https://api-stg.zeb.mx/api/v1/  # staging
# export ZELIGHTED_API_URL=http://localhost:8001/api/v1/    # local dev (default)
export ZELIGHTED_API_KEY=your_api_key
```

`zelighted` reads these on import. `ZELIGHTED_API_URL` defaults to `http://localhost:8001/api/v1/` if unset.

### Option 2: `zelighted.configure()`

```python
import zelighted

zelighted.configure(
    api_base_url="https://api.zeb.mx/api/v1/",
    api_key="YOUR_API_KEY",
)
```

If `python-dotenv` is installed, `configure()` loads `.env` automatically before applying values.

### Option 3: Per-client configuration

```python
from zelighted import Client

client = Client(
    api_key="YOUR_API_KEY",
    api_base_url="https://api.zeb.mx/api/v1/",
)
```

Pass `client=client` to any resource call to use a specific client instance.

---

## Usage

### Person

```python
import zelighted

# Create and schedule a survey immediately
person = zelighted.Person.create(email="user@example.com")

# Create with a 60-second delay
person = zelighted.Person.create(email="user@example.com", delay=60)

# Create without scheduling a survey
person = zelighted.Person.create(email="user@example.com", send=False)

# Create with properties
person = zelighted.Person.create(
    email="user@example.com",
    name="Jane Doe",
    properties={"customer_id": 42, "plan": "pro"},
    delay=30,
)

# List all people (auto-paginated)
for person in zelighted.Person.list().auto_paging_iter():
    print(person.id)

# Delete by id, email, or phone
zelighted.Person.delete(id=42)
zelighted.Person.delete(email="user@example.com")
zelighted.Person.delete(phone_number="+14155551212")
```

### SurveyResponse

```python
import zelighted

# Create
response = zelighted.SurveyResponse.create(person=person.id, score=9)
response = zelighted.SurveyResponse.create(person=person.id, score=5, comment="Good service.")

# Retrieve
response = zelighted.SurveyResponse.retrieve("123")

# Update
response.score = 10
response.save()

# List
page1 = zelighted.SurveyResponse.all()
page2 = zelighted.SurveyResponse.all(page=2)
expanded = zelighted.SurveyResponse.all(expand=["person"])
desc = zelighted.SurveyResponse.all(order="desc")

import datetime, pytz
tz = pytz.timezone("America/Chicago")
filtered = zelighted.SurveyResponse.all(
    since=tz.localize(datetime.datetime(2024, 1, 1)),
    until=tz.localize(datetime.datetime(2024, 3, 31)),
)
```

### Metrics

```python
import zelighted

metrics = zelighted.Metrics.retrieve()
metrics = zelighted.Metrics.retrieve(trend="123")

import datetime, pytz
tz = pytz.timezone("America/Chicago")
metrics = zelighted.Metrics.retrieve(
    since=tz.localize(datetime.datetime(2024, 1, 1)),
    until=tz.localize(datetime.datetime(2024, 3, 31)),
)
```

### Unsubscribe

```python
import zelighted

# Unsubscribe a person
zelighted.Unsubscribe.create(person_email="user@example.com")

# List unsubscribed people
page1 = zelighted.Unsubscribe.all()
page2 = zelighted.Unsubscribe.all(page=2)
```

### Bounce

```python
import zelighted

page1 = zelighted.Bounce.all()
page2 = zelighted.Bounce.all(page=2)
```

### SurveyRequest

```python
import zelighted

# Delete pending survey requests for a person
zelighted.SurveyRequest.delete_pending(person_email="user@example.com")
```

### AutopilotMembership

```python
import zelighted

# Email autopilot
zelighted.AutopilotMembership.forEmail().create(person_email="user@example.com")
for member in zelighted.AutopilotMembership.forEmail().list().auto_paging_iter():
    print(member)
zelighted.AutopilotMembership.forEmail().delete(person_email="user@example.com")

# SMS autopilot
zelighted.AutopilotMembership.forSms().create(person_phone_number="+14155551212")
for member in zelighted.AutopilotMembership.forSms().list().auto_paging_iter():
    print(member)
zelighted.AutopilotMembership.forSms().delete(person_phone_number="+14155551212")
zelighted.AutopilotMembership.forSms().delete(person_id=42)
```

---

## Pagination

Use `auto_paging_iter()` to iterate through all pages automatically:

```python
import zelighted

# Handle rate limits manually
people = zelighted.Person.list()
while True:
    try:
        for person in people.auto_paging_iter():
            print(person.id)
        break
    except zelighted.errors.TooManyRequestsError as e:
        import time
        time.sleep(e.retry_after)

# Or let the client handle rate limits for you
for person in zelighted.Person.list(auto_handle_rate_limits=True).auto_paging_iter():
    print(person.id)
```

---

## Error Handling

```python
import zelighted
from zelighted.errors import (
    ZelightedError,
    AuthenticationError,
    TooManyRequestsError,
)

try:
    metrics = zelighted.Metrics.retrieve()
except AuthenticationError:
    print("Invalid API key.")
except TooManyRequestsError as e:
    print(f"Rate limited. Retry after {e.retry_after} seconds.")
except ZelightedError as e:
    print(f"API error: {e}")
```

---

## Release Process

1. Bump `__version__` in `zelighted/__init__.py` (e.g. `5.1.0` → `5.2.0`)
2. Add a matching entry to `CHANGELOG.md`
3. Push to `master`
4. CI automatically: runs tests → detects version bump → builds package → uploads to PyPI → creates GitHub Release with changelog notes → pushes git tag `v{version}`

> **Prerequisite:** `PYPI_API_TOKEN` must be set as a repository secret in GitHub → Settings → Secrets and variables → Actions.

---

## Contributing

```bash
git clone https://github.com/luuna-tech/Zelighted-python.git
cd Zelighted-python
pip install -e ".[dotenv]"
pip install pytest pytz tzlocal
pytest test/ -v
```

Branch naming: `spec/SPEC-XXX` for spec work, `fix/short-description` for bug fixes.

1. Fork the repo
2. Create your branch (`git checkout -b spec/SPEC-XXX`)
3. Run the tests (`pytest test/ -v`)
4. Commit your changes
5. Push and open a Pull Request against `master`

---

## License

MIT — see [LICENSE](LICENSE).
