"""HTTP transport policy shared by credential-bearing internal clients."""

from typing import Any
from urllib.request import HTTPRedirectHandler, Request


class NoRedirectHandler(HTTPRedirectHandler):
    """Keep service credentials and requests at their configured origin."""

    def redirect_request(
        self,
        req: Request,
        fp: Any,
        code: int,
        msg: str,
        headers: Any,
        newurl: str,
    ) -> None:
        return None
