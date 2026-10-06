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
"""MCP Security Agent powered by Google ADK v2."""

__version__ = "0.2.0"
__all__ = ["create_security_agent", "root_agent", "__version__"]


def __getattr__(name: str):
    if name in ("create_security_agent", "root_agent"):
        import mcp_security_agent.agent as agent_mod
        return getattr(agent_mod, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__():
    return __all__
