#  Subscription Management System

A production-style **multi-tenant SaaS subscription system** built with **Django, DRF, and Celery**, featuring clean architecture with service layer separation.

---

##  Project Structure

```
Subscription_Management_System/
│
├── subscription/                # Main app
│   ├── models.py                # Core models (Merchant, Plan, Subscription, etc.)
│   ├── views.py                 # API views
│   ├── serializers.py          # DRF serializers
│   ├── urls.py
│   ├── tasks.py                # Celery tasks (async jobs)
│   ├── utils.py                # Helper utilities
│   ├── api_response.py         # Standardized API responses
│   ├── services/               # Business logic layer
│   │   ├── billing_service.py  # Recurring billing logic
│   │   ├── subscription_service.py
│   │   ├── tenant_service.py   # Multi-tenancy logic
│
├── Subscription_Management_System/
│   ├── celery.py               # Celery configuration
│   ├── settings.py
│   ├── urls.py
│
├── celerybeat-schedule        # Scheduler state (Celery Beat)
├── db.sqlite3
├── manage.py
```

---

##  Overview

This system simulates a real SaaS platform where multiple merchants manage:

- Customers
- Plans
- Subscriptions
- Payments

with full **data isolation (multi-tenancy)** and **automated billing system** using Celery.

---

##  Features

- Multi-tenant architecture (Merchant-based isolation)
- Clean service-layer architecture
- Subscription management system
- Recurring billing using Celery + Celery Beat
- Payment tracking system
- Plan pricing via `PlanCost`
- API response standardization
- Strict ownership validation

---

##  Architecture Highlights

### 1. Service Layer Pattern

Business logic is separated into:

- `billing_service.py` → handles recurring billing logic
- `subscription_service.py` → subscription lifecycle
- `tenant_service.py` → tenant isolation rules

This keeps views clean and scalable.

---

### 2. Celery Integration

- `tasks.py` contains async tasks
- `celery.py` configures worker system
- `celerybeat-schedule` handles periodic jobs

Used for:
- Recurring billing automation
- Background processing

---

##  Recurring Billing

Handled via **Celery task + billing service**:

- Runs periodically using Celery Beat
- Fetches due subscriptions
- Generates payments
- Updates `next_billing_date`
- Uses atomic operations to ensure consistency

---

##  Tenant Isolation

Implemented using:

- Every model linked to `Merchant`
- Centralized logic in `tenant_service.py`
- Query filtering using `request.user.merchant`
- Strict validation on:
  - Plans
  - Subscriptions
  - Payments

No cross-merchant data access allowed.

---

##  Billing Safety

- Prevents duplicate billing per cycle
- Uses existence checks before payment creation
- Atomic transactions prevent partial updates
- Celery ensures async safe execution

---

##  API Overview

### Plans
- `GET /api/plans/`
- `POST /api/plans/`

### Customers
- `GET /api/users/`
- `POST /api/users/`

### Subscriptions
- `POST /api/subscribe/`
- `GET /api/subscriptions/`
- `POST /api/cancel/<id>/`

### Payments
- `GET /api/payments/`

---

##  Tech Stack

- Python
- Django
- Django REST Framework
- Celery
- Celery Beat
- SQLite (dev)

---

##  How to Run

```bash
git clone <repo-url>
cd Subscription_Management_System

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

python manage.py migrate
python manage.py runserver
```

---

##  Run Celery

```bash
celery -A Subscription_Management_System worker -l info
celery -A Subscription_Management_System beat -l info
```

---

##  Test Billing

- Celery Beat scheduler (automatic)
- Or manual execution via shell

---

##  Questions & Answers

### 1. How did you implement recurring billing?

Recurring billing is implemented using **Celery + a billing service layer**. A periodic Celery Beat job triggers a billing task that:

- Fetches active subscriptions due for renewal
- Calls `billing_service.py` to process billing logic
- Creates payment records
- Updates `next_billing_date`
- Runs asynchronously in the background

---

### 2. How do you prevent duplicate charges?

Duplicate charges are prevented by:

- Checking if a payment already exists for the billing period
- Ensuring idempotent logic inside `billing_service`
- Using database-level atomic transactions
- Making Celery tasks safe for retries

---

### 3. How do you ensure tenant isolation?

Tenant isolation is enforced through:

- Every entity linked to `Merchant`
- Centralized checks inside `tenant_service.py`
- Query filtering using `request.user.merchant`
- Strict validation on all create/update operations

This ensures full data separation between merchants.

---

### 4. What would you improve with more time?

- Replace SQLite with PostgreSQL for production readiness
- Add Redis caching layer for performance
- Add retry policies for failed billing attempts
- Integrate real payment gateways (Stripe / Paymob)
- Add RBAC (roles & permissions per merchant)
- Improve observability (logging + monitoring)
- Add full test suite (unit + integration + Celery tests)

---

##  Author

Abdullah Mohsen
