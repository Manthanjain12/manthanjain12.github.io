# Kirana Store Modular Monolith - API Documentation

The centralized backend service runs on port `5000` (base URL: `http://localhost:5000/api/v1`).
All interfaces (Customer Website, Admin Dashboard, Delivery PWA) communicate through this unified REST API.

---

## 1. Authentication Module (`/api/v1/auth`)

Role-based access control with `CUSTOMER`, `ADMIN`, and `DELIVERY` roles. Pass JWT in the `Authorization: Bearer <token>` header.

### 1.1 Register Customer
- **Endpoint**: `POST /api/v1/auth/register`
- **Access**: Public
- **Request Body**:
```json
{
  "name": "Pooja Verma",
  "phone": "9123456789",
  "password": "CustomerPassword@123"
}
```
- **Response**: `201 Created`
```json
{
  "success": true,
  "message": "Registration successful",
  "data": {
    "user": {
      "id": "uuid",
      "phone": "9123456789",
      "name": "Pooja Verma",
      "role": "CUSTOMER"
    },
    "token": "eyJhbGci..."
  }
}
```

### 1.2 Login
- **Endpoint**: `POST /api/v1/auth/login`
- **Access**: Public
- **Request Body**:
```json
{
  "phone": "9999999999",
  "password": "AdminPassword@123"
}
```
- **Response**: `200 OK`

### 1.3 Get Current User Profile
- **Endpoint**: `GET /api/v1/auth/me`
- **Access**: Authenticated (`CUSTOMER`, `ADMIN`, `DELIVERY`)

---

## 2. User Module (`/api/v1/users`)

### 2.1 Get Addresses
- **Endpoint**: `GET /api/v1/users/addresses`
- **Access**: `CUSTOMER`, `ADMIN`

### 2.2 Add Address
- **Endpoint**: `POST /api/v1/users/addresses`
- **Access**: `CUSTOMER`
- **Request Body**:
```json
{
  "name": "Pooja Verma",
  "phone": "9123456789",
  "addressLine1": "Flat 402, Shanti Kunj Apartments",
  "addressLine2": "Near Shivaji Stadium Metro, Connaught Place",
  "city": "New Delhi",
  "state": "Delhi",
  "pinCode": "110001",
  "isDefault": true
}
```

### 2.3 Create Delivery Personnel Account
- **Endpoint**: `POST /api/v1/users/admin/delivery-personnel`
- **Access**: `ADMIN` only
- **Request Body**:
```json
{
  "name": "Raju Sharma",
  "phone": "9888888888",
  "password": "DeliveryPassword@123",
  "vehicleNumber": "DL-4S-AB-1234"
}
```

### 2.4 List Delivery Personnel
- **Endpoint**: `GET /api/v1/users/admin/delivery-personnel`
- **Access**: `ADMIN` only

---

## 3. Category Module (`/api/v1/categories`)

### 3.1 List All Categories
- **Endpoint**: `GET /api/v1/categories`
- **Access**: Public (Bilingual English + Hindi)

### 3.2 Category Details by Slug
- **Endpoint**: `GET /api/v1/categories/:slug`
- **Access**: Public

### 3.3 Create Category (Admin)
- **Endpoint**: `POST /api/v1/categories`
- **Access**: `ADMIN` only
- **Request Body**:
```json
{
  "nameEn": "Dals & Pulses",
  "nameHi": "दालें एवं दाल उत्पाद",
  "slug": "dals-pulses",
  "imageUrl": "https://...",
  "sortOrder": 3
}
```

---

## 4. Product Module (`/api/v1/products`)

### 4.1 Browse Products
- **Endpoint**: `GET /api/v1/products`
- **Access**: Public
- **Query Params**:
  - `category`: Category slug or ID
  - `search`: Query against English or Hindi titles
  - `featured`: `true`
  - `sortBy`: `price_asc` | `price_desc` | `newest` | `name`
  - `page`: 1
  - `limit`: 20

### 4.2 Product Detail by Slug
- **Endpoint**: `GET /api/v1/products/:slug`
- **Access**: Public

### 4.3 Add Product (Admin)
- **Endpoint**: `POST /api/v1/products`
- **Access**: `ADMIN` only
- **Request Body**:
```json
{
  "nameEn": "Aashirvaad Shudh Chakki Atta",
  "nameHi": "आशीर्वाद शुद्ध चक्की आटा",
  "slug": "aashirvaad-shudh-chakki-atta-5kg",
  "categoryId": "uuid",
  "mrp": 260,
  "price": 235,
  "unit": "5 kg",
  "stockQuantity": 50,
  "minStockThreshold": 10,
  "imageUrl": "https://..."
}
```

---

## 5. Inventory Module (`/api/v1/inventory`)

### 5.1 Low Stock Alerts
- **Endpoint**: `GET /api/v1/inventory/low-stock`
- **Access**: `ADMIN` only

### 5.2 Stock Audit Logs
- **Endpoint**: `GET /api/v1/inventory/logs?productId=:id`
- **Access**: `ADMIN` only

### 5.3 Safe Stock Adjustment (Transaction)
- **Endpoint**: `POST /api/v1/inventory/adjust`
- **Access**: `ADMIN` only
- **Request Body**:
```json
{
  "productId": "uuid",
  "quantity": 25,
  "type": "PURCHASE_RESTOCK",
  "reason": "Weekly procurement"
}
```

---

## 6. Cart Module (`/api/v1/cart`)

### 6.1 Validate Cart & Delivery Fee
- **Endpoint**: `POST /api/v1/cart/validate`
- **Access**: Public
- **Request Body**:
```json
{
  "pinCode": "110001",
  "items": [
    { "productId": "uuid", "quantity": 2 }
  ]
}
```
- **Response**: Live stock availability, discount savings, delivery fee calculation, serviceable PIN check.

---

## 7. Order Module (`/api/v1/orders`)

### 7.1 Place Order (Database Transaction)
- **Endpoint**: `POST /api/v1/orders`
- **Access**: `CUSTOMER`
- **Request Body**:
```json
{
  "addressId": "uuid",
  "paymentMethod": "COD",
  "idempotencyKey": "idemp_170123984",
  "notes": "Leave at front gate",
  "items": [
    { "productId": "uuid", "quantity": 1 }
  ]
}
```
- **Features**: Atomic stock deduction, duplicate prevention, order number generation (`KRN-XXXX`), status history initialization.

### 7.2 Customer My Orders
- **Endpoint**: `GET /api/v1/orders/my-orders?page=1`
- **Access**: `CUSTOMER`

### 7.3 Order Tracking Timeline
- **Endpoint**: `GET /api/v1/orders/:id`
- **Access**: Authenticated

### 7.4 Cancel Order
- **Endpoint**: `POST /api/v1/orders/:id/cancel`
- **Access**: `CUSTOMER`, `ADMIN` (Restores inventory atomically)

### 7.5 Manual Delivery Assignment (Admin)
- **Endpoint**: `POST /api/v1/orders/admin/:id/assign`
- **Access**: `ADMIN` only
- **Request Body**:
```json
{
  "deliveryPersonId": "rider_uuid"
}
```

### 7.6 Admin Orders List
- **Endpoint**: `GET /api/v1/orders/admin/all?status=PLACED`
- **Access**: `ADMIN` only

---

## 8. Payment Module (`/api/v1/payment`)

### 8.1 Verify Razorpay Payment (Server-side HMAC)
- **Endpoint**: `POST /api/v1/payment/razorpay/verify`
- **Access**: `CUSTOMER`
- **Request Body**:
```json
{
  "orderId": "uuid",
  "razorpayOrderId": "order_xyz123",
  "razorpayPaymentId": "pay_abc456",
  "razorpaySignature": "hmac_sha256_hash"
}
```

### 8.2 Confirm COD Cash Collection
- **Endpoint**: `POST /api/v1/payment/cod/confirm`
- **Access**: `DELIVERY`, `ADMIN`

---

## 9. Delivery Module (`/api/v1/delivery`)

Strictly isolated so delivery personnel can only query orders assigned to them.

### 9.1 My Assigned Tasks
- **Endpoint**: `GET /api/v1/delivery/orders?type=active`
- **Access**: `DELIVERY` role only
- **Query Params**: `type=active` | `type=completed`

### 9.2 Assigned Order Detail
- **Endpoint**: `GET /api/v1/delivery/orders/:id`
- **Access**: `DELIVERY` role only

### 9.3 Update Delivery Status
- **Endpoint**: `PUT /api/v1/delivery/orders/:id/status`
- **Access**: `DELIVERY` role only
- **Request Body**:
```json
{
  "status": "DELIVERED",
  "cashCollected": true,
  "notes": "Handed over to customer"
}
```

### 9.4 Daily Delivery Summary
- **Endpoint**: `GET /api/v1/delivery/summary`
- **Access**: `DELIVERY` role only

---

## 10. Notification Module (`/api/v1/notifications`)

- `GET /api/v1/notifications`: List in-app notifications
- `PUT /api/v1/notifications/:id/read`: Mark as read
- `PUT /api/v1/notifications/read-all`: Mark all as read

---

## 11. Analytics Module (`/api/v1/analytics`)

### 11.1 Dashboard Overview
- **Endpoint**: `GET /api/v1/analytics/dashboard`
- **Access**: `ADMIN` only
- **Response**: Total sales revenue, today's sales, status counts, payment splits, top products, 7-day trend.

---

## 12. Store Settings Module (`/api/v1/settings`)

### 12.1 Public Store Settings & Banner
- **Endpoint**: `GET /api/v1/settings`
- **Access**: Public

### 12.2 Check PIN Code Serviceability
- **Endpoint**: `GET /api/v1/settings/pincodes/check/:pinCode`
- **Access**: Public

### 12.3 Update Settings (Admin)
- **Endpoint**: `PUT /api/v1/settings`
- **Access**: `ADMIN` only
- **Fields**: `baseDeliveryCharge`, `freeDeliveryMinAmount`, `minOrderAmount`, `isStoreOpen`, `phone`, `bannerHi`, `bannerEn`

### 12.4 Manage Serviceable PIN Codes (Admin)
- `GET /api/v1/settings/pincodes`: List all PIN codes
- `POST /api/v1/settings/pincodes`: Add new serviceable PIN code
- `PUT /api/v1/settings/pincodes/:id`: Update PIN code or toggle active
- `DELETE /api/v1/settings/pincodes/:id`: Remove PIN code
