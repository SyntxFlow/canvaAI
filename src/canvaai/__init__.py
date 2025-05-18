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


import sys, string, random, time
from canvaai.logger import err
from canvaai.request.curl import Session
from canvaai.constant import api
from canvaai.constant.colors import GREEN, RESET
from http.cookiejar import MozillaCookieJar
from typing import Dict, Any, Iterator


# Save response with custom filename
def save_response_to_file(response: str) -> None:
    save = str(input(f"\r\n[ {GREEN}#{RESET} ] Filename ( with ext ) : "))
    if save == "":
        while save == "":
            save = str(input(f"\r\n[ {GREEN}#{RESET} ] Filename ( with ext ) : "))
    else:
        with open(save, "w") as wr:
            wr.write(response)
        print(f"[ {GREEN}@{RESET} ] Response save to {save}")

# Parsing response JSON
def get_answer(session: Session, ress: Dict[str, Any]) -> Iterator[str]:
    answer_len = 0
    # res2 = session.get_json(
    #     api.GET_CHAT.replace("[CHAT_ID]", ress["A"])
    #     .replace("[AFTER_MESSAGE]", "0" if answer_len == 0 else "2")
    #     .replace("[UPDATE_FRAGMENT]", str(answer_len)),
    #     headers={
    #         **session.headers,
    #         "content-type": "application/json;charset=UTF-8",
    #         "x-canva-request": api.REQUEST_MAP["follow"],
    #     },
    # )
    # if len(res2["f"]) != 0 and res2["f"][len(res2["f"]) - 1]["U"]:
    #     print(json.dumps(res2, indent=2))
    #     answer = ""
    #     for asn in res2.get("f", []):
    #         last_u = asn["U"]
    #         answer += last_u.get("D") or last_u.get("A")

    #     # sys.stdout.write(f"\r{answer}")
    #     yield answer
    #     answer_len += 1 if answer_len == 0 else 5
        
    while True:
        res2 = session.get_json(
            api.GET_CHAT.replace("[CHAT_ID]", ress["A"])
            .replace("[AFTER_MESSAGE]", "0" if answer_len == 0 else "2")
            .replace("[UPDATE_FRAGMENT]", str(answer_len)),
            headers={
                **session.headers,
                "content-type": "application/json;charset=UTF-8",
                "x-canva-request": api.REQUEST_MAP["follow"],
            },
        )
        if len(res2["f"]) != 0 and res2["f"][len(res2["f"]) - 1]["U"]:
            # print(json.dumps(res2, indent=2))
            answer = "".join(
                entry["U"].get("D") or entry["U"].get("A")
                for entry in res2["f"]
            )

            # sys.stdout.write(f"\r{answer}")
            yield answer
            # answer_len += 1 if answer_len == 0 else 5
            
        if (res2.get("A") != []):
            break
        
        time.sleep(2)

# Random uppercase
def random_uppercase(length: int) -> str:
    res = ""
    uppercase = string.ascii_uppercase
    for _ in range(length):
        rnd = random.randint(0, len(uppercase) - 1)
        res += uppercase[rnd]
    return res


# Change netscape format to string header
def netscape_to_string(file_path: str) -> str:
    jar = MozillaCookieJar()
    jar.load(file_path, ignore_discard=True, ignore_expires=True)
    cookie_dict = {cookie.name: cookie.value for cookie in jar}
    return "; ".join(f"{k}={v}" for k, v in cookie_dict.items())


# Get args value
def get_arg(name: str) -> str:
    try:
        args = sys.argv
        find_index = args.index(name)
        return args[find_index + 1]
    except Exception:
        err(
            "\nPlease log in to your Canva account and include your Canva cookies by specifying the --cookies argument.\nex:\n --cookies cookies.txt"
        )
        exit(1)


# Get cookie
# def set_canva_cookie(session: Session) -> None:
#     """
#     To overcome the problem of the
#     set-cookie header not appearing
#     when making a request, we use
#     the allow_redirects=False option
#     so that it limits redirects to 0.
#     """

#     try:
#         session.get(api.BASE, None, allow_redirects=False)
#     except Exception as e:
#         err(e)
