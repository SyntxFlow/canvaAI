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


import sys, os, json, uuid
from canvaai.request.curl import Session
from canvaai.constant import api
from typing import Any, Dict
from canvaai.request.token import get_canva_headers, get_csrf_token
from canvaai.constant.colors import GREEN, RESET, RED, CYAN
from canvaai import (
    get_arg,
    netscape_to_string,
    random_uppercase,
    get_answer,
    save_response_to_file,
)

# from typing import cast

# Init
session: Session = Session()

# Add cookie to header
cookie_str = netscape_to_string(get_arg("--cookies"))
session.set_cookie(cookie_str)


# Clear terminal
def clear() -> None:
    if "win" in sys.platform:
        os.system("cls")
    else:
        os.system("clear")


# Main function
def main() -> None:
    try:
        clear()
        print(
            f"""{GREEN}
  /$$$$$$                                                 /$$$$$$  /$$$$$$
 /$$__  $$                                               /$$__  $$|_  $$_/
| $$  \\__/  /$$$$$$  /$$$$$$$  /$$    /$$ /$$$$$$       | $$  \\ $$  | $$  
| $$       |____  $$| $$__  $$|  $$  /$$/|____  $$      | $$$$$$$$  | $$  
| $$        /$$$$$$$| $$  \\ $$ \\  $$/$$/  /$$$$$$$      | $$__  $$  | $$  
| $$    $$ /$$__  $$| $$  | $$  \\  $$$/  /$$__  $$      | $$  | $$  | $$  
|  $$$$$$/|  $$$$$$$| $$  | $$   \\  $/  |  $$$$$$$      | $$  | $$ /$$$$$$
\\______/  \\_______/|__/  |__/    \\_/    \\_______/      |__/  |__/|______/{RESET}
                                                            
########################################################################
##       Author: SyntxFlow   |   Github: github.com/SyntxFlow         ##
########################################################################

[ CHOOSE MENU ]                                    [ {RED}CTRL + C for exit{RESET} ]
[ {CYAN}01{RESET} ]. General chat ( {GREEN}Cooming soon{RESET} )
[ {CYAN}02{RESET} ]. Generate image ( {GREEN}Cooming soon{RESET} )
[ {CYAN}03{RESET} ]. Code generation
[ {RED}00{RESET} ]. Quit
  """
        )
        ins = str(input("[ # ] Menu : ")).strip()
        if ins == "":
            main()
        elif ins in ["01", "1"]:
            print(f"[ {GREEN}SOON{RESET} ] Comming soon!")
            exit(1)
        elif ins in ["02", "2"]:
            print(f"[ {GREEN}SOON{RESET} ] Comming soon!")
            exit(1)
        elif ins in ["03", "3"]:
            code_generator()
        else:
            main()
    except KeyboardInterrupt:
        exit(1)


# Code generator
def code_generator() -> None:
    while True:
        prompt = str(input(f"\r\n[ {GREEN}*{RESET} ] PROMPT : "))

        res = get_canva_headers(session)
        session.merge_headers(res)

        res = get_csrf_token(session)
        payload: Dict[str, Any] = {
            "A": random_uppercase(26),
            "B": [
                {
                    "A?": "A",
                    "A": prompt,
                }
            ],
            "C": str(uuid.uuid4()),
            "D": {"D": "I"},
            "F": "B",
        }
        ress = session.post_json(
            api.THREADS,
            json.dumps(payload),
            headers={
                **session.headers,
                "x-csrf-token": res,
                "content-type": "application/json;charset=UTF-8",
                "x-canva-request": api.REQUEST_MAP["thread"],
            },
        )
        # print(ress)

        answer = ""
        for chunk in get_answer(session, ress):
            answer = chunk
            sys.stdout.write(f"\r{chunk}")
            sys.stdout.flush()

        print("\r\n")
        save = str(input(f"\r\n[ {GREEN}#{RESET} ] Save response? [y/n] def y : "))
        if save == "":
            while save == "":
                save = str(
                    input(f"\r\n[ {GREEN}#{RESET} ] Save response? [y/n] def y : ")
                )
        elif save in ["y", "Y"]:
            save_response_to_file(answer)
            continue
        elif save in ["n", "N"]:
            continue
        else:
            continue


if __name__ == "__main__":
    main()
