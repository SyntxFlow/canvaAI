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


import re, json, base64
from canvaai.constant import api
from canvaai.request.curl import Session
from canvaai.logger import err
from curl_cffi.requests import Response
from typing import cast, Dict


# Get CSRF header token
# example output:
# {
#   'A': 'wMH4S-YkR2SlgP-x6A2TfoD0V6ygxmTCcZMD-W-5U7pgyj7IqMgucirDenScyIvdAssroWNSQLdHz6D20wBKHhEQac5execkMPti0YuZJDsK3FiQ',
#   'B': 1747552739645
# }
def get_csrf_token(session: Session) -> str:
    try:
        res = session.get_json(
            api.CSRF, {**session.headers, "x-canva-request": api.REQUEST_MAP["csrf"]}
        )
        return res["A"]
    except Exception as e:
        err(e)
        return ""


# Get headers:
#   x-canva-active-user
#   x-canva-analytics
#   x-canva-authz
#   x-canva-brand
#   x-canva-build-name
#   x-canva-build-sha
#   x-canva-locale
#   x-canva-user
def get_canva_headers(session: Session) -> Dict[str, str]:
    """
    How does it work?
    First, we take and parse the javascript object on the page.
    ex:
       1. window['bootstrap'] = JSON.parse('{"base"... <- first regex
       2. "T":{"A?":"A","E":true,"F":1000,"G":20,"...  <- second regex
       3. "a":{"A":"AAQAA1dFQgABAB...

    Then, we change it to JSON format.
    Finally, we take the required parts.
    ex:
      {'A': 'UAGSjaT-GxI', 'B': 'BAGSjSm-a8g'}              <- before encode with base64
      eyJBIjoiVUFHU2phVC1HeEkiLCJCIjoiQkFHU2pTbS1hOGcifQ==  <- after encode
    """

    try:
        reg_flags = re.compile(r"window\[\'bootstrap\'\]\s=\sJSON.parse\(\'(.*\})\'\);")
        reg_T = re.compile(r"\"T\":(\{.*\,\"i\"\:\"web\"\})\,\"U\"")
        reg_a = re.compile(r"\"a\":(\{.*\}\})\,\"d\"\:")

        res = session.get(api.CANVA)
        flags = reg_flags.search(cast(Response, res).text)
        if flags:
            t_obj = reg_T.search(flags.group(1))
            a_obj = reg_a.search(flags.group(1))
            if t_obj and a_obj:
                json_dec = json.loads(t_obj.group(1))
                json_dec2 = json.loads(a_obj.group(1))
                return {
                    "x-canva-active-user": base64.b64encode(
                        json.dumps({"A": json_dec["N"], "B": json_dec["D"]}).encode()
                    ).decode(),
                    "x-canva-analytics": json_dec2["A"],
                    "x-canva-authz": json_dec2["C"],
                    "x-canva-brand": json_dec["D"],
                    "x-canva-build-name": json_dec2["E"],
                    "x-canva-build-sha": json_dec2["F"],
                    "x-canva-locale": json_dec2["J"],
                    "x-canva-user": json_dec["N"],
                }
            else:
                return {}
        else:
            return {}
    except Exception as e:
        err(e)
        return {}
