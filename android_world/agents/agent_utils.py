# Copyright 2024 The android_world Authors.
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

"""Utilities for agents."""

import ast
import json
import re
from typing import Any


def extract_json(s: str) -> dict[str, Any] | None:
  """Extracts JSON from string.

  Tries conversion with ast and json modules. If special_fill_form is True,
  will attempt to parse fill_form actions with nested lists more robustly.

  Args:
    s: A string with a JSON in it.

  Returns:
    JSON object.
  """
  if '"action_type": "fill_form"' in s:
    # Try to extract the JSON object using a greedy match for the outermost braces
    first = s.find('{')
    last = s.rfind('}')
    if first != -1 and last != -1:
      json_str = s[first:last+1]
      try:
        return json.loads(json_str)
      except Exception as error:
        print(f'Cannot extract fill_form JSON, error: {error}')
        return None
  # Default behavior
  pattern = r'\{.*?\}'
  match = re.search(pattern, s)
  if match:
    try:
      return ast.literal_eval(match.group())
    except (SyntaxError, ValueError) as error:
      try:
        return json.loads(match.group())
      except (SyntaxError, ValueError) as error2:
        print(
            'Cannot extract JSON, skipping due to errors %s and %s',
            error,
            error2,
        )
        return None
  else:
    return None
