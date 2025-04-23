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
import re

PYTHON_KEYWORDS = [
    "False",
    "None",
    "True",
    "and",
    "as",
    "assert",
    "async",
    "await",
    "break",
    "class",
    "continue",
    "def",
    "del",
    "elif",
    "else",
    "except",
    "finally",
    "for",
    "from",
    "global",
    "if",
    "import",
    "in",
    "is",
    "lambda",
    "nonlocal",
    "not",
    "or",
    "pass",
    "raise",
    "return",
    "try",
    "while",
    "with",
    "yield",
]


def to_snake_case(name: str) -> str:
    """Converts CamelCase, PascalCase, and space-separated strings to snake_case."""
    original_name_for_fallback = name  # Keep original for potential hash fallback
    if not name:
        return "_unnamed_parameter"
    name = name.replace("(", "")
    name = name.replace(")", "")
    name = name.replace("|", "")
    name = name.replace("'", "")
    name = name.replace("`", "")
    name = name.replace("’", "")
    name = name.replace('"', "")
    name = name.replace("->", "to")
    # Replace known separators and unwanted chars with underscore
    name = re.sub(r"[\s\-./\\]+", "_", name)
    # Insert underscore before uppercase letters preceded by a lowercase/digit
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    # Insert underscore before uppercase letters preceded by another uppercase (for acronyms) followed by lowercase
    name = re.sub("([a-z0-9])([A-Z])", r"\1_\2", name)
    # Handle cases like 'IPAddress' -> 'ip_address' correctly
    name = re.sub("([A-Z]+)([A-Z][a-z])", r"\1_\2", name)
    # Convert to lowercase
    name = name.lower()
    # Remove leading/trailing underscores
    name = name.strip("_")
    # Replace multiple underscores with single underscore
    name = re.sub(r"_+", "_", name)
    # Ensure it's a valid Python identifier
    if not name:
        return "_unnamed_parameter"
    if not name[0].isalpha() and name[0] != "_":
        name = "_" + name
    # Final check for empty string after all processing
    if not name:
        # Extremely unlikely, but provide a fallback using hash
        import hashlib

        name_hash = hashlib.md5(original_name_for_fallback.encode()).hexdigest()[:6]
        return f"_param_{name_hash}"
    # Remove one or more non-alphanumeric/non-underscore characters from the end
    name = re.sub(r"[^a-z0-9_]+$", "", name)
    if name in PYTHON_KEYWORDS:
        name += "_"
    return name


def normalize_integration_name(integration_name: str) -> str:
    return integration_name.replace(" ", "").replace("/", "").lower()
