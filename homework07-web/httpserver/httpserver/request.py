import dataclasses
import http.client
import typing as tp


@dataclasses.dataclass
class HTTPRequest:
    method: bytes
    url: bytes
    headers: tp.Dict[bytes, bytes]
    body: bytes