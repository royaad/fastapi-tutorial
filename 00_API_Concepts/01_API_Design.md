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

What is idempotency... give the definition

do a table of the below
POST resquests are not idempotent.
GET is idempotent by default
PUT is idempotent
PATCH not idempotetnt
Delete is idempotent

to ensure it will require a unique request that will be sent in order to insure that the request will not be repeated. it requires some addtional checks...

My company's software routes orders to a dozen different print companies that print and ship physical goods. I've had this exact conversation, word-for-word, with different tech teams:

> Jeff: How can I ensure that I don't submit duplicate orders?
>
> Print company: Can't you just only submit the order once?

Sigh. No, I'm afraid I cannot. The quick example I always send back is this one:

1. I submit the order
2. The network fails and I get a timeout instead of 200 OK
3. I don't know if the order succeeded or failed

But I need a more detailed answer that I can point people at, so here it goes. If you work for a print company and I sent you here, please don't take it personally! You are not alone.

### A Brief Primer On Idempotence

[](<https://github.com/stickfigure/blog/wiki/How-to-(and-how-not-to)-design-REST-APIs#a-brief-primer-on-idempotence>)

**Idempotence** is the property of an operation such that if you execute it more than once, it doesn't change the result. You already expect `GET`, `PUT`, and `DELETE` operations to be idempotent:

```

# GET doesn't change anything on the server

GET /orders/ORD123

# If you call PUT on the same order more than once, the zip stays the same

PUT /orders/ORD123/address
{"zip": "91202"}

# If you call DELETE multiple times, the order stays deleted

DELETE /orders/ORD123

```

Create operations, usually associated with `POST`, are different. Without special handling, they are *not* idempotent.

```

# Every time you call this, we create a new order

POST /orders
{"product": "frisbee", "address": {...etc...}}

```

Because the network is not reliable, we suffer from the [Two General's Problem](https://en.wikipedia.org/wiki/Two_Generals%27_Problem). If an error occurs, there's no way for the client to know whether or not the operation successfully completed on the server. If the client submits the order again, we may create duplicate orders ("at-least-once"). If the client does not re-submit the order, we may lose orders ("at-most-once").

To get exactly-once behavior for non-idempotent operations, we need additional coordination between the client and server. There are generally two good ways and one crappy way to support this.

#### Good option: An "idempotency key" or "client reference ID"

[](<https://github.com/stickfigure/blog/wiki/How-to-(and-how-not-to)-design-REST-APIs#good-option-an-idempotency-key-or-client-reference-id>)

Let the client submit a unique value with the POST, and enforce uniqueness of this value on the server. [Stripe](https://stripe.com/docs/api/idempotent_requests) works this way, using a header. They store the idempotency key for 24 hours, giving you 24 hours of protection against duplication:

```

POST /v1/customers
Idemptency-Key: blahblahblahblah
{"name":"Bob Dobbs"}

```

Similarly, many order processing systems allow clients to submit a "customer reference ID" which is persisted with each order and included in customer reports. Enforcing uniqueness of this value protects against duplicate orders in perpetuity.

Make sure the key/id is a string - see Rule #6.

#### Good option: Let the client pick IDs

[](<https://github.com/stickfigure/blog/wiki/How-to-(and-how-not-to)-design-REST-APIs#good-option-let-the-client-pick-ids>)

If the client needs to pick a unique idempotency key for each submission, why not just make that the ID?

```

# Client picks the id

POST /things
{"id": "mything1"}

# The id can now be used

GET /things/mything1

```

This can result in simple, ergonomic APIs - though it adds implementation complexity in multitenant systems (where the ID must be uniqued to each tenant).

#### Crappy option: Provide an endpoint to list recent transactions

[](<https://github.com/stickfigure/blog/wiki/How-to-(and-how-not-to)-design-REST-APIs#crappy-option-provide-an-endpoint-to-list-recent-transactions>)

This is a workaround for client developers if the API doesn't offer any explicit help with idempotence:

1. Before *every* submission, fetch a list of recent transactions from the server.
2. Look for an existing transaction that matches your intended submission (hopefully you have a client reference ID to match).

For this to work, the client must serialize all create operations - otherwise there is a race condition. It's slow, and maintaining an N hour safety window means fetching N hours of transactions - potentially prohibitive on a busy system. But if you're building a client and the API doesn't provide another idempotence mechanism, this is what you have to do.

### When a conflict occurs...

[](<https://github.com/stickfigure/blog/wiki/How-to-(and-how-not-to)-design-REST-APIs#when-a-conflict-occurs>)

Now that your API offers a (good) idempotence mechanism, there's one more major consideration: How do you inform the client that there's a conflict? There are two main schools of thought:

#### Return an error

[](<https://github.com/stickfigure/blog/wiki/How-to-(and-how-not-to)-design-REST-APIs#return-an-error>)

When a client submits a duplicate idempotency key, I like to return 409 CONFLICT. There is one trick here - unless you're using user-submitted IDs ("Let the client pick IDs"), you need to include the existing ID in the error message or otherwise provide a mechanism to lookup the ID by idempotency key.

```

POST /things
{"idempotency_key": "blahblahblah", ...etc...}

# Response 409 CONFLICT

{"message": "This is a duplicate", old_id": "THG1234"}

```

When the client gets a 409 CONFLICT response, it says "oh, already done" and records the created ID. Just like it would have if the first POST returned without error.

#### Return the earlier response

[](<https://github.com/stickfigure/blog/wiki/How-to-(and-how-not-to)-design-REST-APIs#return-the-earlier-response>)

Instead of returning an error to the client, give them back the exact response that the client should have gotten the first time.

This allows clients to be a little dumber since they don't have to explicitly code up a CONFLICT error handler. However, it significantly complicates server implementation: You need to store all responses for a period of time and you need to validate that the client sent the exact same parameters with each request.

Stripe chose this route. I personally never have; it's a *lot* of sever work for just a little client convenience.

### TL;DR

[](<https://github.com/stickfigure/blog/wiki/How-to-(and-how-not-to)-design-REST-APIs#tldr>)

There are a few ways of enabling idempotent behavior for non-idempotent operations. As long as you pick *something*, your clients will be happy. If you don't want to think about it too hard, go with this solution:

-   Have the client submit an idempotency key (aka "customer reference ID") with each POST/create operation
-   Store it in the database with a unique constraint
-   Return 409 CONFLICT when you violate the unique constraint
-   Provide the original ID in the 409 response body

## Further Readings

1. [How to (and how not to) design REST APIs-design-REST-APIs](<https://github.com/stickfigure/blog/wiki/How-to-(and-how-not-to)-design-REST-APIs>)
2. [REST API Design - YouTube Video](https://www.youtube.com/watch?v=_gQaygjm_hg&list=PL53DoAIBJrduh8azUQKPFrxOPjAktLnSd&index=6)
3. [Best Practices in API Design](https://swagger.io/resources/articles/best-practices-in-api-design/)
