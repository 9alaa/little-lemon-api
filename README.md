# Little Lemon REST API (local learning project)

Django REST Framework API implementing role-based access, menu browsing, carts, and orders. Intended for local development and study, not production.

## Install

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations restaurant
python manage.py migrate
python manage.py seed_lemon
python manage.py createsuperuser
python manage.py runserver
```

## Endpoints

- `POST /auth/users/` — registration (username, password)
- `POST /auth/token/login/` — token login (username, password)
- `GET, POST /api/groups/manager/users` — manager user membership
- `GET, POST /api/groups/delivery-crew/users` — delivery membership
- `GET, POST /api/menu-items` — listing / manager creation
- `GET, PUT, PATCH, DELETE /api/menu-items/<id>` — item operations
- `GET /api/categories` — category browsing
- `GET, POST, DELETE /api/cart/menu-items` — customer's cart
- `GET, POST /api/orders` — role-scoped orders / customer checkout
- `GET, PUT, PATCH, DELETE /api/orders/<id>` — order details / role-limited changes

Authenticate with `Authorization: Token YOUR_TOKEN`. Use test tokens only; do not paste real tokens into assessment answers. All API routes use authentication. Admin uses `is_staff` or `is_superuser`; managers and delivery crew use Django Groups. Users without either group and without staff/superuser flags are customers.

### Examples

```bash
curl -X POST http://127.0.0.1:8000/auth/users/ -H 'Content-Type: application/json' -d '{"username":"student_demo","password":"ChangeMe12345!"}'
curl -X POST http://127.0.0.1:8000/auth/token/login/ -H 'Content-Type: application/json' -d '{"username":"student_demo","password":"ChangeMe12345!"}'
curl -H 'Authorization: Token YOUR_TOKEN' 'http://127.0.0.1:8000/api/menu-items?ordering=price&page=1'
curl -H 'Authorization: Token YOUR_TOKEN' -H 'Content-Type: application/json' -d '{"menuitem":1,"quantity":2}' http://127.0.0.1:8000/api/cart/menu-items
curl -H 'Authorization: Token YOUR_TOKEN' -X POST http://127.0.0.1:8000/api/orders
```

The sample menu is seeded via `seed_lemon`. To assign a manager or delivery crew member, use Django admin or the authenticated group API as an administrator/manager. API list page size is 5.

**Security note:** `DEBUG=True`, a development secret, and relaxed password validators are for local coursework only. Set secure environment configuration before any public deployment.
