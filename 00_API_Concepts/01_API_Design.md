# API Design

## Introduction

In the [[00_HTTP_Concepts|previous document]] we talked about URL structure which play a crucial rule in api design. in the following we will discuss on the best practices to design a clean and pragmatic API.


## Levels of design

## Naming endpoints rules

## Response Rules


everything else false under the categories above almost...

## Rule #1: DO use plural nouns for collections (group of resources)

## Use clear Naming

It's an arbitrary convention, but it's well-established and I have found violations tend to be a leading indicator of "this API will have rough edges".

```
# GOOD
GET /products              # get all the products
GET /products/{product_id} # get one product

# BAD
GET /product/{product_id}
```

Use resources not action
/orders
not /create_orders
/delete_orders
## add versioning

allows update while supporting backlog compatibilty
does not disrupt api consumers
## Rule #2: DON'T add unnecessary path segments

[](https://github.com/stickfigure/blog/wiki/How-to-\(and-how-not-to\)-design-REST-APIs#rule-2-dont-add-unnecessary-path-segments)

A common mistake seems to be trying to build your relational model into your URL structure. Etsy's _new_ API is [full of this kind of thing](https://developer.etsy.com/documentation/reference#operation/getListing):

```
# GOOD
GET /v3/application/listings/{listing_id}

# BAD
PATCH /v3/application/shops/{shop_id}/listings/{listing_id}
GET /v3/application/shops/{shop_id}/listings/{listing_id}/properties
PUT /v3/application/shops/{shop_id}/listings/{listing_id}/properties/{property_id}
```

The `{listing_id}` is globally unique; there's no reason for `{shop_id}` to be part of the URL. Besides irritating your developers with extra clutter, it inevitably causes problems when your invariant changes down the road - say, a listing moves to a different store or can be listed in multiple stores.

I've seen this mistake repeated over and over; I can only assume it's a manifestation of someone's OCD:

```
GET /shops/{shop_id}/listings              # normal, expected
GET /shops/{shop_id}/listings/{listing_id} # someone trying to be "consistent"?
GET /listings/{listing_id}                 # a much better endpoint
```

Which is not to say that compound URLs don't make sense - use them when you genuinely have compound keys.

```
# When {option_id} is not globally unique
GET /listings/{listing_id}/options/{option_id}
```

## Rule #3: DON'T add .json or other extensions to the url

[](https://github.com/stickfigure/blog/wiki/How-to-\(and-how-not-to\)-design-REST-APIs#rule-3-dont-add-json-or-other-extensions-to-the-url)

This seems to have been some sort of default behavior of Rails, so it shows up intermittently in public APIs. [Shopify](https://shopify.dev/docs/api/admin-rest) gets shame here.

- URLs are resource identifiers, not representations. Adding representation information to the URL means there's no canonical URL for a 'thing'. Clients may have trouble uniquely identifying 'things' by URL.
- "JSON" is not even a complete specification of the representation. What transfer encoding, for example?
- HTTP already offers headers (`Accept`, `Accept-Charset`, `Accept-Encoding`, `Accept-Language`) to negotiate representations.
- Putting stock text at the end of URLs annoys the people writing clients.
- JSON should be the default anyway.

Back in the 2000s there might have been some question about whether clients want JSON or XML, but here in the 2020s it has been settled. Return JSON, and if clients want to negotiate for something else, rely on the standard HTTP headers.

## Rule #4: DON'T return arrays as top level responses

[](https://github.com/stickfigure/blog/wiki/How-to-\(and-how-not-to\)-design-REST-APIs#rule-4-dont-return-arrays-as-top-level-responses)

The top level response from an endpoint should always be an object, never an array.

```
# GOOD
GET /things returns:
{ "data": [{ ...thing1...}, { ...thing2...}] }

# BAD
GET /things returns:
[{ ...thing1...}, { ...thing2...}]
```

The problem is that it's very hard to make backwards compatible changes when you return arrays. Objects let you make additive changes.

The obvious common evolution in this specific example will be to add pagination. You can always add `totalCount` or `hasMore` fields and old clients will continue to work. If your endpoint returns a top-level array, you will need a whole new endpoint.

## Rule #5: DON'T return map structures

[](https://github.com/stickfigure/blog/wiki/How-to-\(and-how-not-to\)-design-REST-APIs#rule-5-dont-return-map-structures)

I often see map structures used for collections in JSON responses. Return an array of objects instead.

```
# BAD
GET /things returns:
{
    "KEY1": { "id": "KEY1", "foo": "bar" },
    "KEY2": { "id": "KEY2", "foo": "baz" },
    "KEY3": { "id": "KEY3", "foo": "bat" }
}

# GOOD (also note application of Rule #4)
GET /things returns:
{
    "data": [
        { "id": "KEY1", "foo": "bar" },
        { "id": "KEY2", "foo": "baz" },
        { "id": "KEY3", "foo": "bat" }
    ]   
}
```

Map structures in JSON are bad:

- The key information is redundant and adds noise to the wire
- Unnecessary dynamic keys create headaches for people working in typed languages
- Whatever you think a "natural" key is can change, or clients may want a different grouping

Converting an array of objects to a map is a one-liner in most languages. If your client wants efficient random-access to the collection of objects, they can create that structure. You don't need to put it on the wire.

The worst thing about returning map structures is that your conceptual keys may change over time, and the only way to migrate is to break backwards compatibility. OpenAPI is a cautionary tale - [v3 to v4](https://github.com/OAI/moonwalk) is full of unnecessary breaking changes because they rely heavily on map structures instead of array structures.

```
# OpenAPI v3 structure
{
    "paths": {
        "/speakers": {
            "post": { ...information about the endpoint...}
        }
    }
}

# Proposed OpenAPI v4 structure, which names requests by adding a new 
# map layer (eg "createSpeaker").
{
    "paths": {
        "/speakers": {
            "requests": {
                "createSpeaker": {
                    "method": "post",
                    ...rest of the endpoint info...
                }
            }
        }
    }
}
```

If this was a flatter list structure, adding a name to an object is a nonbreaking change:

```
# Hypothetical flat array structure, using fields instead of map keys
{
    "requests": [
        {
            name: "createSpeaker",    // adding this field is nonbreaking
            path: "/speakers",
            method: "post",
            ...etc...
        }
    ]
}
```

### Exception to the no-map rule

[](https://github.com/stickfigure/blog/wiki/How-to-\(and-how-not-to\)-design-REST-APIs#exception-to-the-no-map-rule)

The exception to the no-map rule is simple key/value pairs, like [Stripe's metadata](https://stripe.com/docs/api/metadata).

```
# OK
{ 
    "key1": "value1",
    "key2": "value2"
}
```

Nobody will fault you for this structure. But if the values are more than simple strings, prefer arrays of objects instead.
## Rule #6: DO use strings for all identifiers

[](https://github.com/stickfigure/blog/wiki/How-to-\(and-how-not-to\)-design-REST-APIs#rule-6-do-use-strings-for-all-identifiers)

Always use strings for object identifiers, even if your internal representation (ie database column type) is numeric. Just stringify the number.

```
# BAD
{ "id": 123 }

# GOOD
{ "id": "123" }
```

A great API will outlast you, your implementation code, and the company that created it. In that time your infrastructure might be rewritten on a different technology platform, migrated to a new database, or merged with another database that contains conflicting IDs.

String IDs are incredibly flexible. Strings can encode version information or segment ID ranges. Strings can encode composite keys. Numeric IDs put a straightjacket on future developers.

I once worked on a system that (because of a database merge) had to segment numeric ID ranges by giving one group positive IDs, the other negative IDs. Aside from the general ugliness, you can only do this segmentation once.

As a bonus, if all your ID fields are strings, client developers working in typed languages don't need to think about which type to use. Just use strings!

## Rule #7: DO prefix your identifiers

[](https://github.com/stickfigure/blog/wiki/How-to-\(and-how-not-to\)-design-REST-APIs#rule-7-do-prefix-your-identifiers)

If your application is at all complicated, you'll end up with a _lot_ of different object types. Keeping opaque IDs straight is a mental challenge for both you and your client developers. You can dramatically improve the ergonomics of your API by making different types of IDs self-describing.

- Stripe's identifiers have two-letter-plus-underscore prefixes: `in_1MVpWEJVZPfyS2HyRgVDkwiZ`
- Shopify's graphql identifiers look like URLs (though their REST API IDs are numeric, boo): `gid://shopify/FulfillmentOrder/1469358604360`

It doesn't matter what format you use, as long as 1) they're visually distinct and 2) they don't change.

Everyone will appreciate the reduced support load when you can instantly tell the difference between an "order line item ID", a "fulfillment order line item ID", and an "invoice item line item ID".

## Rule #9: BE consistent

[](https://github.com/stickfigure/blog/wiki/How-to-\(and-how-not-to\)-design-REST-APIs#rule-9-be-consistent)

Mostly this section is here so that I can mock Shopify. There are 6 subtly different schemas for an Address in their REST API:

- [DraftOrder](https://shopify.dev/docs/api/admin-rest/2023-07/resources/draftorder) has most of the address fields you would expect, including `name`, `first_name`, `last_name`, `province`, `province_code`, `country`, `country_code`
- [Customer Address](https://shopify.dev/docs/api/admin-rest/2023-07/resources/customer-address) adds `country_name`
- [Order](https://shopify.dev/docs/api/admin-rest/2023-07/resources/order) billing_address adds `latitude`, `longitude` but shipping_address does not
- [Checkout](https://shopify.dev/docs/api/admin-rest/2023-07/resources/checkout) billing_address and shipping_address have no `name` (but still have `first_name`, `last_name`)
- [AssignedFulfillmentOrder](https://shopify.dev/docs/api/admin-rest/2023-07/resources/assignedfulfillmentorder) destination is missing `name`, `province_code`, `country_code` (but still has `first_name`, `last_name`, and the full `country` and `province` names)
- [Location](https://shopify.dev/docs/api/admin-rest/2023-07/resources/location) has `name` but not `first_name` or `last_name` - at least this one makes sense

This is _maddening_. It feels like someone at Shopify is toying with us: "_Simon says_ there's a `country` field. _Simon says_ there's a `country_name` field. There's a `country_code` field. Hahaha, null pointer exception for you!"

Please _please_ do your best to keep fields consistent among objects with similar meanings. If you're working in a dynamic language like Ruby or Python, try extra hard!

## Rule #10: DO use a structured error format

[](https://github.com/stickfigure/blog/wiki/How-to-\(and-how-not-to\)-design-REST-APIs#rule-10-do-use-a-structured-error-format)

If you're building the backend for a simple website you can probably ignore this section. But if you're building a large system with multiple layers of REST services, you can save yourself a lot of headache by establishing a standard error format up front.

My error formats tend to look something like this, roughly shaped like a (Java) exception:

```
{
  "message": "You do not have permission to access this resource",
  "type": "Unauthorized",
  "types": ["Unauthorized", "Security"],
  "cause": { ...recurse for nested any exceptions... }
}
```

The standard error format (with a nested cause) means that you can wrap and rethrow errors multiple layers deep:

```
ServiceAlpha -> ServiceBravo -> ServiceCharlie -> ServiceDelta
```

If ServiceDelta raises an error, ServiceAlpha can return (or log) the complete chain, including the root cause. This is _much_ easier to debug than combing through the logs on four different systems - even with centralized logging.


## Rule #11: DO provide idempotence mechanisms

[](https://github.com/stickfigure/blog/wiki/How-to-\(and-how-not-to\)-design-REST-APIs#rule-11-do-provide-idempotence-mechanisms)

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

[](https://github.com/stickfigure/blog/wiki/How-to-\(and-how-not-to\)-design-REST-APIs#a-brief-primer-on-idempotence)

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

Create operations, usually associated with `POST`, are different. Without special handling, they are _not_ idempotent.

```
# Every time you call this, we create a new order
POST /orders
{"product": "frisbee", "address": {...etc...}}
```

Because the network is not reliable, we suffer from the [Two General's Problem](https://en.wikipedia.org/wiki/Two_Generals%27_Problem). If an error occurs, there's no way for the client to know whether or not the operation successfully completed on the server. If the client submits the order again, we may create duplicate orders ("at-least-once"). If the client does not re-submit the order, we may lose orders ("at-most-once").

To get exactly-once behavior for non-idempotent operations, we need additional coordination between the client and server. There are generally two good ways and one crappy way to support this.

#### Good option: An "idempotency key" or "client reference ID"

[](https://github.com/stickfigure/blog/wiki/How-to-\(and-how-not-to\)-design-REST-APIs#good-option-an-idempotency-key-or-client-reference-id)

Let the client submit a unique value with the POST, and enforce uniqueness of this value on the server. [Stripe](https://stripe.com/docs/api/idempotent_requests) works this way, using a header. They store the idempotency key for 24 hours, giving you 24 hours of protection against duplication:

```
POST /v1/customers
Idemptency-Key: blahblahblahblah
{"name":"Bob Dobbs"}
```

Similarly, many order processing systems allow clients to submit a "customer reference ID" which is persisted with each order and included in customer reports. Enforcing uniqueness of this value protects against duplicate orders in perpetuity.

Make sure the key/id is a string - see Rule #6.

#### Good option: Let the client pick IDs

[](https://github.com/stickfigure/blog/wiki/How-to-\(and-how-not-to\)-design-REST-APIs#good-option-let-the-client-pick-ids)

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

[](https://github.com/stickfigure/blog/wiki/How-to-\(and-how-not-to\)-design-REST-APIs#crappy-option-provide-an-endpoint-to-list-recent-transactions)

This is a workaround for client developers if the API doesn't offer any explicit help with idempotence:

1. Before _every_ submission, fetch a list of recent transactions from the server.
2. Look for an existing transaction that matches your intended submission (hopefully you have a client reference ID to match).

For this to work, the client must serialize all create operations - otherwise there is a race condition. It's slow, and maintaining an N hour safety window means fetching N hours of transactions - potentially prohibitive on a busy system. But if you're building a client and the API doesn't provide another idempotence mechanism, this is what you have to do.

### When a conflict occurs...

[](https://github.com/stickfigure/blog/wiki/How-to-\(and-how-not-to\)-design-REST-APIs#when-a-conflict-occurs)

Now that your API offers a (good) idempotence mechanism, there's one more major consideration: How do you inform the client that there's a conflict? There are two main schools of thought:

#### Return an error

[](https://github.com/stickfigure/blog/wiki/How-to-\(and-how-not-to\)-design-REST-APIs#return-an-error)

When a client submits a duplicate idempotency key, I like to return 409 CONFLICT. There is one trick here - unless you're using user-submitted IDs ("Let the client pick IDs"), you need to include the existing ID in the error message or otherwise provide a mechanism to lookup the ID by idempotency key.

```
POST /things
{"idempotency_key": "blahblahblah", ...etc...}

# Response 409 CONFLICT
{"message": "This is a duplicate", old_id": "THG1234"}
```

When the client gets a 409 CONFLICT response, it says "oh, already done" and records the created ID. Just like it would have if the first POST returned without error.

#### Return the earlier response

[](https://github.com/stickfigure/blog/wiki/How-to-\(and-how-not-to\)-design-REST-APIs#return-the-earlier-response)

Instead of returning an error to the client, give them back the exact response that the client should have gotten the first time.

This allows clients to be a little dumber since they don't have to explicitly code up a CONFLICT error handler. However, it significantly complicates server implementation: You need to store all responses for a period of time and you need to validate that the client sent the exact same parameters with each request.

Stripe chose this route. I personally never have; it's a _lot_ of sever work for just a little client convenience.

### TL;DR

[](https://github.com/stickfigure/blog/wiki/How-to-\(and-how-not-to\)-design-REST-APIs#tldr)

There are a few ways of enabling idempotent behavior for non-idempotent operations. As long as you pick _something_, your clients will be happy. If you don't want to think about it too hard, go with this solution:

- Have the client submit an idempotency key (aka "customer reference ID") with each POST/create operation
- Store it in the database with a unique constraint
- Return 409 CONFLICT when you violate the unique constraint
- Provide the original ID in the 409 response body

## Rule #12: DO use ISO8601 strings for timestamps

[](https://github.com/stickfigure/blog/wiki/How-to-\(and-how-not-to\)-design-REST-APIs#rule-12-do-use-iso8601-strings-for-timestamps)

Use strings for timestamps, not numbers like milliseconds-since-epoch. Human readability matters! Someone glancing at "2023-12-21T11:17:12.34Z" might notice that it's a month in the future; someone glancing at 1703157432340 will not.

There is a [standard format](https://en.wikipedia.org/wiki/ISO_8601) for timestamps. It looks like the string above (including the 'T'). All of your clients will have easy access to library routines that parse and generate this format.

All timestamps should be in UTC ("Z").

**Bad** arguments for numeric timestamps include:

- "There are multiple date/time formats" - Use ISO8601.
- "Adding/subtracting to UTC is hard" - It's easier than counting seconds since 1970.
- "Parsing numbers is faster" - If you care that much about performance, use a binary format rather than JSON.

### Rule #12a: Use ISO8601 for _all_ date/time-related values

[](https://github.com/stickfigure/blog/wiki/How-to-\(and-how-not-to\)-design-REST-APIs#rule-12a-use-iso8601-for-all-datetime-related-values)

ISO8601 standardizes formats for many other date- and time-related concepts, including local (zoneless) dates and times, durations, and intervals. Use them.

### Rule #12b: DON'T trust your language/platform defaults

[](https://github.com/stickfigure/blog/wiki/How-to-\(and-how-not-to\)-design-REST-APIs#rule-12b-dont-trust-your-languageplatform-defaults)

Many development platforms do not generate ISO8601 formats by default. Even worse, the default format often varies depending on the locale and/or timezone of the machine! Whenever you format a date/time value in your API, verify the output. There's always a way to generate ISO8601 (hint: Javascript has `Date.toISOString()`).



Further Info

1. https://github.com/stickfigure/blog/wiki/How-to-(and-how-not-to)-design-REST-APIs
2. https://www.youtube.com/watch?v=_gQaygjm_hg&list=PL53DoAIBJrduh8azUQKPFrxOPjAktLnSd&index=6



talk about pagination

use clear query string for sorting and filtering

GET /products?filter=color:blue&sort_by=name

request header for authorization Authorization: Bearer

keep cross resource linking simple
since resources are grouped in a collection...
avoid more than 2 levels...
/api/vi/cart/123/items/321
/api/v1/items?card_id=123&item_id=321 NO

costumers/1/orders/99/product/2 no make it difficult to maintain change
do 2 uris
constumers/1/orders
order/99/products
no trailing forward slash
/ hierarchal relationships
use hyphens -
query params are best to filter sort paginate and limit

## Solid Error/Exception Handling

catch the exception
give a description
and the correct status codes to return to the client

Hypermedia as the engine of application state
tells us how to interact... but comes at a cost in computation and a low adoption 


<div style="display: flex; justify-content: center; flex-direction: column; align-items: center;">
  <h2 style="font-family: 'Arial Black';">Richardson Maturity Model</h2>
  <table style="border-collapse: collapse; font-family: 'Arial Black'; font-size: 16px;">
    <tr>
      <td style="border: none; background-color: #FFD700; border-radius: 15px; padding: 10px; color: black; text-align: center; width: 150px;">Level 3</td>
      <td style="border: none; text-align: left; vertical-align: middle;">    Hypermedia Controls</td>
    </tr>
    <tr>
      <td style="border: none; background-color: #C0C0C0; border-radius: 15px; padding: 10px; color: black; text-align: center; width: 150px;">Level 2</td>
      <td style="border: none; text-align: left; vertical-align: middle;">    HTTP Verbs</td>
    </tr>
    <tr>
      <td style="border: none; background-color: #B87333; border-radius: 15px; padding: 10px; color: black; text-align: center; width: 150px;">Level 1</td>
      <td style="border: none; text-align: left; vertical-align: middle;">    Resources</td>
    </tr>
    <tr>
      <td style="border: none; background-color: #FF6666; border-radius: 15px; padding: 10px; color: black; text-align: center; width: 150px;">Level 0</td>
      <td style="border: none; text-align: left; vertical-align: middle;">    Swamp of POX</td>
    </tr>
  </table>
</div>
