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

import pytest_asyncio


@pytest_asyncio.fixture(loop_scope="session", autouse=True)
async def setup_bindings():
    """Overrides tests/conftest.py's fixture: these unit tests mock
    bindings/http_client directly and must not require real SOAR
    credentials or network access."""
    yield
