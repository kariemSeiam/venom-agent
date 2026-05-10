# GeoLink API — VENOM to AI

> **Purpose:** Give your AI everything it needs to integrate with GeoLink. Every key. Every param. Every response shape. Every error. No guessing.

---

## 1. Identity & Basics

| Property | Value |
|----------|-------|
| **Platform** | GeoLink — Geolocation API |
| **Base URL** | `https://geolink-eg.com` |
| **Auth** | API key via query param `key` (required on every request) |
| **Method** | All endpoints use **GET** |
| **Content-Type** | `application/json` (responses) |

---

## 2. Global Response Contract

### Success
```json
{
  "success": true,
  "data": { ... }
}
```

### Error
```json
{
  "success": false,
  "error": "Human-readable error message"
}
```

**Important:** There is no `error_code` or `error_id` in the standard response. Only `success` and `error`.

---

## 3. Error Messages (Exact Strings)

These are the **exact** error messages your AI may receive. Use them for parsing and user-facing fallbacks.

| Context | Message |
|---------|---------|
| Missing/invalid API key | `"API key is required"` |
| Invalid params (e.g. bad coords) | `"Some of your parameters are invalid. Please review and try again."` |
| Location not found | `"We couldn't find that location. Please try with a different search term or coordinates."` |
| Route not available | `"We couldn't calculate a route between these locations. Please verify the addresses."` |
| No results | `"No results found for your search. Try refining your query."` |
| Service busy | `"Our service is temporarily busy. Please try again in a moment."` |
| Processing error | `"We encountered an error processing your request. Please try again."` |
| Distance matrix validation | Custom messages (e.g. `"origins must be a semicolon-separated list of 'lat,lng' pairs"`) |

---

## 4. HTTP Status Codes

| Code | When |
|------|------|
| 200 | Success |
| 400 | Bad request — missing param, invalid param, validation failed |
| 401 | Unauthorized — missing or invalid API key |
| 500 | Server error, location not found, route not available, processing error |

---

## 5. Endpoint Matrix

| Endpoint | v1 | v2 | Notes |
|----------|----|----|-------|
| Text Search | `/api/v1/text_search` | `/api/v2/text_search` | v2: structured `address_parts`, `location` object |
| Directions | `/api/v1/directions` | `/api/v2/directions` | v2: `distance`/`duration` objects, `origin`/`destination`, `bounds` |
| Geocode | `/api/v1/geocode` | `/api/v2/geocode` | v2: no lat/lng bias params, faster |
| Reverse Geocode | `/api/v1/reverse_geocode` | `/api/v2/reverse_geocode` | v2: `address_parts`, `bounds` |
| **Distance Matrix** | `/api/v1/distance_matrix` | — | **v1 ONLY** — no v2 |

---

## 6. Endpoint Reference — Full Detail

---

### 6.1 Text Search v1 — `GET /api/v1/text_search`

**Request parameters**

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `key` | string | ✓ | — | API key |
| `query` | string | ✓ | — | Search text (e.g. "coffee shop", "restaurant") |
| `latitude` | number | | 30.0444 | Search center latitude |
| `longitude` | number | | 31.2357 | Search center longitude |
| `language` | string | | ar | Language code |
| `country` | string | | eg | Country code |

**Response `data`** — array of place objects:

| Key | Type | Description |
|-----|------|--------------|
| `short_address` | string | Brief name or address |
| `long_address` | string | Full formatted address |
| `latitude` | number | Latitude |
| `longitude` | number | Longitude |

**Example response**
```json
{
  "success": true,
  "data": [
    {
      "short_address": "Cairo Tower",
      "long_address": "Cairo Tower, Zamalek, Cairo Governorate, Egypt",
      "latitude": 30.0459,
      "longitude": 31.2243
    }
  ]
}
```

---

### 6.2 Text Search v2 — `GET /api/v2/text_search`

**Request parameters** — same as v1.

**Response `data`** — array of place objects (v2 shape):

| Key | Type | Description |
|-----|------|--------------|
| `short_address` | string | Brief name |
| `address` | string | Full formatted address |
| `address_parts` | object | Structured components |
| `address_parts.district` | string | District or neighborhood |
| `address_parts.governorate` | string | Governorate or state |
| `address_parts.country` | string | ISO 3166-1 alpha-2 (e.g. "EG") |
| `location` | object | Coordinates |
| `location.lat` | number | Latitude |
| `location.lng` | number | Longitude |

**Example response**
```json
{
  "success": true,
  "data": [
    {
      "address": "Cairo Tower, Zamalek, Cairo Governorate, Egypt",
      "short_address": "Cairo Tower",
      "address_parts": {
        "district": "Zamalek",
        "governorate": "Cairo Governorate",
        "country": "EG"
      },
      "location": {
        "lat": 30.0459,
        "lng": 31.2243
      }
    }
  ]
}
```

---

### 6.3 Directions v1 — `GET /api/v1/directions`

**Request parameters**

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `key` | string | ✓ | — | API key |
| `origin_latitude` | number | ✓ | — | Origin latitude |
| `origin_longitude` | number | ✓ | — | Origin longitude |
| `destination_latitude` | number | ✓ | — | Destination latitude |
| `destination_longitude` | number | ✓ | — | Destination longitude |
| `language` | string | | ar | Language code |
| `country` | string | | eg | Country code |

**Response `data`** — array of route objects (typically one):

| Key | Type | Description |
|-----|------|--------------|
| `distance_meters` | number | Distance in meters |
| `distance_text` | string | Human-readable (e.g. "12.5 km") |
| `duration_seconds` | number | Travel time in seconds |
| `duration_text` | string | Human-readable (e.g. "30 mins") |
| `waypoints` | array | Route path |
| `waypoints[].lat` | number | Waypoint latitude |
| `waypoints[].lng` | number | Waypoint longitude |

**Example response**
```json
{
  "success": true,
  "data": [
    {
      "distance_meters": 850,
      "distance_text": "0.9 km",
      "duration_seconds": 180,
      "duration_text": "3 mins",
      "waypoints": [
        { "lat": 30.0444, "lng": 31.2357 },
        { "lat": 30.0465, "lng": 31.2370 },
        { "lat": 30.0490, "lng": 31.2390 }
      ]
    }
  ]
}
```

---

### 6.4 Directions v2 — `GET /api/v2/directions`

**Request parameters** — same as v1.

**Response `data`** — array of route objects (v2 shape, may include multiple alternatives):

| Key | Type | Description |
|-----|------|--------------|
| `distance` | object | Distance |
| `distance.meters` | number | Distance in meters |
| `distance.text` | string | Human-readable |
| `duration` | object | Duration |
| `duration.seconds` | number | Travel time in seconds |
| `duration.text` | string | Human-readable |
| `bounds` | object | Bounding box |
| `bounds.northeast` | object | Northeast corner |
| `bounds.northeast.lat` | number | Latitude |
| `bounds.northeast.lng` | number | Longitude |
| `bounds.southwest` | object | Southwest corner |
| `bounds.southwest.lat` | number | Latitude |
| `bounds.southwest.lng` | number | Longitude |
| `origin` | object | Origin point |
| `origin.lat` | number | Latitude |
| `origin.lng` | number | Longitude |
| `origin.address` | string | Full address |
| `origin.short_address` | string | Brief address |
| `destination` | object | Destination point |
| `destination.lat` | number | Latitude |
| `destination.lng` | number | Longitude |
| `destination.address` | string | Full address |
| `destination.short_address` | string | Brief address |
| `waypoints` | array | Array of `[lat, lng]` pairs (not objects) |

**Example response**
```json
{
  "success": true,
  "data": [
    {
      "distance": { "meters": 969, "text": "1.0 km" },
      "duration": { "seconds": 290, "text": "5 min" },
      "bounds": {
        "northeast": { "lat": 30.0440281, "lng": 31.2355882 },
        "southwest": { "lat": 30.049344, "lng": 31.2390348 }
      },
      "origin": {
        "lat": 30.0440343,
        "lng": 31.2356293,
        "address": "Cairo Governorate",
        "short_address": "Tahrir Square"
      },
      "destination": {
        "lat": 30.0490461,
        "lng": 31.2390348,
        "address": "Marouf, Qasr El Nil, Cairo Governorate",
        "short_address": "Haret Al Bosti"
      },
      "waypoints": [
        [30.0440343, 31.2356293],
        [30.0440281, 31.2357117]
      ]
    }
  ]
}
```

---

### 6.5 Geocode v1 — `GET /api/v1/geocode`

**Request parameters**

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `key` | string | ✓ | — | API key |
| `query` | string | ✓ | — | Address or place name |
| `latitude` | number | | 31.5527384 | Center latitude for bias |
| `longitude` | number | | 30.4167506 | Center longitude for bias |
| `language` | string | | ar | Language code |
| `country` | string | | eg | Country code |

**Response `data`** — single object:

| Key | Type | Description |
|-----|------|--------------|
| `latitude` | number | Place latitude |
| `longitude` | number | Place longitude |
| `long_address` | string | Full formatted address |
| `short_address` | string | Brief name or address |

**Example response**
```json
{
  "success": true,
  "data": {
    "latitude": 30.0444,
    "longitude": 31.2357,
    "long_address": "Tahrir Square, Downtown, Cairo Governorate, Egypt",
    "short_address": "Tahrir Square"
  }
}
```

---

### 6.6 Geocode v2 — `GET /api/v2/geocode`

**Request parameters**

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `key` | string | ✓ | — | API key |
| `query` | string | ✓ | — | Address or place name |
| `language` | string | | ar | Language code |
| `country` | string | | eg | Country code |

**Note:** v2 has **no** `latitude`/`longitude` bias params. Ultra-fast, single result.

**Response `data`** — single object (v2 shape):

| Key | Type | Description |
|-----|------|--------------|
| `address` | string | Full formatted address |
| `short_address` | string | Brief name |
| `address_parts` | object | Structured components |
| `address_parts.district` | string | District |
| `address_parts.governorate` | string | Governorate |
| `address_parts.country` | string | Country code |
| `location` | object | Coordinates |
| `location.lat` | number | Latitude |
| `location.lng` | number | Longitude |
| `bounds` | object | Viewport bounds |
| `bounds.northeast` | object | Northeast corner (lat, lng) |
| `bounds.southwest` | object | Southwest corner (lat, lng) |

**Example response**
```json
{
  "success": true,
  "data": {
    "address": "Cairo Tower, Zamalek, Cairo Governorate, Egypt",
    "short_address": "Cairo Tower",
    "address_parts": {
      "country": "EG",
      "district": "Zamalek",
      "governorate": "Cairo"
    },
    "location": {
      "lat": 30.0459,
      "lng": 31.2243
    },
    "bounds": {
      "northeast": { "lat": 30.0469, "lng": 31.2253 },
      "southwest": { "lat": 30.0449, "lng": 31.2233 }
    }
  }
}
```

---

### 6.7 Reverse Geocode v1 — `GET /api/v1/reverse_geocode`

**Request parameters**

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `key` | string | ✓ | — | API key |
| `latitude` | number | ✓ | — | Latitude |
| `longitude` | number | ✓ | — | Longitude |
| `language` | string | | ar | Language code |
| `country` | string | | eg | Country code |

**Response `data`** — single object:

| Key | Type | Description |
|-----|------|--------------|
| `address` | string | Full formatted address |
| `sub_address` | string | Brief name or address |

**Example response**
```json
{
  "success": true,
  "data": {
    "address": "Cairo Tower, Zamalek, Cairo Governorate, Egypt",
    "sub_address": "Cairo Tower"
  }
}
```

---

### 6.8 Reverse Geocode v2 — `GET /api/v2/reverse_geocode`

**Request parameters** — same as v1.

**Response `data`** — single object (v2 shape):

| Key | Type | Description |
|-----|------|--------------|
| `address` | string | Full formatted address |
| `short_address` | string | Brief name |
| `address_parts` | object | Structured components |
| `address_parts.district` | string | District |
| `address_parts.governorate` | string | Governorate |
| `address_parts.country` | string | Country code |
| `location` | object | Coordinates |
| `location.lat` | number | Latitude |
| `location.lng` | number | Longitude |
| `bounds` | object | Viewport bounds |
| `bounds.northeast` | object | Northeast corner |
| `bounds.southwest` | object | Southwest corner |

**Example response**
```json
{
  "success": true,
  "data": {
    "address": "Cairo Tower, Zamalek, Cairo Governorate, Egypt",
    "short_address": "Cairo Tower",
    "address_parts": {
      "country": "EG",
      "district": "Zamalek",
      "governorate": "Cairo Governorate"
    },
    "location": {
      "lat": 30.0459,
      "lng": 31.2243
    },
    "bounds": {
      "northeast": { "lat": 30.0469, "lng": 31.2253 },
      "southwest": { "lat": 30.0449, "lng": 31.2233 }
    }
  }
}
```

---

### 6.9 Distance Matrix — `GET /api/v1/distance_matrix` **(v1 ONLY)**

Batch compute distances and durations between multiple origins and destinations. **No v2.**

**Request parameters**

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `key` | string | ✓ | — | API key |
| `origins` | string | ✓ | — | Semicolon-separated `lat,lng` pairs |
| `destinations` | string | ✓ | — | Semicolon-separated `lat,lng` pairs |
| `language` | string | | ar | Language code |
| `country` | string | | eg | Country code |

**Format for `origins` and `destinations`:**
- Each pair: `lat,lng` (comma, no space)
- Multiple pairs: `;` (semicolon)
- Example: `30.0444,31.2357;30.0500,31.2400`

**Validation rules:**
- At least one pair per origins and destinations
- Max **150** coordinate pairs per origins
- Max **150** coordinate pairs per destinations
- Invalid format → 400 with message like: `"origins must be a semicolon-separated list of 'lat,lng' pairs"`

**Response `data`** — object:

| Key | Type | Description |
|-----|------|--------------|
| `origins` | array | Normalized origins |
| `origins[].coordinates` | array | `[lat, lng]` |
| `origins[].short_name` | string | Often empty |
| `origins[].full_address` | string | Often empty |
| `destinations` | array | Normalized destinations |
| `destinations[].coordinates` | array | `[lat, lng]` |
| `destinations[].short_name` | string | Often empty |
| `destinations[].full_address` | string | Often empty |
| `distance_matrix` | array | 2D array: `[origin_index][destination_index]` |
| `distance_matrix[i][j]` | object | Result for origin i → destination j |
| `distance_matrix[i][j].distance_meters` | number | Distance in meters |
| `distance_matrix[i][j].distance_text` | string | Human-readable (e.g. "0.95 km") |
| `distance_matrix[i][j].duration_seconds` | number | Duration in seconds |
| `distance_matrix[i][j].duration_text` | string | Human-readable (e.g. "3 mins") |
| `nearest_destination_index` | array | For each origin, index of fastest destination (or -1) |

**Example request**
```
GET /api/v1/distance_matrix?origins=30.0444,31.2357;30.0500,31.2400&destinations=30.0600,31.2500&language=en&country=eg&key=YOUR_KEY
```

**Example response**
```json
{
  "success": true,
  "data": {
    "origins": [
      { "coordinates": [30.0444, 31.2357], "short_name": "", "full_address": "" },
      { "coordinates": [30.0500, 31.2400], "short_name": "", "full_address": "" }
    ],
    "destinations": [
      { "coordinates": [30.0600, 31.2500], "short_name": "", "full_address": "" }
    ],
    "distance_matrix": [
      [
        {
          "distance_meters": 950,
          "distance_text": "0.95 km",
          "duration_seconds": 210,
          "duration_text": "3 mins"
        }
      ],
      [
        {
          "distance_meters": 520,
          "distance_text": "0.52 km",
          "duration_seconds": 120,
          "duration_text": "2 mins"
        }
      ]
    ],
    "nearest_destination_index": [0, 0]
  }
}
```

**Index semantics:**
- `distance_matrix[i][j]` = travel from origin `i` to destination `j`
- `nearest_destination_index[i]` = index of destination with shortest duration from origin `i`

---

## 7. V1 vs V2 — Key Differences

| Aspect | v1 | v2 |
|--------|----|----|
| Coordinates | `latitude`, `longitude` (flat) | `location.lat`, `location.lng` (nested) |
| Address | `long_address`, `sub_address` | `address`, `short_address` |
| Address structure | None | `address_parts` (district, governorate, country) |
| Bounds | None | `bounds` (northeast, southwest) |
| Geocode bias | `latitude`, `longitude` params | No bias params |
| Directions | `distance_meters`, `duration_seconds` | `distance.meters`, `duration.seconds` |
| Directions waypoints | `{lat, lng}` objects | `[lat, lng]` arrays |
| Directions extra | — | `origin`, `destination`, `bounds` |

---

## 8. Billing & Rate Limits

- **Billing:** Credit-based. Free monthly quota → account balance → credit limit.
- **Rate limits:** Per-API-key daily limit (configurable by account).
- **Test key:** `key=test` skips validation and billing (use for development only).

---

## 9. Quick Decision Table

| User need | Endpoint |
|-----------|----------|
| Search places by keyword | `/api/v2/text_search` |
| Route between two points | `/api/v2/directions` |
| Address → coordinates | `/api/v2/geocode` |
| Coordinates → address | `/api/v2/reverse_geocode` |
| Batch distances (N origins × M destinations) | `/api/v1/distance_matrix` |

---

*VENOM to AI. GeoLink V1. Last updated: 2026-03-11.*
