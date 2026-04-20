# Zelighted API Python Client

[![CI](https://github.com/luuna-tech/Zelighted-python/actions/workflows/ci.yml/badge.svg)](https://github.com/luuna-tech/Zelighted-python/actions/workflows/ci.yml)

Python client for the Zelighted API.

## Installation

```
pip install --upgrade zelighted
```

## Configuration

### Option 1: Environment variables

```bash
export ZELIGHTED_API_URL=https://api.zeb.mx/api/v1/
export ZELIGHTED_API_KEY=your_api_key
```

On import, `zelighted` reads `ZELIGHTED_API_URL` (defaults to `http://localhost:8001/api/v1/` if unset) and `ZELIGHTED_API_KEY` automatically.

Common URL values:
- Local development: `http://localhost:8001/api/v1/`
- Staging: `https://api-stg.zeb.mx/api/v1/`
- Production: `https://api.zeb.mx/api/v1/`

### Option 2: `zelighted.configure()`

```python
import zelighted

zelighted.configure(api_base_url='https://api.zeb.mx/api/v1/', api_key='YOUR_API_KEY')
```

If `python-dotenv` is installed, `configure()` loads `.env` automatically before applying config. If `python-dotenv` is missing or `.env` is absent, this is silently skipped.

### Option 3: Manual assignment

```python
import zelighted

zelighted.api_key = 'YOUR_API_KEY'
zelighted.api_base_url = 'https://api.zeb.mx/api/v1/'
```

**Note:** Your API key is secret and should be treated like a password.

## Usage

Adding/updating people and scheduling surveys:

```python
# Add a new person, and schedule a survey immediately
person1 = zelighted.Person.create(email='foo+test1@example.com')

# Add a new person, and schedule a survey after 1 minute (60 seconds)
person2 = zelighted.Person.create(email='foo+test2@example.com', delay=60)

# Add a new person, but do not schedule a survey
person3 = zelighted.Person.create(email='foo+test3@example.com', send=False)

# Add a new person with full set of attributes and schedule a survey with a 30 second delay
person4 = zelighted.Person.create(
        email='foo+test4@example.com',
        name='Joe Bloggs',
        properties={'customer_id': 123, 'country': 'USA',
                    'question_product_name': 'The London Trench'},
        delay=30)

# Update an existing person (identified by email), adding a name, without scheduling a survey
updated_person1 = zelighted.Person.create(email='foo+test1@example.com',
                                          name='James Scott', send=False)
```

Unsubscribing people:

```python
zelighted.Unsubscribe.create(person_email='foo+test1@example.com')
```

Listing people:

```python
# List all people, auto pagination
people = zelighted.Person.list()
while True:
    try:
        for person in people.auto_paging_iter():
            # Do something with person
            pass
    except TooManyRequestsError as e:
        e.retry_after
        continue

# For convenience, automatically handle rate limits
people = zelighted.Person.list(auto_handle_rate_limits=True)
for person in people.auto_paging_iter():
    # Do something with person
    pass
```

Listing people who have unsubscribed:

```python
zelighted.Unsubscribe.all()
zelighted.Unsubscribe.all(page=2)
```

Listing people whose emails have bounced:

```python
zelighted.Bounce.all()
zelighted.Bounce.all(page=2)
```

Deleting a person and all of the data associated with them:

```python
zelighted.Person.delete(id=42)
zelighted.Person.delete(email='test@example.com')
zelighted.Person.delete(phone_number='+14155551212')
```

Deleting pending survey requests:

```python
zelighted.SurveyRequest.delete_pending(person_email='foo+test1@example.com')
```

Adding survey responses:

```python
survey_response1 = zelighted.SurveyResponse.create(person=person1.id, score=10)
survey_response2 = zelighted.SurveyResponse.create(person=person1.id, score=5, comment='Really nice.')
```

Retrieving a survey response:

```python
survey_response3 = zelighted.SurveyResponse.retrieve('123')
```

Updating survey responses:

```python
survey_response4 = zelighted.SurveyResponse.retrieve('234')
survey_response4.score = 10
survey_response4.save()
```

Listing survey responses:

```python
survey_responses_page1 = zelighted.SurveyResponse.all()
survey_responses_page2 = zelighted.SurveyResponse.all(page=2)
survey_responses_page1_expanded = zelighted.SurveyResponse.all(expand=['person'])
survey_responses_page1_desc = zelighted.SurveyResponse.all(order='desc')

import pytz
timezone = pytz.timezone('America/Chicago')
filtered_survey_responses = zelighted.SurveyResponse.all(
    page=5,
    per_page=100,
    since=timezone.localize(datetime.datetime(2014, 3, 1)),
    until=timezone.localize(datetime.datetime(2014, 4, 30))
)
```

Retrieving metrics:

```python
metrics = zelighted.Metrics.retrieve()
metrics = zelighted.Metrics.retrieve(trend='123')

import pytz
timezone = pytz.timezone('America/Chicago')
metrics = zelighted.Metrics.retrieve(
    since=timezone.localize(datetime.datetime(2013, 10, 1)),
    until=timezone.localize(datetime.datetime(2013, 11, 1))
)
```

Managing Autopilot:

```python
autopilot = zelighted.AutopilotConfiguration.retrieve('email')

people_autopilot = zelighted.AutopilotMembership.forEmail().list(auto_handle_rate_limits=True)
for person in people_autopilot.auto_paging_iter():
    pass

autopilot = zelighted.AutopilotMembership.forEmail().create(person_email='test@example.com')

zelighted.AutopilotMembership.forSms().delete(person_id=42)
zelighted.AutopilotMembership.forEmail().delete(person_email='test@example.com')
zelighted.AutopilotMembership.forSms().delete(person_phone_number='+14155551212')
```

## Rate limits

```python
try:
    metrics = zelighted.Metrics.retrieve()
except zelighted.errors.TooManyRequestsError as err:
    retry_after_seconds = err.retry_after
    # wait for retry_after_seconds before retrying
```

## Advanced configuration

```python
zelighted.api_key
zelighted.api_base_url  # default: 'http://localhost:8001/api/v1/'
zelighted.http_adapter  # default: zelighted.HTTPAdapter
```

Custom client:

```python
import zelighted
from zelighted import Client
client = Client(api_key='API_KEY',
                api_base_url='http://localhost:8001/api/v1/',
                http_adapter=zelighted.HTTPAdapter())
metrics_from_custom_client = zelighted.Metrics.retrieve(client=client)
```

## Supported versions

- Python 3.8, 3.9, 3.10, 3.11

## Contributing

1. Fork it
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Run the tests (`python -m pytest test/ -v`)
4. Commit your changes (`git commit -am 'Add some feature'`)
5. Push to the branch (`git push origin my-new-feature`)
6. Create new Pull Request

## Releasing

1. Bump the version in `zelighted/__init__.py`.
2. Update the README and CHANGELOG as needed.
3. Tag the commit for release.
4. Create the distribution `python setup.py sdist`
5. Upload to PyPI with `twine upload dist/PACKAGE_NAME`.
