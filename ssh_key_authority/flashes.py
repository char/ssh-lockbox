# Flask-esque flashes for Starlette. Requires session middleware.

from typing import List, Tuple

from starlette.requests import Request


def flash(request: Request, category: str, message: str):
    flashes = request.session.setdefault("flashes", [])
    flashes.append({"category": category, "message": message})


def get_flashes(request: Request) -> List[Tuple[str, str]]:
    flashes = request.session.get("flashes")
    if flashes is None:
        return []

    return [(flash["category"], flash["message"]) for flash in flashes]
