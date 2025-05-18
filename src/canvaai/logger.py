# -----------------------------------------------------------------------------
# Copyright (c) 2025 SyntxFlow
# This file is part of CanvaAI.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# See <https://www.gnu.org/licenses/> for more details.
# -----------------------------------------------------------------------------


from typing import Any
from canvaai.constant.colors import RED, RESET


def err(text: Any) -> None:
    print(f"{RESET}[ {RED}ERROR {RESET}] {RED}{text}{RESET}")
