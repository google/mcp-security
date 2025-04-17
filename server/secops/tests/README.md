# Chronicle SecOps MCP Integration Tests

This directory contains integration tests for the Chronicle SecOps MCP tools. These tests make actual API calls to the Chronicle service to verify the functionality of the tools.

## Requirements

1. Python 3.11 or later
2. Google Cloud SDK installed and configured
3. Chronicle API access
4. Required Python packages installed (see installation instructions below)

## Installation

The tests require pytest and pytest-asyncio, which are specified as optional dependencies in the package. To install the package with test dependencies:

```bash
# Navigate to the secops directory
cd server/secops

# Install the package with test dependencies
pip install -e ".[test]"
```

## Configuration

Before running the tests, you need to create a `config.json` file in this directory with your Chronicle credentials:

```json
{
    "CHRONICLE_PROJECT_ID": "your-project-id",
    "CHRONICLE_CUSTOMER_ID": "your-customer-id",
    "CHRONICLE_REGION": "us"
}
```

You can use the example configuration file as a template:

```bash
# Copy the example config file
cp config.json.example config.json

# Edit the config.json file with your credentials
nano config.json  # or your preferred editor
```

Make sure to replace the placeholder values with your actual Chronicle credentials.

## Authentication

The tests use Google Application Default Credentials (ADC) for authentication. Make sure you have authenticated with:

```bash
gcloud auth application-default login
```

## Running the Tests

To run the tests, from the project root directory:

```bash
# Run all tests
python -m pytest -xvs server/secops/tests/test_secops_mcp.py

# Run a specific test
python -m pytest -xvs server/secops/tests/test_secops_mcp.py::TestChronicleSecOpsMCP::test_search_security_events_basic
```

## Test Coverage

The tests cover all the tools in `secops_mcp.py`:

1. `search_security_events` - Tests natural language search
2. `get_security_alerts` - Tests alert retrieval with various filters
3. `lookup_entity` - Tests entity lookup for IPs, domains, and file hashes
4. `list_security_rules` - Tests rule listing
5. `get_ioc_matches` - Tests IoC match retrieval
6. `get_threat_intel` - Tests threat intelligence queries

## Debugging

If a test fails, check:
1. Your Chronicle credentials are correct
2. You have the necessary permissions
3. Your GCP authentication is valid
4. The Chronicle API is available
5. The test's expectations match your Chronicle environment's data 