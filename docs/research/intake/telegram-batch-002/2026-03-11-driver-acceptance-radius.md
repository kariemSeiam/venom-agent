# Driver Acceptance Radius - Mobile Integration Guide

**Date:** 2026-03-11
**Status:** Backend deployed to production
**Priority:** Ready for mobile implementation

---

## What Changed

Drivers can now set a personal acceptance radius (100m - 15km) to control how far they're willing to go for ride requests. The system filters invitations based on each driver's radius. If no drivers are found after 3 attempts, a Smart Override sends invitations to the closest drivers regardless of their radius setting.

---

## API Endpoints

Base URL: `https://api.taxiarab.net`

All endpoints require:
```
Authorization: Bearer {driver_token}
Accept: application/json
```

### GET /drivers/settings/acceptance-radius

Returns the driver's current radius and allowed range.

**Response:**
```json
{
  "success": true,
  "data": {
    "current_radius": 15000,
    "min_allowed": 100,
    "max_allowed": 15000,
    "unit": "meters"
  }
}
```

### PUT /drivers/settings/acceptance-radius

Updates the driver's acceptance radius.

**Request body:**
```json
{
  "acceptance_radius": 5000
}
```

**Success response:**
```json
{
  "success": true,
  "message": "تم تحديث نطاق القبول بنجاح",
  "data": {
    "id": 1,
    "acceptance_radius": 5000
  }
}
```

**Validation errors:**

| Case | Message |
|------|---------|
| Missing field | نطاق القبول مطلوب |
| Not an integer | نطاق القبول غير صالح |
| Below minimum | نطاق القبول صغير جداً. الحد الأدنى {min} متر |
| Above maximum | نطاق القبول كبير جداً. الحد الأقصى {max} متر |
| During active ride | لا يمكن تغيير نطاق القبول أثناء رحلة نشطة |

---

## What Mobile Needs to Build

### 1. Settings Screen

Add an "نطاق القبول" section in driver settings:

- Slider or input: range from `min_allowed` to `max_allowed` (from GET response)
- Display value in kilometers (divide by 1000)
- Disable the control when the driver has an active ride
- Call GET on screen load, PUT on save

### 2. Invitation Screen

The ride invitation payload now includes a new field:

```json
{
  "is_outside_radius": true
}
```

When `is_outside_radius` is `true`:
- Show a label: "خارج نطاقك المحدد"
- Optionally show distance info: "المسافة: X كم (نطاقك: Y كم)"
- Use a distinct visual style (e.g. different color or border)
- The driver can still accept or decline normally

When `is_outside_radius` is `false` or absent: no change to current behavior.

---

## Notes

- All existing drivers default to 15km (no behavior change until they modify it)
- The `acceptance_radius` field is now included in the DriverResource response
- Bonus display is not needed yet (deferred)
