from starlette.types import ASGIApp, Message, Receive, Scope, Send


class RequestSizeLimitMiddleware:
    def __init__(
        self,
        app: ASGIApp,
        max_body_size: int,
        path: str = "/api/contact",
    ) -> None:
        self.app = app
        self.max_body_size = max_body_size
        self.path = path

    async def __call__(
        self,
        scope: Scope,
        receive: Receive,
        send: Send,
    ) -> None:
        if scope["type"] != "http" or scope.get("path") != self.path:
            await self.app(scope, receive, send)
            return

        headers = dict(scope.get("headers", []))
        content_length = headers.get(b"content-length")

        if content_length is not None:
            try:
                if int(content_length) > self.max_body_size:
                    await self._send_too_large(send)
                    return
            except ValueError:
                pass

        buffered_messages: list[Message] = []
        total_size = 0

        while True:
            message = await receive()
            buffered_messages.append(message)

            if message["type"] == "http.disconnect":
                return

            if message["type"] == "http.request":
                total_size += len(message.get("body", b""))

                if total_size > self.max_body_size:
                    await self._send_too_large(send)
                    return

                if not message.get("more_body", False):
                    break

        async def replay_receive() -> Message:
            if buffered_messages:
                return buffered_messages.pop(0)

            return {
                "type": "http.request",
                "body": b"",
                "more_body": False,
            }

        await self.app(scope, replay_receive, send)

    @staticmethod
    async def _send_too_large(send: Send) -> None:
        body = b'{"detail":"Request body too large"}'

        await send(
            {
                "type": "http.response.start",
                "status": 413,
                "headers": [
                    (b"content-type", b"application/json"),
                    (b"content-length", str(len(body)).encode()),
                ],
            }
        )
        await send(
            {
                "type": "http.response.body",
                "body": body,
            }
        )