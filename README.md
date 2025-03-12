# **Password Manager API - Technical Documentation**

## **Project Overview**
The Password Manager API is a secure password storage system built using Django Rest Framework (DRF). It allows users to store and retrieve encrypted passwords for various services securely. The application is containerized using Docker and runs with PostgreSQL as the database backend.

---

## **Features**
- **User Authentication**: Only authenticated users can access password records.
- **Secure Storage**: Passwords are stored in an encrypted format using Fernet encryption.
- **CRUD Operations**:
  - Create a password entry
  - Retrieve a password entry
  - List all stored passwords
- **Search Functionality**: Filter stored passwords by service name.

---

## **Project Structure**
```
.
├── Dockerfile
├── README.md
├── api
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   │   ├── 0001_initial.py
│   │   ├── __init__.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   ├── utils.py
│   └── views.py
├── core
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── docker-compose.yml
├── manage.py
├── requirements.pip
└── template.env
```

---

## **Environment Configuration**
Before running the application, configure the `.env` file based on the provided `template.env`.

### **Template `.env` file**
Create a `.env` file in the project root with the following structure:
```
SECRET_KEY=django_secure_secret_key
POSTGRES_PASSWORD=htencxn0
FERNET_KEY=s00YJBWgTI_NJzDY_UJ3wJapbd7ZFznd1u3RkZ2iBUY=
```

**Environment Variables Explained:**
- `SECRET_KEY`: A Django secret key used for cryptographic signing.
- `POSTGRES_PASSWORD`: The password for the PostgreSQL database.
- `FERNET_KEY`: A key used for encrypting and decrypting stored passwords.

---

## **Setup & Deployment**

### **Prerequisites**
- Docker & Docker Compose installed on your machine.

### **Steps to Run the Project**

1. **Clone the Repository:**
   ```sh
   git clone https://github.com/Plim4ik/password-manager.git
   cd password-manager
   ```

2. **Create the `.env` file:**
   ```sh
   cp template.env .env
   ```
   Update the `.env` file with your configurations.

3. **Build and Run the Containers:**
   ```sh
   docker compose up --build
   ```

5. **Create a Superuser (for Django Admin Panel):**
   ```sh
   docker compose exec app python manage.py createsuperuser
   ```
   Follow the prompts to set up the admin credentials.

6. **Access the API:**
   - API base URL: `http://localhost:8000/api/schema/swagger-ui/`
   - Django Admin: `http://localhost:8000/admin/`

---

## **API Endpoints**


### **Password Management**
| Method | Endpoint                          | Description                     |
|--------|----------------------------------|---------------------------------|
| `GET`  | `/password/`                     | List all stored passwords       |
| `POST` | `/password/<service_name>/`      | Create/update a password entry  |
| `GET`  | `/password/<service_name>/`      | Retrieve a password entry       |

---

## **Testing the API**
Run the test suite inside the container:
```sh
docker-compose exec app python manage.py test
```

---

## **Security Considerations**
- **Encryption:** Passwords are encrypted before being stored in the database using the Fernet encryption key from `.env`.
- **Authentication:** The API requires users to be authenticated to access password-related endpoints.
- **Environment Variables:** Secrets such as `SECRET_KEY` and `FERNET_KEY` should never be hardcoded and must be stored securely.

---

## **Troubleshooting**
| Issue | Solution |
|-------|----------|
| `Database connection error` | Ensure PostgreSQL is running inside Docker and `.env` variables are set correctly. |
| `Authentication failed` | Ensure you provide the correct token in the request headers. |
| `Permission denied` | Make sure the user is authenticated before accessing password-related endpoints. |

---

## **Conclusion**
This API provides a secure and efficient way to manage passwords using encryption and authentication. By leveraging Docker, it is easy to deploy and scale while maintaining a secure environment.

