******************************************
## Welcome to `ibm-watsonx-orchestrate`
******************************************

`ibm-watsonx-orchestrate` is a Python SDK that allows you to build expert and orchestrator agents and interact with the watsonx.orchestrate service. It also provides a convenient interface for managing credentials, sending requests, and handling responses from the service’s APIs.

------------------------------------------

## Prerequisites

- **Python 3.12+**  
  Ensure you have Python 3.12 or later installed.

- **Dependencies**  
  All required dependencies will be automatically installed when you install the package.

------------------------------------------

## How to Install the Library

Once you have cloned the repo, you can install it locally with `pip`:

```bash
pip install -e .[dev]
```

### Why `-e`?  
The `-e` flag is optional and stands for "editable mode." This allows you to make changes to the source code of the library and have those changes reflected immediately without needing to reinstall the package. This is useful for development purposes.

---

## How to Build the distributable Package

To build the package, use [Hatch](https://hatch.pypa.io/latest/), a modern Python project management tool. Follow these steps:

1. **Install Hatch**  
   If you don’t already have Hatch installed, install it using `pip`:

   ```bash
   pip install hatch
   ```

2. **Build the Package**  
   Navigate to the root directory of the project and run:

   ```bash
   hatch build
   ```

   This will create the distribution files (e.g., `.whl` and `.tar.gz`) in the `dist` directory.

3. **Install the Package**  
   Once the package is built, you can install it locally:

   ```bash
   pip install dist/<filename>.whl
   ```

*(Replace `<filename>` with the actual name of the wheel file created in the `dist` directory.)*

---

## Usage

After installation, you can import and use the SDK in your Python code:

```python
from ibm_watsonx_orchestrate.client import Client

client = Client(api_key="your-api-key")
response = client.some_function()
print(response)
```

------------------------------------------
