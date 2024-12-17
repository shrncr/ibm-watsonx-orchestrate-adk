******************************************
## Welcome to `ibm-watsonx-orchestrate`
******************************************

`ibm-watsonx-orchestrate` is a Python SDK that allows you to interact with the watsonx.orchestrate service. It provides a convenient interface for managing credentials, sending requests, and handling responses from the service’s APIs.

------------------------------------------

## Prerequisites

- **Python 3.12+**  
  Ensure you have Python 3.12 or later installed.

- **Dependencies**  
  All required dependencies will be automatically installed when you install the wheel package.

------------------------------------------

## How to Build the Installable Python Package

This project uses a `pyproject.toml` file for packaging, adhering to modern Python packaging standards (PEP 517/518).

There are two ways to build the package:

1. **Using the `build.sh` Script:**
   
   From the project root directory, run:
   
   ```bash
   sh <project root>/ibm_watsonx_orchestrate/build.sh
   ```
   
   This script will clean previous builds and execute the package build. On successful execution, the `.whl` and `.tar.gz` files will be created in the `dist/` directory:
   
   ```
   dist/
   ├── wxo_clients-0.1.0-py3-none-any.whl
   └── wxo_clients-0.1.0.tar.gz
   ```

2. **Using `python -m build` Directly:**
   
   Install the build tool first:
   ```bash
   pip install build
   ```
   
   Then run:
   ```bash
   python -m build
   ```
   
   This will also create the build artifacts in the `dist/` directory.

------------------------------------------

## How to Install the Library

Once you have built the package, you can install it locally with `pip`:

```bash
pip install dist/wxo_clients-0.1.0-py3-none-any.whl
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