# HTTP Concepts

## Introduction

HTTP forms the foundation of any API request. Specifically, RESTful APIs rely on HTTP 1.1, while gRPC is built on top of HTTP 2.0. Therefore, understanding key HTTP concepts, particularly HTTP methods and responses, is crucial for designing robust APIs.

## HTTP Methods

API requests utilize standard HTTP methods to perform CRUD (Create, Read, Update, Delete) operations on resources. The mapping between CRUD operations and HTTP methods, along with their purpose and usage, is as follows:

| HTTP Method | Operation      | Purpose                                            | Usage                                                                   |
| ----------- | -------------- | -------------------------------------------------- | ----------------------------------------------------------------------- |
| `POST`      | Create         | Create a new resource                              | Adding a new entry to a database or creating a new user account         |
| `GET`       | Read           | Retrieve data from the server                      | Fetching data, such as retrieving a list of users or a specific user    |
| `PUT`       | Update         | Update an existing resource or create if not exist | Updating a resource with new data, such as a user's profile information |
| `DELETE`    | Delete         | Delete a resource from the server                  | Removing a resource, such as deleting a user account                    |
| `PATCH`     | Partial Update | Apply partial modifications to a resource          | Updating specific fields of a resource, like a user's email address     |

## HTTP Status Codes

HTTP responses include status codes that provide information about the result of the request. These status codes are three-digit numbers and can be grouped into five categories: `1XX`, `2XX`, `3XX`, `4XX`, and `5XX`.

<div style="background: #d9edf7; padding: 10px; border: 2px solid #bcdff1; display: flex; align-items: center; height: 50px; border-radius: 5px;">
  <p style="margin: 0; font-size: 18px; font-weight: bold; color: #31708f;">🛈 Informational Responses (1XX)</p>
</div>

The `1XX` status codes indicate informational responses. They are rarely used in API development. Examples include:

-   `100 Continue`: The initial part of a request has been received, and the client should continue with the request.
-   `101 Switching Protocols`: The server is switching protocols as requested by the client, such as from HTTP to WebSocket.

<div style="background: #d4edda; padding: 10px; border: 2px solid #c3e6cb; display: flex; align-items: center; height: 50px; border-radius: 5px;">
  <p style="margin: 0; font-size: 18px; font-weight: bold; color: #155724;">✅ Successful Responses (2XX)</p>
</div>

The `2XX` status codes indicate that the request was successfully processed by the server.

-   `200 OK`: The request was successful. This is the most general success code, indicating that the request was received, understood, and accepted. It is used for a wide range of successful interactions, such as retrieving data with a `GET` request or submitting data with a `POST` request. The response body typically contains the requested data or confirmation of the action performed.
-   `201 Created`: The request was successful, and a new resource was created. POST requests to create resources should return a `201` status code.
-   `204 No Content`: The request was successful, but there is no content to send back (commonly used for DELETE operations).

<div style="background: #fff3cd; padding: 10px; border: 2px solid #ffeeba; display: flex; align-items: center; height: 50px; border-radius: 5px;">
  <p style="margin: 0; font-size: 18px; font-weight: bold; color: #856404;">🔀 Redirection Messages (3XX)</p>
</div>

The `3XX` status codes indicate that further action needs to be taken by the client to complete the request, usually involving redirection.

-   `301 Moved Permanently`: The resource has been permanently moved to a new URL. This status code indicates that the requested resource has been assigned a new permanent URI, and future references should use this URI.
-   `302 Found`: The resource is temporarily located at a different URL. This status code indicates that the requested resource resides temporarily under a different URI.
-   `304 Not Modified`: The resource has not been modified since the last request (used for caching). This status code tells the client that the response has not been modified, so the client can continue to use the same cached version of the response.
-   `307 Temporary Redirect`: The request should be repeated with another URL, but the method and the body of the original request must be used. Unlike `302`, `307` guarantees that the method used in the original request (e.g., POST) will not be changed to GET.

> [!IMPORTANT]
> Understanding client and server error codes is essential for good API design. Handling some exceptions is necessary, while handling all is unrealistic.

<div style="background: #f8d7da; padding: 10px; border: 2px solid #f5c6cb; display: flex; align-items: center; height: 50px; border-radius: 5px;">
  <p style="margin: 0; font-size: 18px; font-weight: bold; color: #d6336c;">⛔ Client Error Responses (4XX)</p>
</div>

The `4XX` status codes indicate client-side errors.

-   `400 Bad Request`: General error message indicating that the request could not be understood or was missing required parameters. This status code is used when the server cannot process the request due to client error (e.g., malformed request syntax).
-   `401 Unauthorized`: The client must authenticate itself to get the requested response (e.g., missing API key). This status code indicates that the request has not been applied because it lacks valid authentication credentials for the target resource.
-   `403 Forbidden`: The client does not have access rights to the content (e.g., insufficient permissions). This status code indicates that the server understands the request but refuses to authorize it.
-   `404 Not Found`: The server could not find the requested resource. This status code indicates that the server cannot find the requested resource.
-   `408 Request Timeout`: The server timed out waiting for the request. This status code indicates that the server did not receive a complete request message within the time that it was prepared to wait.
-   `429 Too Many Requests`: The user has sent too many requests in a given amount of time (rate limiting). This status code indicates that the user has sent too many requests in a given amount of time.

<div style="background: #f8d7da; padding: 10px; border: 2px solid #f5c6cb; display: flex; align-items: center; height: 50px; border-radius: 5px;">
  <p style="margin: 0; font-size: 18px; font-weight: bold; color: #721c24;">⚠ Server Error Responses (5XX)</p>
</div>

The `5XX` status codes indicate server-side errors.

-   `500 Internal Server Error`: The server encountered an unexpected condition that prevented it from fulfilling the request. This status code indicates that the server encountered an unexpected condition that prevented it from fulfilling the request.
-   `502 Bad Gateway`: The server received an invalid response from the upstream server. This status code indicates that the server, while acting as a gateway or proxy, received an invalid response from an inbound server.
-   `503 Service Unavailable`: The server is not ready to handle the request, often due to maintenance or overload. This status code indicates that the server is currently unable to handle the request due to temporary overloading or maintenance of the server.

For further read, you can check the following links:

-   [HTTP Status Codes - RESTAPI Tutorial](https://www.restapitutorial.com/httpstatuscodes)
-   [Every Important HTTP Status Code Explained](https://blog.webdevsimplified.com/2022-12/http-status-codes/)
-   [HTTP response status codes - Mozilla](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)
