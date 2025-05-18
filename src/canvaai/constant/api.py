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


from typing import Dict

# x-canva-request header map
REQUEST_MAP: Dict[str, str] = {
    "csrf": "createthread",
    "thread": "createthread",
    "follow": "getthread",
}

# Get cookie
BASE: str = "https://www.canva.com/ai/code"

# Get csrf
CSRF: str = "https://www.canva.com/_ajax/csrf3/assistant"

# Start chat
THREADS: str = "https://www.canva.com/_ajax/assistant/threads"

# Get headers:
#   x-canva-active-user
CANVA: str = "https://www.canva.com/"

# Chatting
# [CHAT_ID, AFTER_MESSAGE, UPDATE_FRAGMENT]
GET_CHAT: str = (
    "https://www.canva.com/_ajax/assistant/threads/[CHAT_ID]?afterMessageSeq=[AFTER_MESSAGE]&updateFragmentsOffset=[UPDATE_FRAGMENT]"
)
