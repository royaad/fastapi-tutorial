# API Design

## Introduction

In the [[00_HTTP_Concepts|previous document]] we talked about URL and HTTP which play a crucial rule in api design. in the following we will discuss on the best practices to design a clean and pragmatic API.

## Richardson Maturity Model

Before we delve into more details, let's take a look at the Richardson Maturity Model, a framework for evaluating the maturity of web services based on their adherence to RESTful principles. Developed by Leonard Richardson, this model consists of four levels, each representing a step towards a more RESTful design.

Below is an illustrative table summarizing the levels of the Richardson Maturity Model:

<div style="display: flex; justify-content: center; flex-direction: column; align-items: center;">
  <p style="font-family: 'Copperplate', sans-serif; font-weight: bold; font-size: 20px">Richardson Maturity Model</p>
  <table style="border-collapse: collapse; font-family: Tahoma, sans-serif; font-size: 18px;">
    <tr>
      <td style="border: none; background: linear-gradient(to right, #4CAF50, #81C784); border-radius: 7px; padding: 10px; color: white; text-align: center; width: 90px; font-weight: bold;">Level 3</td>
      <td style="border: none; text-align: left; vertical-align: middle; padding-left: 10px;">Hypermedia Controls</td>
    </tr>
    <tr>
      <td colspan="2" style="border: none; height: 10px;"></td>
    </tr>
    <tr>
      <td style="border: none; background: linear-gradient(to right, #2196F3, #64B5F6); border-radius: 7px; padding: 10px; color: white; text-align: center; width: 90px; font-weight: bold;">Level 2</td>
      <td style="border: none; text-align: left; vertical-align: middle; padding-left: 10px;">HTTP Verbs</td>
    </tr>
    <tr>
      <td colspan="2" style="border: none; height: 10px;"></td>
    </tr>
    <tr>
      <td style="border: none; background: linear-gradient(to right, #FF9800, #FFB74D); border-radius: 7px; padding: 10px; color: white; text-align: center; width: 90px; font-weight: bold;">Level 1</td>
      <td style="border: none; text-align: left; vertical-align: middle; padding-left: 10px;">Resources</td>
    </tr>
    <tr>
      <td colspan="2" style="border: none; height: 10px;"></td>
    </tr>
    <tr>
      <td style="border: none; background: linear-gradient(to right, #F44336, #E57373); border-radius: 7px; padding: 10px; color: white; text-align: center; width: 90px; font-weight: bold;">Level 0</td>
      <td style="border: none; text-align: left; vertical-align: middle; padding-left: 10px;">Swamp of POX</td>
    </tr>
  </table>
</div>

### Level 0: The Swamp of POX

At this level, services use a single URI and a single HTTP method (typically POST). This is the most basic form of service-oriented architecture, often using XML or JSON for communication but not leveraging the full capabilities of HTTP.

### Level 1: Resources

Services at this level introduce the use of URIs to identify resources. Each resource is represented by a unique URI, but interactions still typically use a single HTTP method. This level improves upon Level 0 by providing a more structured way to access different resources.

### Level 2: HTTP Verbs

Level 2 services make use of both URIs and HTTP methods (GET, POST, PUT, DELETE, etc.). This allows for a more expressive and standardized way to interact with resources, aligning more closely with RESTful principles.

### Level 3: Hypermedia Controls (HATEOAS)

The highest level of maturity, Level 3, incorporates **H**ypermedia **A**s **T**he **E**ngine **O**f **A**pplication **S**tate (HATEOAS). This means that responses include links to related resources, allowing clients to navigate the API dynamically. This level fully embraces RESTful principles, making the API more flexible and discoverable.

However, achieving Level 3 is challenging due to its computational demands and low adoption within the community. As a result, Level 2 is often considered the most desirable level for API design, balancing expressiveness and practicality.

## API Design Best Practices

In this section, we will discuss best practices for designing APIs, divided into three main sub-sections:

1. **Naming Rules**: Guidelines for naming API endpoints.
2. **Response Rules**: Best practices for structuring API responses.
3. **Header Usage**: Recommendations for using headers for authentication, content negotiation, and idempotency.

### Naming Rules

This section outlines the rules for naming API endpoints, with good and bad examples provided for each rule.

#### Rule #1: Use Versions

Versioning your API allows for updates and backward compatibility without disrupting existing consumers.

```http
# GOOD
GET /v1/products

# BAD
GET /products
```

#### Rule #2: Use Plural Nouns

Resources are typically grouped in collections, so use plural nouns to indicate a collection rather than a single resource.

```http
# GOOD
GET /v1/products

# BAD
GET /v1/product
```

#### Rule #3: Use Hyphens (-) Instead of Underscores (\_)

Hyphens are preferred for readability and consistency.

```http
# GOOD
GET /v1/my-orders

# BAD
GET /v1/my_orders
```

#### Rule #4: Avoid Trailing Slashes (/)

Trailing slashes can cause confusion and inconsistency.

```http
# GOOD
GET /v1/products

# BAD
GET /v1/products/
```

#### Rule #5: Use Resources, Not Actions

The HTTP method already indicates the action, so use resource names to avoid redundancy.

```http
# GOOD
GET /products

# BAD
GET /get-products
```

However, for specific non-database-related operations, using an action can provide clarity:

```http
# GOOD
POST /v1/transcribe-audio

# BAD
POST /v1/audio
```

#### Rule #6: Maintain Hierarchical Relationships

Use slashes (/) to indicate hierarchical relationships. Avoid more than two levels of nesting to keep URLs manageable and maintainable.

```http
# GOOD
GET /v2/clients/{client_id}/orders
GET /v2/orders/{order_id}/items

# BAD
GET /v1/clients/{client_id}/orders/{order_id}/items
```

#### Rule #7: Use Clear Query Strings for Sorting and Filtering

Query parameters are best for filtering, sorting, paginating, and limiting results. Avoid using query parameters to filter higher-order collections.

```http
# GOOD
GET /v1/shops/{shop_id}/products?filter=color:blue&sort_by=price
GET /v1/cart/123/items

# BAD
GET /api/v1/items?cart_id=123
```

### Response Rules

#### Rule #1: Don't Return Arrays or Map Structures as Top-Level Responses

Returning arrays or map structures as top-level responses can lead to several issues, making it difficult to maintain and evolve your API. Here are the main reasons why this should be avoided:

##### Arrays

1. **Backward Compatibility**: Returning arrays makes it challenging to introduce backward-compatible changes. For example, adding pagination or metadata fields like `totalCount` or `hasMore` is straightforward with objects but problematic with arrays.
2. **Extensibility**: Objects allow for more flexible and extensible responses. You can add new fields without breaking existing clients.

```http
# GOOD
GET /things returns:
{ "data": [{ ...thing1...}, { ...thing2...}] }

# BAD
GET /things returns:
[{ ...thing1...}, { ...thing2...}]
```

##### Map Structures

1. **Redundancy**: Map structures often include redundant key information, adding unnecessary noise to the response.
2. **Typed Languages**: Dynamic keys in map structures can create challenges for developers working in typed languages.
3. **Key Changes**: Conceptual keys may change over time, leading to breaking changes and backward compatibility issues.

```http
# BAD
GET /things returns:
{
  "KEY1": { "id": "KEY1", "foo": "bar" },
  "KEY2": { "id": "KEY2", "foo": "baz" },
  "KEY3": { "id": "KEY3", "foo": "bat" }
}

# GOOD (also note application of Rule #1)
GET /things returns:
{
  "data": [
    { "id": "KEY1", "foo": "bar" },
    { "id": "KEY2", "foo": "baz" },
    { "id": "KEY3", "foo": "bat" }
  ]
}
```

##### Exception to the No-Map Rule

The exception to the no-map rule is simple key/value pairs, such as Stripe's metadata.

```http
# OK
{
  "key1": "value1",
  "key2": "value2"
}
```

#### Rule #2: Solid Error/Exception Handling

Effective error handling is essential for ensuring the stability, security, and usability of your API. Here are the best practices:

##### Catch the Exception

Anticipate potential failures and catch exceptions at appropriate points in your code to handle errors gracefully.

##### Provide a Clear Description

When an error occurs, provide a clear and meaningful description to help clients understand the issue.

##### Return Appropriate Status Codes

Use the correct [[00_HTTP_Concepts|HTTP status codes]] to indicate the nature of the error.

##### Use a Structured Error Format

Establish a standard error format for consistency and easier debugging:

```json
{
  "message": "You do not have permission to access this resource",
  "type": "Unauthorized",
  "types": ["Unauthorized", "Security"],
  "cause": { ...nested exceptions... }
}
```

This format allows for wrapping and re-throwing errors across multiple layers, providing a complete chain of the error's origin and context:

```plaintext
ServiceAlpha -> ServiceBravo -> ServiceCharlie -> ServiceDelta
```

If ServiceDelta raises an error, ServiceAlpha can return or log the complete chain, including the root cause. This approach simplifies debugging compared to searching through logs on multiple systems, even with centralized logging.

By following these best practices, you can ensure your API is robust, reliable, and provides a smooth user experience.

#### Rule #3: Implement Pagination in Responses

Pagination is a crucial aspect of API design, especially when dealing with large datasets. It helps improve performance, reduce resource usage, and enhance the user experience by delivering data in manageable chunks. Here are the best practices for implementing pagination in API responses:

##### Use Query Parameters

Use query parameters to control pagination. Common parameters include:

-   **limit**: The number of items to return per page.
-   **offset**: The starting point for the items to return.
-   **page**: The page number to return.
-   **cursor**: A unique identifier for the current position in the dataset.

```http
GET /v1/products?limit=10&offset=20
GET /v1/products?page=2
GET /v1/products?cursor=abc123
```

##### Include Pagination Metadata

Provide metadata in the response to help clients navigate through the paginated data. This metadata can include:

-   **totalItems**: The total number of items available.
-   **totalPages**: The total number of pages.
-   **currentPage**: The current page number.
-   **pageSize**: The number of items per page.
-   **nextPage**: The URL for the next page.
-   **prevPage**: The URL for the previous page.

```json
{
    "data": [
        { "id": 1, "name": "Product 1" },
        { "id": 2, "name": "Product 2" }
    ],
    "meta": {
        "totalItems": 100,
        "totalPages": 10,
        "currentPage": 2,
        "pageSize": 10,
        "nextPage": "/v1/products?page=3",
        "prevPage": "/v1/products?page=1"
    }
}
```

##### Use Link Headers

Include link headers in the response to provide URLs for navigating to other pages. This is particularly useful for clients that prefer to use headers for pagination.

```http
HTTP/1.1 200 OK
Content-Type: application/json
Link: <http://api.example.com/v1/products?page=1>; rel="first",
      <http://api.example.com/v1/products?page=2>; rel="prev",
      <http://api.example.com/v1/products?page=3>; rel="next",
      <http://api.example.com/v1/products?page=10>; rel="last"
```

##### Benefits of Pagination

1. **Improved Performance**: Retrieving and processing smaller chunks of data reduces response time and improves overall efficiency.
2. **Reduced Resource Usage**: Pagination minimizes memory, processing power, and bandwidth usage on both the server and client side.
3. **Enhanced User Experience**: Delivering data in manageable portions allows users to navigate through the data incrementally, providing a smoother interaction.

By following these best practices, you can ensure your API handles large datasets efficiently and provides a better experience for clients.

### Advanced Rules

#### Rule #1: Use Headers for Content Negotiation and Authorization

Using headers for content negotiation and authorization is a best practice that ensures flexibility and security in your API design.

##### Content Negotiation

URLs should serve as resource identifiers, not representations. Adding representation information (e.g., `.json`) to the URL can lead to issues with canonical URLs and client identification of resources. Instead, use HTTP headers for content negotiation:

-   **Accept**: Specifies the media types that are acceptable for the response.
-   **Accept-Charset**: Specifies the character sets that are acceptable.
-   **Accept-Encoding**: Specifies the content-coding values that are acceptable.
-   **Accept-Language**: Specifies the preferred languages for the response.

```http
# GOOD
GET /products
Accept: application/json

# BAD
GET /products.json
```

JSON should be the default response format. If clients need a different format, they can specify it using the appropriate headers.

##### Authorization

Use headers for authorization to maintain security and prevent exposure of sensitive information:

```http
# GOOD
GET /clients/{client_id}/orders
Authorization: Bearer <token>

# BAD
GET /clients/{token}/orders
```

Avoid placing authorization tokens in the URL path.

#### Rule #2: Use Strings for All Identifiers

Always use strings for object identifiers, even if your internal representation is numeric. This practice ensures flexibility and future-proofing. Using strings also allows for an easier switch between different types of identifiers, such as integers and UUIDs, without causing issues.

```json
# GOOD
{ "id": "123" }

# BAD
{ "id": 123 }
```

String IDs can encode version information, segment ID ranges, and handle composite keys. They also simplify client development in typed languages.

#### Rule #3: Prefix Your Identifiers

Prefixing identifiers makes them self-describing and easier to manage, especially in complex applications with multiple object types. Here are some generic examples:

```json
# GOOD
{ "order_id": "ord_12345" }
{ "user_id": "usr_67890" }

# BAD
{ "id": "12345" }
{ "id": "67890" }
```

Ensure that prefixes are visually distinct and consistent.

#### Rule #4: Use ISO 8601 Strings for Timestamps

Use ISO 8601 strings for timestamps to ensure human readability and standardization:

```json
"timestamp": "2023-12-21T11:17:12.34Z"
```

ISO 8601 is widely supported and avoids issues with multiple date/time formats. Always use UTC ("Z") for timestamps.

#### Rule #5: Provide Idempotence Mechanisms

Idempotency ensures that repeated operations produce the same result, enhancing reliability and preventing duplicate operations. Implement idempotency keys for non-idempotent methods like POST.

Idempotency is a significant topic, and we will dedicate the next section to discuss it in detail.

By following these advanced rules, you can create a robust, flexible, and user-friendly API.

## Idempotency

Idempotency in APIs ensures that performing an operation multiple times has the same effect as performing it once. This means that making the same API request multiple times will not change the result beyond the initial application.

Some HTTP methods are idempotent by default, while others are not. The table below summarizes the idempotency of common HTTP methods:

| HTTP Method | Idempotency |
| ----------- | ----------- |
| POST        | ❌          |
| GET         | ✅          |
| PUT         | ✅          |
| PATCH       | ❌          |
| DELETE      | ✅          |

To achieve exactly-once behavior for non-idempotent operations, additional coordination between the client and server is required. This typically involves using an idempotency key.

### Idempotency Key

Clients can submit a unique value with the POST request, and the server enforces the uniqueness of this value. The idempotency key can be sent in the header as `Idempotency-Key` or `X-Idempotency-Key`:

```http
POST /clients/{client_id}/orders
X-Idempotency-Key: FDH23AB5DHC
{"name":"Bob Dobbs"}
```

### Methods to Generate an Idempotency Key

1. **Hashing the Request Body**: Generate a hash of the request body to ensure that identical requests produce the same key.
2. **Combining User ID and Request Path**: Create a key by combining the user ID and the request path, ensuring uniqueness for each user and endpoint.
3. **Checking Time Between Requests**: Use timestamps to identify retries. If the same request is sent within a very short time frame (e.g., a few milliseconds), it is likely a retry.
4. **Using a Mixture of Random ID and Body Hash**: Combine a random ID with a hash of the request body to create a unique key that is resistant to collisions.
5. **UUID Generation**: Use universally unique identifiers (UUIDs) to generate idempotency keys. This method ensures a high degree of uniqueness and is commonly used in distributed systems.
6. **Client-Generated Keys**: Allow clients to generate their own idempotency keys and send them with requests. This approach gives clients control over key generation and can be useful in scenarios where client-side logic determines uniqueness.
7. **Server-Side Hashing**: Implement server-side hashing of request parameters to generate idempotency keys. This method can be combined with other techniques to enhance security and uniqueness.
8. **Structured Idempotency**: Use structured idempotency keys that include metadata such as user ID, timestamp, and request type. This approach is used by companies like Airbnb to ensure safe financial transactions.

### Storing

Store the idempotency key using a key-value store such as Redis. The key is stored along with the response before sending it to the client. The storage duration depends on the application and can range from 10 minutes to 48 hours, using TTL (time to live).

### Handling Conflicts

When a conflict occurs due to a duplicate idempotency key, there are two main approaches:

#### Return an Error

Return a 409 CONFLICT response, including the existing ID in the error message:

```http
# Response 409 CONFLICT
{"message": "This is a duplicate", "old_id": "THG1234"}
```

The client can then recognize the conflict and record the created ID.

#### Return the Earlier Response

Instead of returning an error, return the exact response that the client should have received the first time. This approach simplifies client implementation but requires the server to store all responses for a period and validate that the client sent the same parameters with each request.

## Further Readings

1. [How to (and how not to) design REST APIs-design-REST-APIs](<https://github.com/stickfigure/blog/wiki/How-to-(and-how-not-to)-design-REST-APIs>)
2. [REST API Design - YouTube Video](https://www.youtube.com/watch?v=_gQaygjm_hg&list=PL53DoAIBJrduh8azUQKPFrxOPjAktLnSd&index=6)
3. [Best Practices in API Design](https://swagger.io/resources/articles/best-practices-in-api-design/)
4. [Idempotency - What it is and How to Implement it?](https://www.alexhyett.com/idempotency/)
