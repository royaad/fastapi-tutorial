# Temporary Note

## Concepts

In FastAPI (and ASGI applications in general), `scope`, `receive`, and `send` are key components of the ASGI interface. Here's a breakdown of each:

1. **Scope**: This is a dictionary containing information about the connection. For HTTP requests, it includes details like the HTTP method, headers, path, query string, etc. Here's an example of what the `scope` might look like for an HTTP request:

    ```python
    {
        "type": "http",
        "http_version": "1.1",
        "method": "GET",
        "scheme": "http",
        "path": "/",
        "query_string": b"",
        "headers": [
            (b"host", b"localhost:8000"),
            (b"user-agent", b"curl/7.64.1"),
            (b"accept", b"*/*")
        ],
        "client": ("127.0.0.1", 12345),
        "server": ("127.0.0.1", 8000)
    }
    ```

2. **Receive**: This is an asynchronous callable that you use to receive messages from the client. For HTTP requests, you typically receive the request body in chunks. Here's an example of how you might use `receive`:

    ```python
    async def receive_body(receive):
        body = b""
        more_body = True
        while more_body:
            message = await receive()
            body += message.get("body", b"")
            more_body = message.get("more_body", False)
        return body
    ```

3. **Send**: This is an asynchronous callable that you use to send messages to the client. For HTTP responses, you send the response headers and body. Here's an example of how you might use `send`:

    ```python
    async def send_response(send, status_code, headers, body):
        await send({
            "type": "http.response.start",
            "status": status_code,
            "headers": headers
        })
        await send({
            "type": "http.response.body",
            "body": body
        })
    ```

    Putting it all together, here's a simple example of an ASGI application that echoes back the request body:

    ```python
    async def app(scope, receive, send):
        if scope["type"] == "http":
            body = await receive_body(receive)
            headers = [(b"content-type", b"text/plain")]
            await send_response(send, 200, headers, body)
    ```

This example demonstrates how `scope`, `receive`, and `send` work together to handle an HTTP request and response. If you have any more questions or need further clarification, feel free to ask!

## Batching

Let's ensure the middleware processes requests in a FIFO (First-In-First-Out) manner. Here's the updated version of the FastAPI app with FIFO batching:

1. **Install FastAPI and Uvicorn**:

    ```bash
    pip install fastapi uvicorn
    ```

2. **Create the FastAPI app**:

    ```python
    from fastapi import FastAPI, Request
    import asyncio
    from typing import List

    app = FastAPI()

    class BatchMiddleware:
        def __init__(self, app, max_batch_size: int, wait_time: float):
            self.app = app
            self.max_batch_size = max_batch_size
            self.wait_time = wait_time
            self.queue = []
            self.lock = asyncio.Lock()

        async def __call__(self, scope, receive, send):
            if scope["type"] == "http":
                request = Request(scope, receive)
                async with self.lock:
                    self.queue.append(request)
                    if len(self.queue) >= self.max_batch_size:
                        await self.process_batch()
                    else:
                        await asyncio.sleep(self.wait_time)
                        if self.queue:
                            await self.process_batch()
            await self.app(scope, receive, send)

        async def process_batch(self):
            async with self.lock:
                batch = self.queue[:self.max_batch_size]
                self.queue = self.queue[self.max_batch_size:]
            concatenated_text = await self.handle_batch(batch)
            for request in batch:
                response = {
                    "type": "http.response.start",
                    "status": 200,
                    "headers": [(b"content-type", b"application/json")]
                }
                await request.send(response)
                response_body = {
                    "type": "http.response.body",
                    "body": concatenated_text.encode('utf-8')
                }
                await request.send(response_body)

        async def handle_batch(self, batch: List[Request]):
            texts = []
            for request in batch:
                body = await request.body()
                texts.append(body.decode('utf-8'))
            concatenated_text = " ".join(texts)
            return concatenated_text

    app.add_middleware(BatchMiddleware, max_batch_size=10, wait_time=1.0)

    @app.post("/submit")
    async def submit_text(request: Request):
        return {"message": "Request received"}

    if __name__ == "__main__":
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=8000)
    ```

In this updated version:

-   The middleware ensures that requests are processed in the order they are received (FIFO).
-   The `process_batch` method processes the oldest requests first by slicing the queue from the start.

Feel free to test this out and let me know if you need any further adjustments or have any questions!
