import dataclasses
import io
import typing as tp

from httpserver import HTTPRequest


@dataclasses.dataclass
class WSGIRequest(HTTPRequest):
    def to_environ(self) -> tp.Dict[str, tp.Any]:
        query_string = ""
        url_split = self.url.decode("utf-8").split("?")
        if len(url_split) > 1:
            query_string = url_split[1]

        environ = {
            # WSGI
            "wsgi.version": (1, 0),
            "wsgi.url_scheme": "http",
            "wsgi.input": io.BytesIO(self.body),
            # CGI
            "CONTENT_TYPE": self.headers.get(b"Content-Type", b"").decode("utf-8"),
            "CONTENT_LENGTH": self.headers.get(b"Content-Length", b"").decode("utf-8"),
            "REQUEST_METHOD": self.method.decode("utf-8"),
            "PATH_INFO": self.url.decode("utf-8"),
            "QUERY_STRING": query_string,
            "SCRIPT_NAME": "",  # accordingly to the https://www.python.org/dev/peps/pep-0333/#environ-variables
            # HTTP_Variables - переменные соответствующие заголовкам запроса переданным клиентом
        }
        return environ
