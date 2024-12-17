******************************************
## Welcome to `ibm-watsonx-orchestrate`
******************************************

`ibm-watsonx-orchestrate` is a Python SDK that allows you to build expert and orchestrator agents and interact with the watsonx.orchestrate service It also provides a convenient interface for managing credentials, sending requests, and handling responses from the service’s APIs.

------------------------------------------

## Prerequisites

- **Python 3.12+**  
  Ensure you have Python 3.12 or later installed.

- **Dependencies**  
  All required dependencies will be automatically installed when you install the wheel package.

------------------------------------------

## How to Install the Library

Once you have cloned the repo, you can install it locally with `pip`:

```bash
pip install .
```

*(Update the filename to match the version you’ve built.)*

After installation, you can import and use the SDK in your Python code:

```python
from ibm_watsonx_orchestrate.client import Client

client = Client(api_key="your-api-key")
response = client.some_function()
print(response)
```

------------------------------------------