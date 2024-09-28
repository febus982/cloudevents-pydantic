# cloudevents-pydantic
![Static Badge](https://img.shields.io/badge/Python-3.9_%7C_3.10_%7C_3.11_%7C_3.12-blue?logo=python&logoColor=white)
[![Stable Version](https://img.shields.io/pypi/v/cloudevents-pydantic?color=blue)](https://pypi.org/project/cloudevents-pydantic/)
[![stability-wip](https://img.shields.io/badge/stability-wip-lightgrey.svg)](https://github.com/mkenney/software-guides/blob/master/STABILITY-BADGES.md#work-in-progress)

[![Python tests](https://github.com/febus982/cloudevents-pydantic/actions/workflows/python-tests.yml/badge.svg?branch=main)](https://github.com/febus982/cloudevents-pydantic/actions/workflows/python-tests.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/c7fe3ebcadd850d7ed3f/maintainability)](https://codeclimate.com/github/febus982/cloudevents-pydantic/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/c7fe3ebcadd850d7ed3f/test_coverage)](https://codeclimate.com/github/febus982/cloudevents-pydantic/test_coverage)

[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v1.json)](https://github.com/charliermarsh/ruff)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)

This is an implementation of the [CloudEvents spec](https://github.com/cloudevents/spec/tree/main) using
[Pydantic V2](https://docs.pydantic.dev/latest/) for high performance during validation and serialization.

Currently supported bindings:

| Binding | Format | Single  |  Batch  |
|---------|:-------|:-------:|:-------:|
| HTTP    | JSON   |    ✅    |    ✅    |
| HTTP    | Binary | planned | planned |
| KAFKA   | JSON   | planned | planned |
| KAFKA   | Binary | planned | planned |

## How to use

```shell
pip install cloudevents-pydantic
```

```python
from cloudevents_pydantic.bindings.http import HTTPHandler
from cloudevents_pydantic.events import CloudEvent

handler = HTTPHandler()
minimal_attributes = {
    "type": "com.example.string",
    "source": "https://example.com/event-producer",
}

# `CloudEvent` is a Pydantic model to handle validation and serialization
# `event_factory` is a helper method to autogenerate some of the mandatory 
# such as id, time, specversion
event = CloudEvent.event_factory(**minimal_attributes)

# Single event HTTP serialization
headers, single_event_as_json = handler.to_json(event)

# Batch of events HTTP serialization
headers, batch_of_events_as_json = handler.to_json_batch([event])

# Parsing a JSON string for a single event
parsed_event = handler.from_json(single_event_as_json)

# Parsing a JSON string for a single event
parsed_event_list = handler.from_json(batch_of_events_as_json)
```

Refer to the [docs](https://febus982.github.io/cloudevents-pydantic/) for more advanced use cases and
for details on how to create custom events.

## Performance

Using pydantic gives a great performance boost if compared to the official SDK. (there's obviously
some performance issue in the official serialization using pydantic)

These results come from a Macbook Pro M3 Max on python 3.12. Feel free to run the `benchmark.py`
script yourself.

```
Timings for HTTP JSON deserialization:
This package: 3.0855846670019673
Official SDK with pydantic model: 15.35431600001175
Official SDK with http model: 13.728038166998886

Timings for HTTP JSON serialization:
This package: 4.292417042001034
Official SDK with pydantic model: 44.50933354199515
Official SDK with http model: 8.929204874992138
```


## Commands for development

All the common commands used during development can be run using make targets:

* `make dev-dependencies`: Install dev requirements
* `make update-dependencies`: Update dev requirements
* `make fix`: Run code style and lint automatic fixes (where possible)
* `make test`: Run test suite against system python version
* `make check`: Run tests against all available python versions, code style and lint checks
* `make type`, `make format`, `make lint`, `make bandit`: Run the relevant check
* `make docs`: Render the mkdocs website locally
