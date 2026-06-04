# Case Study: Ravelweb Nexus

> A multi-tenant SaaS ERP platform built from scratch for small retail businesses in
> Bangladesh -- replacing manual records with a complete, role-based business management system.

---

## Client / Context

The client is a small retail business owner in Dhaka, Bangladesh. Their business manages
product inventory, buys from multiple suppliers, sells to both walk-in and wholesale
customers, employs several staff members, and tracks daily cash flow.

Before this project, they ran the business across paper ledgers, a WhatsApp group for
stock queries, and a spreadsheet that one person controlled. Every end-of-month calculation
was done manually. The owner had no reliable answer to "how much did I make this month?"
without spending two to three hours pulling data together.

The project was designed as a productized SaaS platform, not just a one-off client build.
The goal was to create a system that could serve multiple businesses on the same
infrastructure, each with full data isolation and their own branded experience.

---

## The Challenge

Small retail businesses in Bangladesh lack access to business software that is both
affordable and complete. Enterprise ERP systems are too complex and expensive. Accounting
tools require a trained accountant to operate. POS apps handle sales but not purchasing,
payroll, or reporting.

The result is that business owners use a combination of tools that do not talk to each
other. Stock counts are in one place, supplier dues in another, employee salaries in a
third notebook. Connecting them takes time every day.

### Key Pain Points

- **No single source of truth for stock.** Owners could not answer "how many units do
  I have right now?" without physically counting.

- **Customer due tracking was manual.** Who owes what amount was recorded in a notebook
  that one person controlled. If that person was absent, no one else could answer.

- **Financial reporting was delayed.** Profit and loss was calculated manually, usually
  once a month, and often inaccurately because expense records were incomplete.

- **No role separation for staff.** Every staff member used the same tools with the same
  access. A salesman could see purchase prices, and there was no audit trail if something
  went wrong.

- **Multi-business scaling was impossible.** If a second business or branch opened, the
  process had to start over from scratch with a new spreadsheet.

---

## The Approach

### Discovery Phase

The first step was mapping every operation the business did each week. Sales (walk-in and
wholesale), supplier purchases, customer due collection, employee salary, stock counting,
and end-of-month profit review.

The constraint was that the system had to be usable by staff with no technical background.
It had to work on a basic laptop or tablet. Response time had to be fast even on a slow
internet connection.

A SaaS model was chosen from the start. This meant the engineering decisions had to
account for multiple tenants from day one, not be retrofitted later.

### Architecture Decision

Three multi-tenancy approaches were considered:

1. **Shared database, shared schema** (row-level tenant_id column): Simplest to operate,
   but one missing WHERE clause exposes another tenant's financial data. Not acceptable
   for a financial application.

2. **Shared database, separate schemas** (PostgreSQL schemas per tenant): Better
   isolation, but schema management is complex and PostgreSQL has limitations on
   schema-level connection pooling.

3. **Separate database per tenant:** Maximum isolation. Each business's data is
   physically in its own database. The operational complexity is higher, but the
   security guarantee is absolute.

Option 3 was chosen. The isolation guarantee outweighed the operational cost.

### Engineering Priorities

The priorities in order were: correctness, simplicity, performance.

**Correctness** meant financial numbers had to be accurate. Stock calculations use a
derived view, not a stored counter that can drift. Invoice numbers use database triggers,
not application-side auto-increment that breaks under concurrent writes.

**Simplicity** meant the UI had to work for staff without training. HTMX was used for
interactive features (live product search, inline updates) without the complexity of
building a full single-page application and a separate API layer.

**Performance** meant report queries had to return in under a second for typical business
sizes. Targeted indexes on date and foreign key columns achieved this without caching.

---

## What Was Built

A full-stack web application with a server-side rendered UI and a separate mobile REST API,
running on Docker on a single VPS with automatic tenant provisioning.

### Core Capabilities

- **Sales and purchasing workflows** with live product search, payment tracking, and
  printable PDF invoices in both English and Bangla.

- **Complete ledger system** for every customer and supplier, with running balances,
  opening amounts, and PDF export for sharing.

- **Financial reports** covering profit and loss, VAT, monthly trends, best-selling
  products, and full ledger -- all computed in real time from the source data.

- **Employee and payroll management** with role-based access so a salesman cannot see
  purchase prices or salary information.

- **Multi-tenant SaaS control panel** for the platform operator with TOTP two-factor
  authentication, license management, and per-tenant AI chat configuration.

- **AI chat integration** supporting Anthropic Claude, OpenAI GPT, and Google Gemini
  with per-organization monthly budget caps and encrypted API key storage.

- **Mobile REST API** with JWT authentication for future mobile app clients.

### Technical Highlights

- Database-per-tenant isolation with atomic provisioning and rollback on failure.
- PostgreSQL triggers for gap-free sequential invoice numbering under concurrent writes.
- Server-side barcode generation (Code128-B) without any external barcode service.
- Multi-LLM provider abstraction layer with encrypted key storage and budget enforcement.

---

## Results and Impact

| Metric | Before | After |
|--------|--------|-------|
| Time to get end-of-month P&L | 2 to 3 hours manual | Under 10 seconds |
| Customer due visibility | Paper notebook (one person) | Real-time, any staff member |
| Stock accuracy | Manual weekly count | Real-time calculated view |
| Invoice generation | Handwritten receipt | PDF in under 5 seconds |
| Staff access control | No separation | Role-based, audited |
| Multi-business capability | One-off setup per business | New tenant in under 2 minutes |

The platform now supports multiple businesses on the same infrastructure. Each business
owner can log in, manage their operations, and get financial reports without any
involvement from the platform operator.

---

## Lessons Learned

### What Went Well

- Choosing database-per-tenant from day one was the right call. Adding it later would
  have required migrating all existing data.

- Using PostgreSQL triggers for invoice numbering solved a problem that kept recurring
  in earlier designs (race conditions producing duplicate invoice numbers).

- HTMX was the right UI choice for this audience. Pages feel fast and interactive
  without requiring a separate frontend build pipeline or API layer.

- Writing all SQL as parameterized queries from day one made the codebase consistent
  and prevented an entire class of bugs.

### What I Would Do Differently

- The migration system is a collection of numbered SQL files applied manually. For a
  growing number of tenants, a proper migration runner with tracking and idempotency
  would reduce deployment friction.

- The stock calculation view does subqueries per product. For very large product catalogs
  (thousands of products), this approach would need to be replaced with materialized views
  or incremental aggregation tables.

---

## Technologies Used

Python, Flask 3, PostgreSQL, psycopg2, HTMX, Alpine.js, Tailwind CSS, Redis, Docker,
Gunicorn, Nginx, JWT, pyotp, Authlib, Anthropic SDK, OpenAI SDK, Google Generative AI,
xhtml2pdf, openpyxl, cryptography (Fernet), Flask-WTF, Flask-Limiter

---

## Want to Discuss This Project?

I am available for a private demo and technical walkthrough.

- **LinkedIn:** [linkedin.com/in/salehmdasif](https://linkedin.com/in/salehmdasif)
- **Portfolio:** [asif.ravelweb.com](https://asif.ravelweb.com)
- **Email:** salehmdasif@gmail.com
