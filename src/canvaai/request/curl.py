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


import json
from curl_cffi.requests import Session as Ses, Response
from typing import Any, Dict
from canvaai.logger import err


class Session:
    session: Ses[Response]
    headers: Dict[str, str]

    def __init__(self):
        self.session = Ses()
        self.headers = {
            "authority": "www.canva.com",
            "accept": "*/*",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7,ru;q=0.6",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "priority": "u=1, i",
            "Referer": "https://www.canva.com/ai/code",
            # "referer": "https://www.canva.com/ai/code/thread/[CHAT_ID]",
            "sec-ch-ua": '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-ch-ua-platform-version": '"10.0.0"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
            "x-canva-app": "home",
        }
    
    # Set chatid for headers
    def set_chat_id(self, chat_id: str) -> None:
      self.headers["referer"] = self.headers["referer"].replace("[CHAT_ID]", chat_id)
      
    # Set cookie
    def set_cookie(self, cookies: str) -> None:
      self.headers["cookie"] = cookies
    
    def merge_headers(self, headers: Dict[str, str]) -> None:
        self.headers.update(headers)

    # Get Response
    def get(self, url: str, headers: Dict[str, str] | None = None, **kwargs: Any) -> Response | None:
        try:
            req = self.session.get(url, headers=headers if headers else self.headers, impersonate="chrome110", **kwargs)
            return req
        except Exception as e:
            err(e)
            return None

    # Get Response ( POST )
    def post(self, url: str, data: Any, headers: Dict[str, str] | None = None, **kwargs: Any) -> Response | None:
        try:
            req = self.session.post(url, data=data, headers=headers if headers else self.headers, impersonate="chrome110", **kwargs)
            return req
        except Exception as e:
            err(e)
            return None

    # Get Response JSON
    def get_json(self, url: str, headers: Dict[str, str] | None = None, **kwargs: Any) -> Dict[str, Any]:
        """
        This function is used to
        convert text output into JSON format.

        API response:
          '"])}while(1);</x>//...(json format) <- Get JSON response
        """
        
        try:
            req = self.session.get(url, headers=headers if headers else self.headers, impersonate="chrome110", **kwargs)
            raw = req.text
            json_part = raw[raw.find("{") :]
            data = json.loads(json_part)
            return data
        except Exception as e:
            err(e)
            return {}

    # Get Response JSON
    def  post_json(self, url: str, data: Any, headers: Dict[str, str] | None = None, **kwargs: Any) -> Dict[str, Any]:
        """
        This function is used to
        convert text output into JSON format.

        API response:
          '"])}while(1);</x>//...(json format) <- Get JSON response
        """
        
        try:
            req = self.session.post(url, data=data, headers=headers if headers else self.headers, impersonate="chrome110", **kwargs)
            raw = req.text
            json_part = raw[raw.find("{") :]
            data = json.loads(json_part)
            return data
        except Exception as e:
            err(e)
            return {}
