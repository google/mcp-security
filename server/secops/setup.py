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
#
#!/usr/bin/env python3
import setuptools

setup = setuptools.setup

setup(
    name="google-secops-mcp",
    version="0.7.1",
    py_modules=["secops_mcp", "main"],  # Include both modules
    install_requires=[
        "httpx>=0.28.1",
        "mcp[cli]>=1.26.0,<2.0",
        "secops>=0.35.1",
        "google-auth>=2.48.0",
        "google-auth-httplib2>=0.3.0",
        "google-api-python-client>=2.190.0",
    ],
    entry_points={
        "console_scripts": [
            "secops-mcp=secops_mcp.server:main",
        ],
    },
)
