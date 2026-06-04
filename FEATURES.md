# Features: Ravelweb Nexus

This document covers every major feature in the system with purpose, workflow, business value,
and technical notes. Proprietary implementation details are not included.

---

## 1. User Authentication

**Purpose:** Secure login for all user types with multiple authentication methods.

**User Workflow:**
1. New user registers with name, email, and password.
2. Email verification is required before access.
3. User logs in with email/password or Google OAuth.
4. On first login, user completes a profile setup step.
5. Session is maintained via an encrypted server-side cookie.

**Business Value:** Each staff member has their own account with their own audit trail.
No shared passwords.

**Technical Notes:**
- Password hashing via Werkzeug PBKDF2.
- Google OAuth 2.0 via Authlib.
- OTP-based email verification with time-limited codes.
- Account lockout after repeated failed login attempts.
- Password recovery via emailed OTP.
- Force-password-change flag for admin-created accounts.

**Edge Cases:**
- Expired OTP codes are rejected; user must request a new one.
- Google OAuth users who sign up before email verification receives a linked account.
- Locked sessions redirect to a lock screen that requires the user's own password.

---

## 2. Shop Request and Onboarding Flow

**Purpose:** New users apply for a business account; superadmin reviews and approves.

**User Workflow:**
1. Registered user submits a shop request with business name and contact details.
2. Request enters a review queue visible only to the superadmin.
3. Superadmin approves the request and generates a license key.
4. User receives the license key and activates it from the settings page.
5. Activation provisions a new database and logs the user into their shop.

**Business Value:** Controlled onboarding. No tenant is provisioned without superadmin
approval.

**Technical Notes:**
- Shop request status: `waiting_for_approval`, `approved`, `rejected`.
- License generation creates a unique key stored in the main database.
- Activation is atomic: if any step fails, the database is dropped and the transaction
  is rolled back.
- Redirect rules prevent unapproved users from accessing business modules.

---

## 3. Role-Based Access Control

**Purpose:** Limit what each staff member can see and do.

**Roles:**
- **Admin:** Full access.
- **Manager:** Access to purchases, reports, employees. No system settings.
- **Salesman:** Sales, quotations, customers only.

**Technical Notes:**
- Role is stored in the session after login.
- `@role_required('Admin', 'Manager')` decorator applied to route handlers.
- Superadmin role is separate and only active in the SaaS admin panel.

---

## 4. Dashboard

**Purpose:** Show the business owner the most important numbers at a glance.

**User Workflow:**
1. Admin opens the application.
2. Dashboard loads with today's sales total, today's purchases, current month's profit,
   and pending customer dues.
3. Chart shows daily sales for the current period.
4. Low-stock alert panel lists products below their threshold.
5. Support reply notifications appear if the platform sent a response.

**Business Value:** Reduces the time needed to understand daily business health.

**Technical Notes:**
- Dashboard period is configurable per tenant (today, this week, this month, this year).
- Chart data served as JSON from a separate endpoint.
- Low-stock calculation uses the `v_product_stock` PostgreSQL view.
- Context processor injects low-stock count into all templates so the notification badge
  stays updated on every page.

---

## 5. Product and Inventory Management

**Purpose:** Maintain a product catalog, track stock, and print barcodes.

**User Workflow:**
1. Admin creates a product with name, category, supplier, cost price, sell price, and barcode.
2. A low-stock alert threshold is set per product.
3. Products appear in sale and purchase flows via live search.
4. Admin can print a barcode label sheet for any set of products.
5. Manual stock adjustments (add or remove) are recorded with a reason.

**Business Value:** Single source of truth for inventory. Barcode printing works without
any external service.

**Technical Notes:**
- Code128-B barcodes are generated entirely server-side in Python. No external barcode
  library is used. The renderer outputs PNG data URIs embedded directly in the HTML/PDF.
- Stock is a computed value from the `v_product_stock` view, not a stored counter.
- Product categories support arbitrary nesting (flat list, one level).
- VAT rate can be set per product for VAT-inclusive reporting.

**Edge Cases:**
- Voided sale invoices do not reduce stock (handled in the stock view by status filter).
- Fractional quantities are supported with a tenant-level toggle.
- Unit types (kg, g, liter, etc.) are configurable per product when fractional mode is on.

---

## 6. Sales Invoices and POS

**Purpose:** Create sale invoices, collect payment, and manage delivery.

**User Workflow:**
1. Salesman opens New Sale.
2. Products are searched by name or barcode with HTMX live results.
3. Each line item shows unit price, quantity, and per-item discount.
4. Invoice totals, discounts, tax, and shipping cost are calculated.
5. Payment method is selected (from the configurable payment method list).
6. Invoice is submitted and saved.
7. Salesman prints the invoice PDF or creates a delivery challan.

**Business Value:** Replaces paper receipts. Due balances are tracked automatically.

**Technical Notes:**
- Invoice numbers are generated by a PostgreSQL trigger on insert.
- HTMX partial template returns product rows for the inline search without a full page reload.
- Delivery challans track shipment status (pending, delivered) separately from invoice payment.
- Sale invoices can be voided. Voiding does not delete the record; it sets `status = 'void'`
  and removes the sale from all stock and ledger calculations.
- Backdated entries are supported when the tenant setting is enabled.
- Advance-dated entries are also toggleable.

**Edge Cases:**
- Voiding a sale that was linked to a delivery challan updates the challan status.
- Customer's credit limit is enforced at sale time if set.
- Walk-in sales (no customer selected) use a `bill_to` text field.

---

## 7. Purchase Invoices

**Purpose:** Record supplier invoices and update inventory.

**User Workflow:**
1. Manager opens New Purchase.
2. Selects a supplier, adds purchased products with quantities and unit cost.
3. Records payment method and amount paid.
4. Submits. Stock increases and supplier ledger updates.

**Business Value:** Tracks supplier payables accurately. Stock is always up to date.

**Technical Notes:**
- A purchase invoice can be linked to a purchase order if one exists for the supplier.
- Partial payment creates an `amount_due` for the supplier ledger.
- Auto-expense entry is created for supplier payments to avoid double-entry in the
  expense register.

---

## 8. Purchase Orders

**Purpose:** Plan procurement before committing to a purchase.

**User Workflow:**
1. Manager creates a purchase order for a supplier with expected delivery date.
2. Line items show ordered quantity and expected unit price.
3. When goods arrive, the PO is converted to a purchase invoice.
4. Partially received quantities are tracked per line item.

**Business Value:** Formal procurement document. Supplier knows what to deliver.
Partial receipt prevents over-receiving.

**Technical Notes:**
- PO status: `draft`, `sent`, `partially_received`, `received`, `cancelled`.
- A PO can be printed as a PDF.
- Receiving a PO auto-fills the purchase invoice form.

---

## 9. Customer Management

**Purpose:** Store customer information and track their financial relationship.

**User Workflow:**
1. Admin creates a customer with contact, address, type (retail/wholesale), and credit limit.
2. An opening balance can be set for customers who already had dues before joining the system.
3. The customer ledger shows every transaction in date order with a running balance.
4. Due collection is recorded as a separate payment entry.

**Business Value:** Owner knows exactly what each customer owes. No separate notebook needed.

**Technical Notes:**
- Customer type (retail/wholesale) affects which sale type defaults are applied.
- Standard discount per customer auto-applies to new sale invoices.
- Priority (normal/high/VIP) is a label field for sorting and filtering.
- Ledger PDF export available for sharing with customers.

---

## 10. Supplier Management

**Purpose:** Store supplier information and track supplier payables.

**User Workflow:** Same structure as customer management, but for suppliers. Tracks what the
business owes each supplier. Supplier payments are recorded separately.

**Technical Notes:**
- Opening balance supports suppliers who had outstanding amounts before the system.
- Supplier ledger includes purchases, returns, and payments.

---

## 11. Customer and Supplier Returns

**Purpose:** Record goods returned by customers or sent back to suppliers.

**User Workflow:**
1. Admin opens Returns, selects the party, and links to the original invoice.
2. Items and quantities are entered.
3. Return invoice is saved. Stock adjusts and ledger updates.

**Business Value:** Correct stock levels even after returns. Ledger stays accurate.

**Technical Notes:**
- Customer returns increase stock. Supplier returns decrease stock.
- Return invoices have their own auto-generated numbers.
- Return amounts appear in ledger and P&L calculations.

---

## 12. Employee Management

**Purpose:** Store employee records and manage monthly salary payments.

**User Workflow:**
1. Admin creates an employee (who is also a system user with a role).
2. Base salary is stored against the employee record.
3. Each month, admin records salary payment with payment type, amount, and date.
4. Salary history is viewable per employee.

**Business Value:** Replaces a paper salary register.

**Technical Notes:**
- Employees are stored as users in the tenant database with the Salesman or Manager role.
- Salary payment creates an auto-expense entry under the 'Salary' cost category.
- Unique constraint on (employee_id, month, year, payment_type) prevents duplicate salary
  entries for the same period.

---

## 13. Expense Tracking

**Purpose:** Record all business outgoings with category classification.

**User Workflow:**
1. Admin creates an expense with title, category, amount, and date.
2. System categories (Salary, Rent, Utilities, Transport, etc.) are pre-seeded.
3. Custom categories can be added.
4. Expenses feed into the P&L report.

**Business Value:** Complete picture of cash outflow alongside sales income.

**Technical Notes:**
- System-generated expenses (from salary payments, supplier payments) are created
  automatically with a unique reference to prevent double-counting.
- A partial unique index on `(ref_type, ref_id)` enforces this at the database level.

---

## 14. Quotations

**Purpose:** Create formal price quotations without committing inventory.

**User Workflow:**
1. Salesman creates a quotation with customer details and line items.
2. Quotation is printed as a PDF and shared with the customer.
3. If accepted, the quotation is converted to a sale invoice with one action.

**Business Value:** Professional price communication without stock reservation risk.

---

## 15. Delivery Challans

**Purpose:** Track physical delivery of goods linked to a sale invoice.

**User Workflow:**
1. Admin creates a challan from a sale invoice.
2. Challan includes delivered items, quantities, and the deliverer's name.
3. Status is updated as the delivery progresses (pending, delivered).

**Business Value:** Formal delivery record. Useful for businesses that dispatch goods
before or after payment.

---

## 16. Financial Vouchers

**Purpose:** Record miscellaneous financial transactions not linked to a sale or purchase.

**Voucher Types:**
- **Debit Voucher:** Money paid out to a customer or supplier.
- **Credit Voucher:** Money received from a customer or supplier.

**User Workflow:** Admin creates a voucher, selects party type and party, enters amount
and payment method. Voucher appears in the ledger.

---

## 17. Production Orders

**Purpose:** Track manufacturing that converts raw materials into finished goods.

**User Workflow:**
1. Manager creates a production order for a finished product with target quantity.
2. Raw material inputs are listed with quantities and unit costs.
3. Order is completed. Raw material stock decreases; finished product stock increases.

**Business Value:** Supports small manufacturers without a separate MRP system.

**Technical Notes:**
- Production module is enabled per tenant via a shop settings toggle.
- Stock movements are recorded as adjustments linked to the production order ID.

---

## 18. Customer Rebates

**Purpose:** Reward loyal customers with annual purchase volume rebates.

**User Workflow:**
1. Admin sets up rebate rules: purchase amount tiers and rebate percentages.
2. At year end, admin calculates which customers qualify.
3. Rebate amounts are approved and paid. Payment is recorded in the ledger.

**Business Value:** Loyalty program without third-party software. Calculated from actual
purchase data.

**Technical Notes:**
- Rebate module is enabled per tenant via a shop settings toggle.
- Rules have min/max purchase amount brackets to create multiple tiers.

---

## 19. Financial Reports

**Purpose:** Give the owner a complete financial picture without manual calculation.

### Profit and Loss Report

Shows total sales, cost of goods sold, gross profit, and net profit after expenses for a
selected date range. Business year start month is configurable per tenant.

### Monthly Summary Report

Month-by-month breakdown of sales and purchases for the financial year.

### Best-Selling Products Report

Products ranked by quantity sold or revenue in a selected period.

### Customer Sales Report

Sales totals per customer for a selected period. Useful for identifying top customers.

### Supplier Purchases Report

Purchase totals per supplier for a selected period.

### VAT Report

Tax-collected and tax-paid summary for VAT filing purposes. Supports both VAT-exclusive
and VAT-inclusive product configurations.

### Full Ledger Report

Complete debit/credit ledger for the business for any date range. Exportable to PDF.

---

## 20. PDF Export

**Purpose:** Generate printable documents for invoices, challans, quotations, and ledgers.

**Technical Notes:**
- Generated server-side using xhtml2pdf.
- Bangla/Bengali language support via a bundled Kalpurush TTF font file.
- Invoice layout respects per-tenant settings: prefix, footer text, logo, currency symbol.
- Ledger PDF shows running balance per page.

---

## 21. Analytics Dashboard

**Purpose:** Visual summary of business performance trends.

**Features:**
- Daily, weekly, monthly, and yearly revenue charts.
- Sales vs. purchases comparison.
- Cash flow summary.
- Configurable default period per tenant.

---

## 22. AI Chat Module

**Purpose:** Let staff ask business questions using a conversational LLM interface.

**User Workflow:**
1. Admin enables AI Chat for their organization (from superadmin panel).
2. Staff member opens the AI Chat panel from the sidebar.
3. User types a question and receives a response from the configured LLM.
4. Usage and cost are logged per organization.

**Business Value:** Platform add-on feature. Per-org budget enforcement keeps costs
under control.

**Technical Notes:**
- Providers: Anthropic Claude, OpenAI GPT, Google Gemini.
- Only one provider is active at a time (configured by superadmin).
- API keys are encrypted with Fernet before storage.
- Monthly spend is checked before each request. If the budget cap is reached, the
  request is blocked with a clear message.
- Usage log stores input tokens, output tokens, and estimated USD cost per session.

---

## 23. Mobile REST API

**Purpose:** Provide all business operations via a JSON API for mobile clients.

**Endpoints Available:**
- Auth: login, logout, refresh token
- Dashboard summary
- Sales: list, create, detail
- Purchases: list, detail
- Products: list, search
- Customers: list, ledger, due collection
- Suppliers: list, payments
- Reports: summary data
- AI Chat passthrough

**Technical Notes:**
- CSRF protection is disabled for this Blueprint (mobile clients cannot send CSRF tokens).
- JWT access tokens expire in 30 minutes. Refresh tokens expire in 7 days.
- Token blacklist via Redis handles logout and forced revocation.
- Rate limiting applied per IP and per user.

---

## 24. SaaS Admin Panel

**Purpose:** Platform operator manages all tenants, licenses, and system configuration.

**Features:**
- Dashboard: total organizations, active tenants, support ticket count.
- Organizations: list all tenants, view details, deactivate or offboard.
- Shop Requests: review and approve/reject incoming requests.
- License Management: generate, revoke, or suspend license keys.
- Admins: add or remove platform admin accounts.
- AI Providers: configure which LLM is active, set API keys, manage per-org AI settings.
- AI Usage: view token and cost usage across all organizations.
- Audit Log: full platform-level action history.
- Support Tickets: respond to in-app support requests from tenants.

**Technical Notes:**
- Superadmin login requires TOTP in addition to password.
- TOTP setup uses `pyotp` and standard TOTP apps (Google Authenticator, etc.).
- Admin actions are logged to a dedicated `admin_audit_log` table in the main database.
- Tenant offboarding drops the tenant database and removes all main-DB references.

---

## 25. Tenant Settings

**Purpose:** Each business configures its own preferences.

**Settings Available:**
- Shop name, address, phone, email, logo.
- Currency (40+ currencies with symbol auto-lookup).
- Currency display format (international grouping, Indian grouping, or no grouping).
- Amount display (decimal or rounded).
- Date format (6 options).
- Tax rate.
- Invoice and challan number prefixes.
- Invoice footer text.
- Dark mode toggle.
- Business year start month.
- Default sale type (retail/wholesale).
- Feature flags: production module, rebate module, fractional quantities.
- Fractional unit types (kg, g, liter, ml, m, ft, etc.).
- Backdated entry permission.
- Advance-dated entry permission.
- Per-tenant SMTP configuration for email notifications.
- Payment method list (add, reorder, enable/disable).
- License key display and renewal.

---

## 26. Audit Log

**Purpose:** Record every write action taken by any user.

**User Workflow:** Admin opens the Audit Log and sees a searchable, paginated list of
actions with user name, module, action type, record ID, description, IP address, and
timestamp.

**Business Value:** Accountability. If something changes unexpectedly, the audit log
shows who did it and when.

---

## 27. Multi-currency and Localization

**Purpose:** Support businesses in different countries with different currencies and
date conventions.

**Features:**
- 40+ currency codes with automatic symbol lookup.
- Custom currency symbol override per tenant.
- Three number grouping formats: international (1,234,567), Indian (12,34,567), none.
- Rounded vs. decimal amount display.
- Six date format options.
- Bangla language support in PDF exports.

---

## 28. Low-Stock Notification System

**Purpose:** Alert staff when products are running low.

**User Workflow:** A bell icon in the navigation bar shows the count of low-stock products.
Clicking it shows the product names and current stock levels.

**Technical Notes:**
- Low-stock count is computed on every request via a context processor.
- Threshold is set per product.
- Stock calculation uses the `v_product_stock` view.

---

## Error and Edge Case Handling

- All database errors in context processors degrade gracefully to safe defaults so the
  page still renders.
- Voided invoices are excluded from all financial calculations.
- Duplicate OTP submissions are rejected with a clear error.
- All form inputs are validated server-side. CSRF tokens are required on all forms.
- Rate limiting protects login, registration, and OTP endpoints from brute-force attacks.
