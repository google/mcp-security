# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Live connection test for Chronicle SOAR MCP."""

import asyncio
import os
import sys
from pathlib import Path
import dotenv

# Load environment
env_path = Path(__file__).resolve().parents[3] / ".env"
if env_path.exists():
    dotenv.load_dotenv(env_path)

# Add parent path to PYTHONPATH
sys.path.append(str(Path(__file__).resolve().parents[1]))

from secops_soar_mcp import bindings
from secops_soar_mcp.utils import consts

async def main():
    url = os.getenv("SOAR_URL")
    app_key = os.getenv("SOAR_APP_KEY")
    print(f"Connecting to SOAR URL: {url}")
    print(f"SOAR APP KEY defined: {bool(app_key)}")
    
    try:
        await bindings.bind()
        print("Successfully bound and verified scopes!")
        print(f"Valid scopes count: {len(bindings.valid_scopes)}")
        print(f"Scopes: {bindings.valid_scopes}")
        
        print("\nTesting list_cases endpoint...")
        cases = await bindings.http_client.get(consts.Endpoints.BASE_CASE_URL)
        if cases is not None:
            print("Successfully retrieved cases from live API!")
            if isinstance(cases, list):
                print(f"Retrieved {len(cases)} cases.")
                if len(cases) > 0:
                    print("Sample case summary:")
                    first_case = cases[0]
                    if isinstance(first_case, dict):
                        for k in ["id", "identifier", "name", "priority", "status"]:
                            print(f"  {k}: {first_case.get(k)}")
                    else:
                        print(f"  Raw: {first_case}")
            else:
                print("Response content:")
                print(cases)
        else:
            print("Failed to fetch cases (response was None).")
            
    except Exception as e:
        print(f"Error during live test execution: {e}")
    finally:
        if bindings.http_client:
            await bindings.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
