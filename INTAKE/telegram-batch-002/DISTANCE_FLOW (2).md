# Distance Flow — Client ↔ Backend ↔ Driver

> End-to-end journey of distance data from user request to driver screen. No code — architecture only.

---

## Data Keys

| Key | Meaning | Unit |
|-----|---------|------|
| `estimated_distance_in_km` | User's trip distance (pickup → dropoff) | km |
| `expected_distance` | Same, stored on ride | km |
| `driver_distance_from_pickup` | Driver → pickup | km |
| `actual_distance` | Real distance after ride | km |

---

## 1. User Journey — With Destination

```
User selects pickup + destination
    → Client: RouteManager.getRouteBetweenPickAndDest() or calculateSimpleRoute()
    → Source: GeoLink API (road) or android.location.Location.distanceTo() (straight line)
    → route.distance (km) + route.duration
    → CarTypesUseCase.findSuitableCars(distance) → POST /users/ride/upfront-fare
    → RideManager.createRide() parses route.distance → estimated_distance_in_km
    → POST /users/ride/create { estimated_distance_in_km, ... }
    → Backend: StartRideService stores expected_distance, uses for fare
```

**Where calculated:** Client (Android). Backend receives and stores.

---

## 2. User Journey — Quick Request (No Destination)

```
User selects pickup only, dest = "وجهه غير معلومة"
    → route.distance = "" (empty)
    → RideManager: distanceValue = 0.0
    → POST /users/ride/create { estimated_distance_in_km: 0, dropoff: null }
    → Backend: expected_distance = 0, estimateRidePriceForCarType(0)
    → Fare = baseFare + 0 = minimum fare
```

**Where calculated:** Client sends 0. Backend treats as 0 km → minimum fare.

---

## 3. Driver — Distance on Ride Request (Invitation)

```
Backend: RideInviteEvent → highlightRideInfoResource(ride)
    → driver_distance_from_pickup = null (no driver yet)
    → expected_distance = ride.expected_distance (from user)

Driver app receives invitation:
    → Backend payload: driver_distance_from_pickup = null, expected_distance = X
    → Driver calculates locally: getDistanceFromDriverAndPickUpLocationFromCurrentRide()
    → calculateAndUpdateRouteState(driverLoc, pickupLoc) → android.location.Location.distanceTo()
    → routeBetweenDriverAndPickUp.distance → shown on UI
```

**Where calculated:** Driver app (Android). Backend sends null; driver computes for display.

---

## 4. Driver — Accept Ride

```
Driver taps Accept
    → distanceToPickupKm = extractDistanceInKm(routeBetweenDriverAndPickUp?.distance)
    → POST /drivers/ride/{id}/accept { driver_distance_from_pickup_in_km }
    → Backend: RideAcceptService saves to ride.driver_distance_from_pickup
    → Used for: driver compensation (≥2 km), fare logic
```

**Where calculated:** Driver app. Backend stores and uses for compensation.

---

## 5. End Ride — Actual Distance

```
Driver ends ride
    → RideTrackingService: actual_distance from GPS tracking (SharedPreferences)
    → POST /drivers/ride/end { actual_distance, waiting_minutes }
    → Backend: RideFareCalculator.calculatePostTripFare(actual_distance)
    → Final fare based on actual_distance, not expected
```

**Where calculated:** Driver app (GPS during ride). Backend uses for final fare.

---

## Endpoint Summary

| Endpoint | Distance Field | Source |
|----------|----------------|--------|
| POST /users/ride/upfront-fare | estimated_distance_in_km | Client (optional, default 1 km) |
| POST /users/ride/create | estimated_distance_in_km | Client |
| ride_invitation (Pusher) | driver_distance_from_pickup | null; expected_distance from ride |
| POST /drivers/ride/{id}/accept | driver_distance_from_pickup_in_km | Driver |
| POST /drivers/ride/end | actual_distance | Driver |

---

## Bad Behaviors & Risks

| Issue | Where | Impact |
|-------|-------|--------|
| Quick request sends 0 km | Client | Fare = minimum only; may undercharge for long trips |
| Backend never validates distance | Backend | Client can send fake low distance → lower fare |
| driver_distance_from_pickup from client | N/A | Correct: driver sends on accept |
| Driver can fake driver_distance_from_pickup | Driver | Compensation abuse (≥2 km) |
| actual_distance from driver only | Driver | No backend verification; driver can over/underreport |
| GeoLink vs straight-line inconsistency | Client | RouteManager uses both; results can differ |
| Arabic numerals in distance string | Client | RideManager converts; regex `[\d.]+` can fail on bad input |
| Backend typo: `sucess` in response | Backend | Client must check both `success` and `sucess` |

---

## Flow Diagram (Text)

```
[User Client]
    │
    ├─ With dest: RouteManager → route.distance → createRide(estimated_distance_in_km)
    └─ No dest:   route.distance="" → 0.0 → createRide(0)
    │
    ▼
[Backend] POST /users/ride/create
    │
    ├─ expected_distance = request.estimated_distance_in_km
    ├─ driver_distance_from_pickup = null
    └─ SearchForDriverJob → RideInviteService
    │
    ▼
[Backend] ride_invitation (Pusher)
    │
    ├─ expected_distance (from ride)
    └─ driver_distance_from_pickup = null
    │
    ▼
[Driver App]
    │
    ├─ Displays: expected_distance (backend), distance to pickup (local calc)
    └─ On Accept: POST /accept { driver_distance_from_pickup_in_km } ← local calc
    │
    ▼
[Backend] Saves driver_distance_from_pickup
    │
    ▼
[Driver] Ends ride → actual_distance (GPS) → POST /end
    │
    ▼
[Backend] calculatePostTripFare(actual_distance)
```

---

*Last updated: 2025-03-17*
