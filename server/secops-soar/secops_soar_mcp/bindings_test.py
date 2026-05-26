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

"""Tests for SecOps SOAR binding startup errors."""

import ssl

from secops_soar_mcp import bindings


def test_valid_scopes_error_message_identifies_certifi_issue():
    error = ssl.SSLCertVerificationError("certificate verify failed")

    message = bindings._valid_scopes_error_message(error)

    assert "TLS certificate verification failed" in message
    assert "Install Certificates.command" in message
    assert "certifi" in message


def test_valid_scopes_error_message_preserves_credentials_hint():
    message = bindings._valid_scopes_error_message(RuntimeError("401 unauthorized"))

    assert "configured the right SOAR credentials" in message
