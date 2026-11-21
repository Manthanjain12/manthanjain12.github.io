# 🛒 Apna Kirana Store - Modular Monolith System

A complete full-stack Kirana Store e-commerce and delivery management platform built with a **centralized Modular Monolith backend** and **three connected interfaces**.

---

## 🌟 Exactly Three Connected Interfaces

| Interface | URL Path | Description | Key Features |
|---|---|---|---|
| **1. Customer E-Commerce Website** | `/` | Responsive Next.js Web Store | • Hindi default language + English toggle<br>• Public browsing without registration<br>• Mobile number + password authentication<br>• Serviceable PIN checker & live stock validation<br>• Cash on Delivery (COD) + Razorpay online payment<br>• Real-time order tracking with complete status history |
| **2. Admin Management Dashboard** | `/admin` | Store Operations Portal | • Analytics overview (Revenue, order pipeline, payment split)<br>• Product CRUD (Hindi + English names, units, stock, Cloudinary)<br>• Category CRUD<br>• Inventory audit trail & low stock alerts<br>• **Manual Delivery Assignment to riders (Req 4)**<br>• **Create delivery personnel accounts (Req 3)**<br>• Store settings: delivery charges & serviceable PIN codes (Req 6) |
| **3. Delivery Person Mobile PWA** | `/delivery` | Touch-Optimized PWA for Riders | • Installable Progressive Web App (`manifest.json` + `sw.js`)<br>• Low-memory optimized for basic Android devices<br>• **Strictly isolated to assigned orders only (Req 5)**<br>• One-touch "Call Customer" (`tel:`) & Navigation<br>• Step transitions: Start Delivery → Mark Delivered<br>• COD cash collection verification & daily earnings summary |

---

## 🏗️ Backend Architecture (Modular Monolith)

Centralized Node.js + TypeScript service (`backend/src`) organized into 12 independent business modules:

```
backend/src/modules/
├── auth/            # Mobile + Password authentication, JWT issue/verify, RBAC
├── user/            # Profile management, saved addresses, delivery rider management
├── category/        # Bilingual Category CRUD, hierarchy & sorting
├── product/         # Bilingual Product catalog, search (Hindi/English), price, stock
├── inventory/       # Low stock alerts, audit trail, atomic transaction adjustments
├── cart/            # Live stock validation, delivery fee calculation, savings
├── order/           # DB transaction placement, atomic stock deduction, duplicate prevention
├── payment/         # Cash on Delivery confirmation, server-side Razorpay signature check
├── delivery/        # Rider-isolated task list, status transitions, COD cash collection
├── notification/    # In-app notifications & SMS/WhatsApp event dispatcher
├── analytics/       # Store metrics, revenue stats, status counts, 7-day trend
└── store-settings/  # Serviceable PIN codes, delivery fee thresholds, store timing
```

---

## 🔑 Default Seed Credentials

Run the database seed script (`npm run seed:backend`) to populate all categories, products, and default accounts:

| Role | Mobile Number | Password | Capabilities |
|---|---|---|---|
| **Store Admin** | `9999999999` | `AdminPassword@123` | Full administrative control, manual delivery assignment, product CRUD, settings |
| **Delivery Rider 1** | `9888888888` | `DeliveryPassword@123` | Assigned orders access, one-tap calling, mark delivered, COD cash collection |
| **Delivery Rider 2** | `9777777777` | `DeliveryPassword@123` | Assigned orders access |
| **Customer** | `9123456789` | `CustomerPassword@123` | Browse, cart, order placement, order history & live tracking |

---

## 🚀 Quick Start & Installation

### 1. Prerequisites
- Node.js 20+
- npm or pnpm
- (Optional) Docker for PostgreSQL & Redis

### 2. Install Dependencies
```bash
# Backend dependencies
cd backend
npm install

# Frontend dependencies
cd ../frontend
npm install
cd ..
```

### 3. Initialize Database & Seed Data
```bash
cd backend
npx prisma db push --schema=./src/prisma/schema.sqlite.prisma
npm run seed
cd ..
```

### 4. Run Development Servers
In two separate terminals:

```bash
# Terminal 1: Backend API (runs on http://localhost:5000)
npm run dev:backend

# Terminal 2: Frontend 3 Interfaces (runs on http://localhost:3000)
npm run dev:frontend
```

Now open:
- **Customer Store**: [http://localhost:3000](http://localhost:3000)
- **Admin Dashboard**: [http://localhost:3000/admin](http://localhost:3000/admin)
- **Delivery Mobile PWA**: [http://localhost:3000/delivery](http://localhost:3000/delivery)

---

## 🧪 Automated Integration Tests

To run the full suite of integration tests verifying all 12 modules, database transactions, duplicate prevention, and role access isolation:

```bash
cd backend
npm test
```

Result:
```
PASS tests/kirana.test.ts
  Kirana Store Modular Monolith Integration Tests
    Requirement 1 & 2: Public Browsing & Customer Registration
      ✓ allows browsing categories and products without authentication
      ✓ registers a new customer with mobile number and password
    Requirement 3: Admin Creates Delivery Personnel
      ✓ admin can create delivery personnel accounts with vehicle info
      ✓ rejects delivery person creation by non-admin users
    Requirement 6: Admin Controls Delivery Charges & Serviceable PINs
      ✓ admin can fetch, add, and toggle serviceable PIN codes
      ✓ admin updates delivery charge rules in store settings
    Requirement 7, 9, 10, 11: Orders, Stock Safety, Transactions & COD
      ✓ validates cart and delivery fee calculation
      ✓ creates an order with COD, decrements stock atomically, and logs status history
      ✓ prevents overselling when requested quantity exceeds available stock
    Requirement 4 & 5: Admin Assigns Orders & Delivery Isolation
      ✓ admin manually assigns the order to delivery personnel
      ✓ delivery personnel can access their assigned orders
      ✓ delivery personnel updates status to OUT_FOR_DELIVERY then DELIVERED with COD collection
    Requirement 8: Online Payment Verification
      ✓ verifies razorpay signature on the server
    Analytics & Inventory Alerts
      ✓ admin can retrieve dashboard analytics with revenue and order breakdown
      ✓ admin can view low stock products and inventory audit logs

Test Suites: 1 passed, 1 total
Tests:       15 passed, 15 total
```

---

## 📦 Production Builds

```bash
# Build backend
npm run build:backend

# Build frontend
npm run build:frontend
```

---

## 🐳 Docker Deployment

To launch the full stack with PostgreSQL and Redis:

```bash
docker compose up -d --build
```
See [DEPLOYMENT.md](DEPLOYMENT.md) for full production deployment instructions.
