# Copyright 2025 Google LLC
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
#
import setuptools

setup = setuptools.setup

setup(
    name="compliance-mcp",
    version="0.1.0",
    py_modules=["compliance_mcp", "main"],
    install_requires=[
        "mcp",
        "google-cloud-cloudsecuritycompliance",
        "google-cloud-org-policy",
    ],
    entry_points={
        "console_scripts": [
            "compliance_mcp=compliance_mcp:main",
        ],
    },
) 