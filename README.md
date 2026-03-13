# Digital Coupon Marketplace
This is my backend exercise for a coupon marketplace with admin, customer, and reseller flows.
Stack: FastAPI, SQLAlchemy, PostgreSQL, Alembic, Docker, and a minimal HTML/JS frontend.
Products are polymorphic (base Product + Coupon subtype) to support future product types.
Coupon pricing is enforced server-side only.
Formula: minimum_sell_price = cost_price * (1 + margin_percentage / 100).
Customers can view available coupons and buy at minimum_sell_price (no custom price input).
Resellers use Bearer token auth and can buy only if reseller_price >= minimum_sell_price.
All purchase operations are atomic and prevent double-selling on concurrent requests.
Coupon value is returned only after successful purchase.
Admin API supports create, list, get, patch, and delete coupon endpoints.
Reseller API supports list, get by id, and purchase endpoints.
Error format is consistent across domain errors: {"error_code": "...", "message": "..."}.
Common errors: PRODUCT_NOT_FOUND, PRODUCT_ALREADY_SOLD, RESELLER_PRICE_TOO_LOW, UNAUTHORIZED.

Run project: docker-compose up --build

Backend: http://localhost:8000
Swagger: http://localhost:8000/docs
Frontend: open frontend/index.html (or serve it locally).
Env variables in backend/.env: DATABASE_URL, ADMIN_TOKEN, RESELLER_TOKEN.

Token setup: copy backend/.env.example to backend/.env, 
then set ADMIN_TOKEN and RESELLER_TOKEN values there.

Use ADMIN_TOKEN for /api/v1/admin/* endpoints (header: Authorization: Bearer <ADMIN_TOKEN>).
Use RESELLER_TOKEN for /api/v1/products/* reseller endpoints (header: Authorization: Bearer <RESELLER_TOKEN>).

If reseller auth fails, verify the startup seeding ran and that RESELLER_TOKEN in backend/.env matches the token in DB.
Migrations are managed with Alembic and applied on backend container startup.
