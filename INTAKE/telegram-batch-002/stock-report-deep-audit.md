# Hvar ERP — Stock Report Deep Audit

> **Endpoint:** `/reports/stock-report`
> **Audit Date:** 2026-04-28
> **Scope:** Full data cycle — Route → Controller → Util → SQL → View → JS → Widget

---

## Table of Contents

1. [Request Flow Overview](#1-request-flow-overview)
2. [Route Layer](#2-route-layer)
3. [Controller Layer](#3-controller-layer)
4. [Utility Layer — ProductUtil::getProductStockDetails](#4-utility-layer--productutilgetproductstockdetails)
5. [Utility Layer — TransactionUtil::getOpeningClosingStock](#5-utility-layer--transactionutilgetopeningclosingstock)
6. [Database Tables & Relationships](#6-database-tables--relationships)
7. [View Layer — Blade Templates](#7-view-layer--blade-templates)
8. [JavaScript Layer — DataTable & Widgets](#8-javascript-layer--datatable--widgets)
9. [Computed Columns — Formulas Reference](#9-computed-columns--formulas-reference)
10. [The Two-Engine Problem](#10-the-two-engine-problem)
11. [Zero-Value Root Cause Analysis](#11-zero-value-root-cause-analysis)
12. [Dead Code & Bugs](#12-dead-code--bugs)
13. [Key Statistics](#13-key-statistics)

---

## 1. Request Flow Overview

```
Browser                              Server
  │                                    │
  │  GET /reports/stock-report         │
  │───────────────────────────────────>│  Route (web.php:658)
  │                                    │    → ReportController::getStockReport()
  │                                    │       ├── Permission: stock_report.view
  │                                    │       ├── Session: user.business_id
  │                                    │       ├── NOT AJAX → return Blade view
  │  HTML + JS (empty DataTable)       │       │   with dropdowns (categories, brands, etc.)
  │<───────────────────────────────────│       │
  │                                    │
  │  JS: DataTable init                │
  │  GET /reports/stock-report         │
  │  ?draw=1&location_id=X&...        │
  │───────────────────────────────────>│       ├── IS AJAX →
  │                                    │       │   ProductUtil::getProductStockDetails()
  │                                    │       │     → 6-table JOIN + 4 subqueries
  │                                    │       │     → GROUP BY variations.id, vld.location_id
  │                                    │       │   DataTable response with column transforms
  │  JSON (page data)                  │       │
  │<───────────────────────────────────│       │
  │                                    │
  │  JS: get_stock_value()             │
  │  GET /reports/get-stock-value      │
  │───────────────────────────────────>│  Route (web.php:686)
  │                                    │    → ReportController::getStockValue()
  │                                    │       ├── Permission: view_product_stock_value
  │                                    │       ├── TransactionUtil::getOpeningClosingStock(by_sale_price=false)
  │                                    │       ├── TransactionUtil::getOpeningClosingStock(by_sale_price=true)
  │                                    │       └── profit_margin = (sp - pp) / sp * 100
  │  JSON {closing_stock_by_pp,        │
  │        closing_stock_by_sp,        │
  │        potential_profit,           │
  │        profit_margin}              │
  │<───────────────────────────────────│
  │                                    │
  │  JS updates widget DOM elements    │
  │  (#closing_stock_by_pp, etc.)      │
  │                                    │
```

**Key Insight:** There are TWO separate AJAX calls on page load:
1. **DataTable** → `/reports/stock-report` (paginated rows)
2. **Widget** → `/reports/get-stock-value` (summary totals)

These use **different query engines** and can produce different numbers.

---

## 2. Route Layer

**File:** `routes/web.php`

| Line | Route | Controller | Purpose |
|------|-------|------------|---------|
| 658 | `GET /reports/stock-report` | `ReportController::getStockReport` | Main page + DataTable data |
| 686 | `GET /reports/get-stock-value` | `ReportController::getStockValue` | Widget summary values |

Both inside the standard auth middleware group. No additional route-level middleware.

---

## 3. Controller Layer

### 3.1 ReportController::getStockReport (Lines 379–582)

**File:** `app/Http/Controllers/ReportController.php`

**Permission Gate:**
```php
// Line 381
if (!auth()->user()->can('stock_report.view')) {
    abort(403, 'Unauthorized action.');
}
```

**Session Data:**
```php
// Line 385
$business_id = $request->session()->get('user.business_id');
```

**Selling Price Group Check (Lines 387–395):**
Iterates all `SellingPriceGroup` records for the business. Sets `$allowed_selling_price_group = true` if the user has permission to ANY group via `selling_price_group.{id}`. This controls whether a "View Group Prices" button appears in the unit_price column.

**Manufacturing Flag (Lines 396–400):**
```php
$show_manufacturing_data = 1;
// Only if Manufacturing module installed AND user has permission
```

**AJAX Branch (Line 402):**
```php
if ($request->ajax()) {
    // → Returns DataTable JSON response
    // → Core data from ProductUtil::getProductStockDetails()
    // → Column transforms in addColumn() callbacks
} else {
    // → Returns Blade view: report.stock_report
    // → Passes: $categories, $brands, $units, $business_locations, $show_manufacturing_data
}
```

**Filters Extracted (Lines 404–421):**
`location_id, category_id, sub_category_id, brand_id, unit_id, tax_id, type, only_mfg_products, active_state, not_for_selling, repair_model_id, product_id`

**Core Data Call (Line 430):**
```php
$products = $this->productUtil->getProductStockDetails($business_id, $filters, $for);
// $for = 'datatables' for AJAX, 'view_product' for view
```

### 3.2 ReportController::getStockValue (Lines 3585–3625)

**Permission Gate:**
```php
// Line 3587
if (!auth()->user()->can('view_product_stock_value')) {
    abort(403);
}
```

**Parameters:**
```php
$business_id = request()->session()->get('user.business_id');
$end_date = \Carbon::now()->format('Y-m-d');  // ← ALWAYS TODAY, no date param from frontend
$location_id = request()->input('location_id');
$filters = request()->only(['category_id', 'sub_category_id', 'brand_id', 'unit_id']);
```

**Two Calculation Calls:**
```php
// By PURCHASE price
$closing_stock_by_pp = $this->transactionUtil->getOpeningClosingStock(
    $business_id, $end_date, $location_id, false, false, $filters, $permitted_locations
);

// By SALE price
$closing_stock_by_sp = $this->transactionUtil->getOpeningClosingStock(
    $business_id, $end_date, $location_id, false, true, $filters, $permitted_locations
);
```

**Derived Values:**
```php
$potential_profit = $closing_stock_by_sp - $closing_stock_by_pp;
$profit_margin = empty($closing_stock_by_sp) ? 0 : ($potential_profit / $closing_stock_by_sp) * 100;
```

**Response:**
```json
{
    "closing_stock_by_pp": 39742418.04,
    "closing_stock_by_sp": null,
    "potential_profit": null,
    "profit_margin": 0
}
```

---

## 4. Utility Layer — ProductUtil::getProductStockDetails

**File:** `app/Http/Utils/ProductUtil.php` (Lines 1964–2113)

This is the **Engine #1** — powers the DataTable rows.

### 4.1 Base Query & Joins

```php
$query = Variation::join('products as p', 'p.id', '=', 'variations.product_id')
    ->join('units', 'p.unit_id', '=', 'units.id')
    ->leftjoin('variation_location_details as vld', 'variations.id', '=', 'vld.variation_id')
    ->leftjoin('business_locations as l', 'vld.location_id', '=', 'l.id')
    ->leftjoin('categories as c', 'p.category_id', '=', 'c.id')
    ->join('product_variations as pv', 'variations.product_variation_id', '=', 'pv.id')
    ->where('p.business_id', $business_id)
    ->where('p.is_inactive', 0)
    ->whereNotNull('vld.variation_id')    // ← Only rows with stock location
    ->whereIn('p.type', ['single', 'variable']);
```

**Tables Joined (6):**

| Alias | Table | Join Type | Purpose |
|-------|-------|-----------|---------|
| — | `variations` | PRIMARY | SKU-level product variants |
| `p` | `products` | INNER | Product master data |
| — | `units` | INNER | Unit names (قطعة, كرتونة, etc.) |
| `vld` | `variation_location_details` | LEFT | Stock quantity cache |
| `l` | `business_locations` | LEFT | Location names |
| `c` | `categories` | LEFT | Category names |
| `pv` | `product_variations` | INNER | Variation group names |

### 4.2 Location Filtering (Lines 1980–2002)

Two layers:
1. **User-level:** If `$permitted_locations != 'all'` → `whereIn('vld.location_id', $permitted_locations)`
2. **Filter-level:** If explicit `$filters['location_id']` → `where('vld.location_id', $location_id)` + joins `product_locations`

### 4.3 Subqueries (Lines 2050–2090)

**Subquery 1 — total_sold (Lines 2054–2057):**
```sql
SELECT SUM(TSL.quantity - TSL.quantity_returned)
FROM transactions
JOIN transaction_sell_lines AS TSL ON transactions.id = TSL.transaction_id
WHERE transactions.status = 'final'
  AND transactions.type = 'sell'
  AND transactions.location_id = vld.location_id
  AND TSL.variation_id = variations.id
```

**Subquery 2 — total_transfered (Lines 2058–2060):**
```sql
SELECT SUM(IF(transactions.type = 'sell_transfer', TSL.quantity, 0))
FROM transactions
JOIN transaction_sell_lines AS TSL ON transactions.id = TSL.transaction_id
WHERE transactions.status = 'final'
  AND transactions.type = 'sell_transfer'
  AND transactions.location_id = vld.location_id
  AND TSL.variation_id = variations.id
```

**Subquery 3 — total_adjusted (Lines 2061–2064):**
```sql
SELECT SUM(IF(transactions.type = 'stock_adjustment', SAL.quantity, 0))
FROM transactions
JOIN stock_adjustment_lines AS SAL ON transactions.id = SAL.transaction_id
WHERE transactions.type = 'stock_adjustment'
  AND transactions.location_id = vld.location_id
  AND SAL.variation_id = variations.id
```

**Subquery 4 — stock_price (Lines 2067–2070) ⚠️ CRITICAL:**
```sql
SELECT SUM(
    COALESCE(
        pl.quantity - (
            pl.quantity_sold
            + pl.quantity_adjusted
            + pl.quantity_returned
            + pl.mfg_quantity_used
        ), 0
    ) * purchase_price_inc_tax
)
FROM transactions
JOIN purchase_lines AS pl ON transactions.id = pl.transaction_id
WHERE (transactions.status = 'received' OR transactions.type = 'purchase_return')
  AND transactions.location_id = vld.location_id
  AND pl.variation_id = variations.id
```

**Formula:**
```
stock_price = Σ (remaining_qty × purchase_price_inc_tax)
where remaining_qty = quantity - quantity_sold - quantity_adjusted - quantity_returned - mfg_quantity_used
```

**Subquery 5 — stock (Line 2071):**
```sql
SUM(vld.qty_available) as stock
```

### 4.4 GROUP BY

```php
->groupBy('variations.id', 'vld.location_id')
```

One row per variation per location. This is the grain of the report.

### 4.5 Helper: get_pl_quantity_sum_string

**File:** `app/Utils/Util.php` (Lines 1214–1220)

```php
public function get_pl_quantity_sum_string($table_name = '') {
    $table_name = !empty($table_name) ? $table_name . '.' : '';
    return $table_name . 'quantity_sold + '
         . $table_name . 'quantity_adjusted + '
         . $table_name . 'quantity_returned + '
         . $table_name . 'mfg_quantity_used';
}
```

This helper is used throughout the ERP to compute "consumed quantity" from purchase lines.

---

## 5. Utility Layer — TransactionUtil::getOpeningClosingStock

**File:** `app/Utils/TransactionUtil.php` (Lines 4227–4303)

This is **Engine #2** — powers the widget summary.

### 5.1 Base Query

```php
$query = PurchaseLine::join('transactions as purchase', 'purchase_lines.transaction_id', '=', 'purchase.id')
    ->where('purchase.type', '!=', 'purchase_order')
    ->where('purchase.business_id', $business_id);
```

### 5.2 Price Determination

```php
// Purchase price mode (default):
$price_query_part = '(purchase_lines.purchase_price + COALESCE(purchase_lines.item_tax, 0))';

// Sale price mode:
if ($by_sale_price) {
    $price_query_part = 'v.sell_price_inc_tax';
}
```

### 5.3 Additional Joins

```php
$query->leftjoin('variations as v', 'v.id', '=', 'purchase_lines.variation_id')
      ->leftjoin('products as p', 'p.id', '=', 'purchase_lines.product_id');
```

### 5.4 Date Filtering (Lines 4264–4274)

```php
// Closing stock ($is_opening = false):
->whereRaw("date(purchase.transaction_date) <= '$date'")

// Opening stock ($is_opening = true):
// Same + includes next-day opening_stock transactions
```

### 5.5 THE CORE FORMULA (Lines 4276–4287)

```sql
SELECT SUM(
    (
        purchase_lines.quantity
        - purchase_lines.quantity_returned
        - purchase_lines.quantity_adjusted
        - (
            SELECT COALESCE(SUM(tspl.quantity - tspl.qty_returned), 0)
            FROM transaction_sell_lines_purchase_lines AS tspl
            JOIN transaction_sell_lines AS tsl ON tspl.sell_line_id = tsl.id
            JOIN transactions AS sale ON tsl.transaction_id = sale.id
            WHERE tspl.purchase_line_id = purchase_lines.id
              AND date(sale.transaction_date) <= '$date'
        )
    ) * {price_query_part}
) as stock
```

**Expanded:**
```
remaining_qty = quantity
              - quantity_returned
              - quantity_adjusted
              - sold_qty_linked    ← LIVE subquery against link table

stock_value = Σ(remaining_qty × price)

where price = purchase_price + item_tax          (purchase mode)
   or   price = variations.sell_price_inc_tax    (sale mode)
```

### 5.6 Key Difference from Engine #1

| Aspect | Engine #1 (getProductStockDetails) | Engine #2 (getOpeningClosingStock) |
|--------|-------------------------------------|-------------------------------------|
| **Sold qty source** | `pl.quantity_sold` (denormalized column) | Live subquery on `transaction_sell_lines_purchase_lines` |
| **Location filter** | Correlated subquery per row | WHERE clause on main query |
| **Scope** | Per variation × location | Global aggregate |
| **Date filter** | None (current state) | `<= today` |
| **Transaction filter** | `status='received' OR type='purchase_return'` | `type != 'purchase_order'` |
| **Price mode** | Always `purchase_price_inc_tax` | Configurable: purchase or sale price |

---

## 6. Database Tables & Relationships

### 6.1 Entity Relationship

```
products ──┬── variations ──┬── variation_location_details (VLD)
           │                │
           │                ├── purchase_lines ←── transactions
           │                │
           │                ├── transaction_sell_lines ←── transactions
           │                │
           │                └── variation_group_prices (⚠️ NOT JOINED in stock report)
           │
           ├── product_variations
           ├── categories
           ├── brands
           └── units
```

### 6.2 Table Details

| Table | Rows | Purpose |
|-------|------|---------|
| `products` | 306 | Product master (name, type, category, brand, enable_stock) |
| `variations` | ~370 | SKU-level variants (sell_price_inc_tax, sub_sku) |
| `variation_location_details` | 731 | Stock quantity cache (variation_id × location_id) |
| `purchase_lines` | 1,775 | Purchase/stock ledger (quantity, price, consumption tracking) |
| `transaction_sell_lines` | ~57,895 | Sales line items |
| `transactions` | ~60,000+ | Master transaction records (type, status, location, dates) |
| `variation_group_prices` | 112 | Price-group-specific pricing (⚠️ unused in stock report) |
| `transaction_sell_lines_purchase_lines` | — | Link table: sell lines → purchase lines (FIFO tracking) |

### 6.3 The Dual Stock System

```
┌─────────────────────────────────┐     ┌─────────────────────────────────┐
│  variation_location_details     │     │  purchase_lines                 │
│  (VLD) — The Cache              │     │  — The Ledger                   │
│                                 │     │                                 │
│  qty_available                  │     │  quantity                       │
│  (denormalized, updated by      │     │  - quantity_sold                │
│   transaction events)           │     │  - quantity_returned            │
│                                 │     │  - quantity_adjusted            │
│  Used by: DataTable rows        │     │  - mfg_quantity_used            │
│  ("Current Stock" column)       │     │                                 │
│                                 │     │  Used by: stock_price subquery  │
│  ⚠️ Can diverge from ledger     │     │  & getOpeningClosingStock       │
│                                 │     │                                 │
│  SUM = 176,531                  │     │  Net SUM = 499,974              │
└─────────────────────────────────┘     └─────────────────────────────────┘
                     GAP: 323,443 units (2.83×)
```

---

## 7. View Layer — Blade Templates

### 7.1 Main Template: `report/stock_report.blade.php` (182 lines)

**File:** `resources/views/report/stock_report.blade.php`

#### Structure:
1. **Filters Section (Lines 31–93)** — 6 filter dropdowns + optional manufacturing checkbox
2. **Widget Section (Lines 96–117)** — 4 summary values (permission-gated)
3. **Data Table Section (Lines 118–131)** — Includes partial `report/partials/stock_report_table`
4. **Inline JS (Lines 137–182)** — Loads `report.js`, debug helpers

#### Filters Available:
| Filter | Source | DOM ID |
|--------|--------|--------|
| Location | `$business_locations` | `#location_id` |
| Category | `$categories` | `#category_id` |
| Sub-Category | Dynamic (AJAX) | `#sub_category_id` |
| Brand | `$brands` | `#brand` |
| Unit | `$units` | `#unit` |
| Manufacturing Only | `$show_manufacturing_data` | `#only_mfg_products` |

#### Widget Section:
```html
@can('view_product_stock_value')  <!-- Entire widget hidden without this permission -->
<table>
  <tr>
    <td>المخزون الحالي (بسعر الشراء)</td>
    <td><h3 id="closing_stock_by_pp"></h3></td>  <!-- Empty — filled by JS -->
  </tr>
  <tr>
    <td>المخزون الحالي (بسعر البيع)</td>
    <td><h3 id="closing_stock_by_sp"></h3></td>  <!-- Empty — filled by JS -->
  </tr>
  <tr>
    <td>الربح المحتمل</td>
    <td><h3 id="potential_profit"></h3></td>  <!-- Empty — filled by JS -->
  </tr>
  <tr>
    <td>هامش الربح</td>
    <td><h3 id="profit_margin"></h3></td>  <!-- Empty — filled by JS -->
  </tr>
</table>
@endcan
```

**All 4 widget values are empty on render.** They are populated exclusively by the `get_stock_value()` JavaScript function via AJAX.

### 7.2 Table Partial: `report/partials/stock_report_table.blade.php` (53 lines)

**File:** `resources/views/report/partials/stock_report_table.blade.php`

#### Columns:

| # | Column Header | Permission Gate |
|---|--------------|-----------------|
| 1 | Action | — |
| 2 | SKU | — |
| 3 | Product | — |
| 4 | Variation | — |
| 5 | Category | — |
| 6 | Location | — |
| 7 | Unit Selling Price | — |
| 8 | Current Stock | — |
| 9 | Total Stock Price (by purchase price) | `@can('view_product_stock_value')` |
| 10 | Total Stock Price (by sale price) | `@can('view_product_stock_value')` |
| 11 | Potential Profit | `@can('view_product_stock_value')` |
| 12 | Total Unit Sold | — |
| 13 | Total Unit Transferred | — |
| 14 | Total Unit Adjusted | — |
| 15–18 | Custom Fields 1–4 | — |
| 19 | Current Stock Mfg | `@if($show_manufacturing_data)` |

#### Footer Row:
Contains summary `<td>` elements with classes for JS to populate:
- `.footer_total_stock` — sum of stock column
- `.footer_total_stock_price` — sum of stock_price (gated)
- `.footer_stock_value_by_sale_price` — sum of sale-price values (gated)
- `.footer_potential_profit` — sum of profit (gated)
- `.footer_total_sold`, `.footer_total_transfered`, `.footer_total_adjusted`

---

## 8. JavaScript Layer — DataTable & Widgets

**File:** `public/js/report.js` (1832 lines)

### 8.1 DataTable Initialization (Lines 131–211)

```javascript
stock_report_table = $('#stock_report_table').DataTable({
    processing: true,
    serverSide: true,          // ← Server-side pagination
    ajax: {
        url: '/reports/stock-report',
        data: function(d) {
            d.location_id = $('#location_id').val();
            d.category_id = $('#category_id').val();
            d.sub_category_id = $('#sub_category_id').val();
            d.brand_id = $('#brand').val();
            d.unit_id = $('#unit').val();
            d.only_mfg_products = $('#only_mfg_products').val();
        }
    },
    order: [[1, 'asc']],       // ← Default sort by SKU
    scrollY: "75vh",
    scrollX: true,
    columns: [/* dynamic based on permissions */]
});
```

### 8.2 Column Definitions (Lines 103–129)

Base 8 columns always present:
`action, sku, product, variation, category_name, location_name, unit_price, stock`

Conditional (if user has `view_product_stock_value`):
+ `stock_price, stock_value_by_sale_price, potential_profit`

Then always: `total_sold, total_transfered, total_adjusted`, 4 custom fields

Conditional manufacturing: `total_mfg_stock`

### 8.3 footerCallback (Lines 165–210)

```javascript
footerCallback: function(tfoot, data, start, end, display) {
    var api = this.api();
    // Iterate ONLY current page rows
    for (var r = 0; r < data.length; r++) {
        // Extract data-orig-value from each cell's span
        total_stock += parseFloat($(api.cell(r, 7).node()).find('span').data('orig-value'));
        total_stock_price += parseFloat($(api.cell(r, 8).node()).find('span').data('orig-value'));
        // ... etc for each total column
    }
    // Update footer cells
    $(api.column(7).footer()).html(__currency_trans_from_en(total_stock));
    // ... etc
}
```

**⚠️ CRITICAL:** footerCallback sums **only the current page rows**, not all rows server-side. The widget totals (from `get_stock_value()`) are server-side aggregates of ALL matching rows. These two can differ significantly.

### 8.4 get_stock_value() Function (Lines 1784–1807)

```javascript
function get_stock_value() {
    var data = {
        location_id: $('#location_id').val(),
        category_id: $('#category_id').val(),
        sub_category_id: $('#sub_category_id').val(),
        brand_id: $('#brand').val(),
        unit_id: $('#unit').val(),
    };

    // Show loading spinner in all 4 widget cells
    $('#closing_stock_by_pp').html('<i class="fa fa-spinner fa-spin"></i>');
    $('#closing_stock_by_sp').html('<i class="fa fa-spinner fa-spin"></i>');
    $('#potential_profit').html('<i class="fa fa-spinner fa-spin"></i>');
    $('#profit_margin').html('<i class="fa fa-spinner fa-spin"></i>');

    $.get('/reports/get-stock-value', data, function(result) {
        $('#closing_stock_by_pp').text(__currency_trans_from_en(result.closing_stock_by_pp));
        $('#closing_stock_by_sp').text(__currency_trans_from_en(result.closing_stock_by_sp));
        $('#potential_profit').text(__currency_trans_from_en(result.potential_profit));
        $('#profit_margin').text(__currency_trans_from_en(result.profit_margin, false));
    });
}
```

### 8.5 Filter Change Handlers (Lines 238–250)

```javascript
$('#stock_report_filter_form #location_id, #category_id, #sub_category_id, #brand, #unit, #view_stock_filter')
    .change(function() {
        stock_report_table.ajax.reload();       // Reload DataTable
        stock_expiry_report_table.ajax.reload(); // Also reload expiry report
        get_stock_value();                       // Reload widget totals
    });
```

### 8.6 Initial Call (Lines 1481–1483)

```javascript
if ($('#closing_stock_by_pp').length == 1) {
    get_stock_value();  // Called on DOM ready, only if widget element exists
}
```

---

## 9. Computed Columns — Formulas Reference

### 9.1 DataTable Row Columns (Controller addColumn callbacks)

| Column | Formula | Location |
|--------|---------|----------|
| **stock** | `vld.qty_available` (aggregated) | SQL: Line 2071 |
| **unit_price** | `variations.sell_price_inc_tax` | SQL: Line 2080 |
| **stock_price** | `Σ(pl_net_qty × purchase_price_inc_tax)` | SQL: Lines 2067–2070 |
| **stock_value_by_sale_price** | `stock × (group_price ?? unit_price)` | PHP: Lines 515–521 |
| **potential_profit** | `stock_value_by_sale_price - stock_price` | PHP: Lines 522–529 |
| **total_sold** | `Σ(sell_qty - sell_returned)` | SQL: Lines 2054–2057 |
| **total_transfered** | `Σ(sell_transfer_qty)` | SQL: Lines 2058–2060 |
| **total_adjusted** | `Σ(adjustment_qty)` | SQL: Lines 2061–2064 |

### 9.2 Widget Summary Values

| Widget | Formula | Source |
|--------|---------|--------|
| **المخزون الحالي (بسعر الشراء)** | `Σ(pl_remaining × (purchase_price + item_tax))` | getOpeningClosingStock(by_sale_price=false) |
| **المخزون الحالي (بسعر البيع)** | `Σ(pl_remaining × sell_price_inc_tax)` | getOpeningClosingStock(by_sale_price=true) |
| **الربح المحتمل** | `sale_price_value - purchase_price_value` | Controller: Line 3616 |
| **هامش الربح** | `(profit / sale_price_value) × 100%` | Controller: Line 3617 |

---

## 10. The Two-Engine Problem

This is the **most important architectural finding** in this audit.

### What are the two engines?

| Aspect | Engine #1 (Table Rows) | Engine #2 (Widget Totals) |
|--------|------------------------|---------------------------|
| **Method** | `ProductUtil::getProductStockDetails` | `TransactionUtil::getOpeningClosingStock` |
| **Stock source** | `vld.qty_available` (cache) | `purchase_lines` (ledger) |
| **Price value** | Subquery on `purchase_lines.purchase_price_inc_tax` | `purchase_price + item_tax` (purchase mode) |
| **Sale price value** | `stock × sell_price_inc_tax` (per-row in PHP) | `Σ(remaining × sell_price_inc_tax)` (SQL) |
| **Sold qty** | `pl.quantity_sold` (denormalized) | Live subquery on `tspl` link table |
| **Scope** | Per variation × location | Global SUM |
| **Pagination** | Server-side (DataTables) | N/A (single aggregate) |
| **Date filter** | None | `<= today` |
| **Transaction types** | `status=received OR type=purchase_return` | `type != purchase_order` |

### Why do they diverge?

1. **VLD vs purchase_lines:** `variation_location_details.qty_available` is a denormalized cache maintained by the ERP's transaction processing. It can drift from the `purchase_lines` ledger because:
   - Not all transaction types update VLD properly
   - Custom types (`stock_exchange_authorization`, `stock_add_permission`) may not trigger VLD updates
   - Manual database edits can break synchronization

2. **Denormalized vs live sold qty:** Engine #1 uses `purchase_lines.quantity_sold` (a column that should be incremented on each sale). Engine #2 uses a live subquery against `transaction_sell_lines_purchase_lines` (the actual link between sell lines and purchase lines). If `quantity_sold` isn't updated correctly, these diverge.

3. **Different transaction filters:** Engine #1 excludes transactions where `status != 'received'` (except purchase_return). Engine #2 only excludes `purchase_order`. This means Engine #2 may count transactions that Engine #1 skips.

### Evidence of divergence:

| Metric | Engine #1 | Engine #2 |
|--------|-----------|-----------|
| Total quantity | 176,531 (VLD) | 499,974 (purchase_lines) |
| **Gap** | — | **323,443 units (2.83×)** |

---

## 11. Zero-Value Root Cause Analysis

This section answers: **"Why are المخزون الحالي / قيمة المخزون sometimes zero?"**

### 11.1 Root Cause #1: Zero Stock Quantity (584 of 731 rows)

**584 out of 731 VLD rows** have `qty_available = 0` (79.9%).

When stock = 0, ALL value columns are zero regardless of price:
- `stock_price = 0 × price = 0`
- `stock_value_by_sale_price = 0 × price = 0`
- `potential_profit = 0 - 0 = 0`

**This is normal** — products that have been fully sold or transferred out will show zero stock.

### 11.2 Root Cause #2: Zero Purchase Price (566 of 1,775 lines)

**31.9% of purchase_lines** have `purchase_price_inc_tax = 0`.

When `purchase_price_inc_tax = 0`:
- `stock_price = remaining_qty × 0 = 0` (even if stock > 0!)

**Breakdown by transaction type:**

| Transaction Type | Zero-Price Lines | Reason |
|-----------------|-----------------|--------|
| `stock_exchange_authorization` | 205 | Custom type — transfers between locations, no price |
| `opening_stock` | 151 | Opening balances entered without price |
| `purchase_transfer` | 131 | Transfers from other locations |
| `stock_add_permission` | 71 | Custom type — counterpart to exchange |
| `purchase` | 8 | Regular purchases with missing price |

### 11.3 Root Cause #3: Zero Sell Price (107 variations)

**107 variations** have `sell_price_inc_tax = 0`.

All are "DUMMY" variations — spare parts, accessories, catalogs:
- حله 2000 وات, ماتور خلاط, جوان كبه, etc.

When `sell_price_inc_tax = 0`:
- `stock_value_by_sale_price = stock × 0 = 0`
- `unit_price` column shows 0

### 11.4 Root Cause #4: group_price is Always NULL (Dead Code)

The controller checks:
```php
$unit_selling_price = (float) $row->group_price > 0 ? $row->group_price : $row->unit_price;
```

But `group_price` is **never selected in the SQL query** and there's no Eloquent accessor. Result: always falls back to `unit_price`.

If both `group_price` (null) and `unit_price` (0) are zero, the value is zero.

### 11.5 Root Cause #5: Negative Stock (15 rows)

**15 VLD rows** have negative `qty_available`:
- خلاط هفار 8000 وات → HVAR Bulky: **-126**
- كبه هفار 6.5 لتر → HVAR Bulky: **-93**
- عجان هفار 11 لتر → مخزن اون لاين: **-45**
- فرن هفار 46 لتر → HVAR Bulky: **-17**
- مكملة قطاعة خضار → HVAR Bulky: **-9**

Negative stock × price = negative value, which can cause confusing totals.

### 11.6 Root Cause #6: Widget Sale-Price Value Can Be NULL

The widget's `المخزون الحالي (بسعر البيع)` comes from `getOpeningClosingStock(by_sale_price=true)`, which uses:
```sql
v.sell_price_inc_tax  -- via LEFT JOIN variations
```

Since this is a LEFT JOIN, if a `purchase_line` has no matching variation (data integrity issue), `sell_price_inc_tax` is NULL, and `NULL × qty = NULL`. The SUM of values including NULLs can produce unexpected results.

---

## 12. Dead Code & Bugs

### 12.1 group_price Dead Code (Severity: Medium)

**Location:** `ReportController.php` Lines 517, 524

```php
$unit_selling_price = (float) $row->group_price > 0 ? $row->group_price : $row->unit_price;
```

**Problem:** `$row->group_price` is always NULL because:
1. `getProductStockDetails()` never selects or joins `variation_group_prices`
2. No Eloquent accessor `getGroupPriceAttribute` exists on the Variation model
3. The `variation_group_prices` table (112 entries) is only used in `filterProduct()`, not in stock reports

**Impact:** The selling price group feature has NO effect on stock reports. All `stock_value_by_sale_price` and `potential_profit` calculations use the default `sell_price_inc_tax`.

### 12.2 Denormalized quantity_sold Drift (Severity: High)

**Engine #1** uses `purchase_lines.quantity_sold` (a column updated by application code on each sale).
**Engine #2** uses a live subquery on `transaction_sell_lines_purchase_lines`.

If `quantity_sold` is not updated correctly during a sale (race condition, bug, manual edit), the two engines produce different stock_price values.

### 12.3 VLD Cache Staleness (Severity: High)

`variation_location_details.qty_available` can diverge from the `purchase_lines` ledger. Evidence: **176,531 vs 499,974** — a 323,443 unit gap.

This means the "Current Stock" column may not reflect the true stock position.

### 12.4 footerCallback Only Sums Current Page (Severity: Low)

The DataTable footer sums only visible page rows, not all rows. The widget totals are server-side aggregates. Users may see footer ≠ widget and think there's a bug.

### 12.5 getStockValue Always Uses Today (Severity: Low)

`$end_date = \Carbon::now()->format('Y-m-d')` — hardcoded. No date range parameter from frontend. If a user wants historical stock valuation, this endpoint can't provide it.

---

## 13. Key Statistics

### Database

| Metric | Value |
|--------|-------|
| Total products | 306 |
| Products with stock enabled | 305 |
| Variable products | 0 (all single) |
| VLD rows total | 731 |
| VLD rows with stock > 0 | 132 (18.1%) |
| VLD rows with stock = 0 | 584 (79.9%) |
| VLD rows with stock < 0 | 15 (2.1%) |
| SUM(VLD qty_available) | 176,531 |
| Purchase lines total | 1,775 |
| Purchase lines with price = 0 | 566 (31.9%) |
| Variations with sell_price = 0 | 107 |
| Variation group prices | 112 (unused in stock report) |
| Sell transactions | ~57,895 |

### Dual-System Gap

| System | Total Quantity |
|--------|---------------|
| VLD (cache) | 176,531 |
| Purchase lines (ledger) | 499,974 |
| **Gap** | **323,443 (2.83×)** |

---

## Appendix: File Reference

| File | Lines | Purpose |
|------|-------|---------|
| `routes/web.php` | 658, 686 | Route definitions |
| `app/Http/Controllers/ReportController.php` | 379–582 | getStockReport |
| `app/Http/Controllers/ReportController.php` | 3585–3625 | getStockValue |
| `app/Utils/ProductUtil.php` | 1964–2113 | getProductStockDetails |
| `app/Utils/TransactionUtil.php` | 4227–4303 | getOpeningClosingStock |
| `app/Utils/Util.php` | 1214–1220 | get_pl_quantity_sum_string |
| `resources/views/report/stock_report.blade.php` | 1–182 | Main Blade template |
| `resources/views/report/partials/stock_report_table.blade.php` | 1–53 | Table partial |
| `public/js/report.js` | 103–210, 238–250, 1784–1807, 1481–1483 | DataTable + widgets |
