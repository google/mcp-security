# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Google Security Operations MCP server.

This module implements the Security Operations MCP server to perform
security operations tasks using Chronicle, including natural language search.
"""

import logging
import os
import signal
import sys
import threading
import time
from typing import Any, Optional

from mcp.server.fastmcp import FastMCP
from secops import SecOpsClient

# Initialize FastMCP server with a descriptive name
server = FastMCP('Google Security Operations MCP server', log_level="ERROR")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('secops-mcp')

# Constants
USER_AGENT = 'secops-app/1.0'

# Default Chronicle configuration from environment variables
DEFAULT_PROJECT_ID = os.environ.get('CHRONICLE_PROJECT_ID', '725716774503')
DEFAULT_CUSTOMER_ID = os.environ.get(
    'CHRONICLE_CUSTOMER_ID', 'c3c6260c1c9340dcbbb802603bbf9636'
)
DEFAULT_REGION = os.environ.get('CHRONICLE_REGION', 'us')


def get_chronicle_client(
    project_id: Optional[str] = None, 
    customer_id: Optional[str] = None, 
    region: Optional[str] = None
) -> Any:
    """Initialize and return a Chronicle client.

    Args:
        project_id: Google Cloud project ID (defaults to CHRONICLE_PROJECT_ID env var)
        customer_id: Chronicle customer ID (defaults to CHRONICLE_CUSTOMER_ID env var)
        region: Chronicle region (defaults to CHRONICLE_REGION env var or "us")

    Returns:
        Any: Initialized Chronicle client
        
    Raises:
        ValueError: If required configuration is missing
        RuntimeError: If authentication fails or times out
    """
    # Use provided values or defaults from environment variables
    project_id = project_id or DEFAULT_PROJECT_ID
    customer_id = customer_id or DEFAULT_CUSTOMER_ID
    region = region or DEFAULT_REGION

    if not project_id or not customer_id:
        raise ValueError(
            'Chronicle project_id and customer_id must be provided either '
            'as parameters or through environment variables '
            '(CHRONICLE_PROJECT_ID, CHRONICLE_CUSTOMER_ID)'
        )

    # Check for Google Cloud authentication credentials
    google_creds = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
    if not google_creds:
        # Check if ADC might be available
        try:
            from google.auth import default
            default()
        except Exception:
            raise RuntimeError(
                'Google Cloud authentication is required but not configured.\n\n'
                'Please set up authentication using one of these methods:\n'
                '1. Set GOOGLE_APPLICATION_CREDENTIALS environment variable:\n'
                '   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-key.json"\n\n'
                '2. Use Application Default Credentials (ADC):\n'
                '   gcloud auth application-default login\n\n'
                '3. Set up a service account and download the key file\n\n'
                'For more information, see: https://cloud.google.com/docs/authentication'
            )

    # Initialize client with timeout protection
    logger.info('Initializing SecOps client...')
    
    # Use threading-based timeout for cross-platform compatibility
    client_result = [None]
    client_error = [None]
    
    def init_client():
        try:
            client = SecOpsClient()
            chronicle = client.chronicle(
                customer_id=customer_id, project_id=project_id, region=region
            )
            client_result[0] = chronicle
        except Exception as e:
            client_error[0] = e
    
    # Start initialization in a separate thread
    init_thread = threading.Thread(target=init_client, daemon=True)
    init_thread.start()
    
    # Wait for initialization with timeout
    timeout_seconds = 30
    init_thread.join(timeout=timeout_seconds)
    
    if init_thread.is_alive():
        # Thread is still running - initialization timed out
        raise TimeoutError(
            f'SecOps client initialization timed out after {timeout_seconds} seconds. '
            'This usually indicates an authentication problem.\n\n'
            'Please verify:\n'
            '1. GOOGLE_APPLICATION_CREDENTIALS is correctly set\n'
            '2. The service account has necessary permissions for Chronicle Security Operations\n'
            '3. Network connectivity to Google Cloud APIs\n'
            '4. The specified project_id, customer_id, and region are correct'
        )
    
    if client_error[0]:
        # Initialization failed with an exception
        logger.error(f'Failed to initialize SecOps client: {str(client_error[0])}')
        raise RuntimeError(
            f'Failed to initialize Chronicle SecOps client: {str(client_error[0])}\n\n'
            'This error often indicates:\n'
            '1. Missing or invalid GOOGLE_APPLICATION_CREDENTIALS\n'
            '2. Insufficient permissions on the service account\n'
            '3. Network connectivity issues\n'
            '4. Invalid project_id, customer_id, or region\n\n'
            'Please verify your configuration and try again.'
        )
    
    if client_result[0] is None:
        # Unexpected case - no result and no error
        raise RuntimeError(
            'SecOps client initialization completed but returned no result. '
            'This may indicate an internal error.'
        )
    
    logger.info('SecOps client initialized successfully')
    return client_result[0]


# Import all tools
from secops_mcp.tools import *


def main() -> None:
    """Run the MCP server for SecOps tools.

    This function initializes and starts the MCP server with all the defined
    tools.
    """
    # Initialize and run the server
    server.run(transport='stdio')


if __name__ == '__main__':
    main() 