# Modular Entity and Mapping System

A Django REST Framework backend for managing Vendors, Products, Courses, Certifications, and their mappings. Each entity and each mapping lives in its own Django app. All APIs are built using `APIView` only.

---

## Setup

```bash
git clone https://github.com/Muskan244/django-entity-mapping-api.git
cd django-entity-mapping-api
pip install -r requirements.txt
```

---

## Installed Apps

**Master apps**
- `vendor`
- `product`
- `course`
- `certification`

**Mapping apps**
- `vendor_product_mapping`
- `product_course_mapping`
- `course_certification_mapping`

---

## Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## Run the server

```bash
python manage.py runserver
```

---

## Load sample data

```bash
python manage.py seed_data
```

This creates 3 vendors (Microsoft, AWS, Google), 3 products, 3 courses, 3 certifications, and links them with primary mappings.

---

## API Endpoints

### Vendors
| Method | URL | Description |
|--------|-----|-------------|
| GET | `/api/vendors/` | List all vendors |
| POST | `/api/vendors/` | Create a vendor |
| GET | `/api/vendors/<id>/` | Get a vendor |
| PUT | `/api/vendors/<id>/` | Update a vendor |
| PATCH | `/api/vendors/<id>/` | Partial update |
| DELETE | `/api/vendors/<id>/` | Delete a vendor |

Same pattern applies for `/api/products/`, `/api/courses/`, `/api/certifications/`.

### Mappings
| Method | URL |
|--------|-----|
| GET/POST | `/api/vendor-product-mappings/` |
| GET/PUT/PATCH/DELETE | `/api/vendor-product-mappings/<id>/` |
| GET/POST | `/api/product-course-mappings/` |
| GET/PUT/PATCH/DELETE | `/api/product-course-mappings/<id>/` |
| GET/POST | `/api/course-certification-mappings/` |
| GET/PUT/PATCH/DELETE | `/api/course-certification-mappings/<id>/` |

### Filtering

```
GET /api/vendors/?is_active=true
GET /api/vendor-product-mappings/?vendor_id=1
GET /api/product-course-mappings/?product_id=2
GET /api/course-certification-mappings/?course_id=1
```

---

## API Documentation

- Swagger UI: `http://127.0.0.1:8000/swagger/`
- ReDoc: `http://127.0.0.1:8000/redoc/`

---

## Admin Panel

```bash
python manage.py createsuperuser
```

Then visit `http://127.0.0.1:8000/admin/`.

---

## Example Requests

**Create a vendor**
```bash
curl -X POST http://127.0.0.1:8000/api/vendors/ \
  -H "Content-Type: application/json" \
  -d '{"name": "IBM", "code": "IBM", "description": "IBM Cloud services"}'
```

**Create a vendor-product mapping**
```bash
curl -X POST http://127.0.0.1:8000/api/vendor-product-mappings/ \
  -H "Content-Type: application/json" \
  -d '{"vendor": 1, "product": 1, "primary_mapping": true}'
```

**Filter mappings by vendor**
```bash
curl http://127.0.0.1:8000/api/vendor-product-mappings/?vendor_id=1
```
