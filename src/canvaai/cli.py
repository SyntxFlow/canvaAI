import argparse

def tui():
    parser = argparse.ArgumentParser(
        prog="canvaai",
        description="CLI to interact with Canva AI terminal user interface"
    )
    parser.add_argument(
        "-c", "--cookies",
        help="To add cookies from a file, for example cookies.txt. with netscape format",
        required=True
    )

    args = parser.parse_args()

    if args.cookies:
        print(f"File cookies anda: {args.cookies}")
