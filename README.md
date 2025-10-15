# Brand-Influencer Connector Backend

A FastAPI-based backend system that connects brands with influencers based on tags (niches) and location. This platform enables brands to find relevant influencers and influencers to discover brand collaboration opportunities.

## 🚀 Features

- **Dual User System**: Support for both brands and influencers
- **JWT Authentication**: Secure login and session management
- **Smart Matching**: Connect brands and influencers by tags and location
- **Profile Management**: Update and manage user profiles
- **Reach Verification**: System for verifying influencer reach
- **RESTful APIs**: Clean and well-documented API endpoints

## 🛠️ Tech Stack

- **Framework**: FastAPI
- **Database**: MySQL
- **ORM**: SQLAlchemy
- **Authentication**: JWT (PyJWT)
- **Password Hashing**: bcrypt
- **Data Validation**: Pydantic
- **Server**: Uvicorn

## 📋 Prerequisites

- Python 3.8+
- MySQL Server
- pip (Python package manager)

## 🔧 Installation

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd brand_influencer_backend/backend
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Setup
Create a `.env` file in the root directory:
```env
DATABASE_URL=mysql+pymysql://username:password@localhost:3306/your_database_name
JWT_SECRET=your-super-secret-jwt-key-here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
```

### 5. Database Setup
1. Create a MySQL database
2. Update the `DATABASE_URL` in your `.env` file
3. The tables will be automatically created when you run the application

## 🚀 Running the Application

### Start the Server
```bash
uvicorn main:app --reload
```

The API will be available at: `http://127.0.0.1:8000`

### API Documentation
- **Swagger UI**: `http://127.0.0.1:8000/docs`
- **ReDoc**: `http://127.0.0.1:8000/redoc`

## 📚 API Endpoints

### Authentication
- `POST /auth/signup` - User registration
- `POST /auth/login` - User login

### Influencer Endpoints
- `GET /influencers/filter` - Filter influencers by tag, location, name, reach
- `GET /influencers/suggestions` - Get brand suggestions (requires auth)
- `PUT /influencers/{id}/update` - Update influencer profile (requires auth)
- `POST /influencers/{id}/verify-reach` - Verify influencer reach (brand only)

### Brand Endpoints
- `GET /brands/filter` - Filter brands by name, tag, location, event date
- `GET /brands/trending` - Get trending influencers
- `PUT /brands/{id}/update` - Update brand profile (requires auth)

## 🧪 Testing with Postman

### 1. User Signup (Influencer)
```json
POST http://127.0.0.1:8000/auth/signup
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "password123",
  "tag": "fitness",
  "location": "Los Angeles",
  "role": "influencer"
}
```

### 2. User Login
```json
POST http://127.0.0.1:8000/auth/login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "password123"
}
```

### 3. Update Influencer Profile
```json
PUT http://127.0.0.1:8000/influencers/{user_id}/update
Authorization: Bearer {your_access_token}
Content-Type: application/json

{
  "reach": 50000,
  "verified": true,
  "email": "john.doe@example.com"
}
```

### 4. Get Brand Suggestions
```json
GET http://127.0.0.1:8000/influencers/suggestions
Authorization: Bearer {your_access_token}
```

## 🗄️ Database Schema

### Users Table
- `id` (UUID, Primary Key)
- `name` (VARCHAR)
- `email` (VARCHAR, Unique)
- `password_hash` (VARCHAR)
- `tag` (VARCHAR)
- `location` (VARCHAR)
- `role` (ENUM: 'brand', 'influencer')
- `created_at` (DATETIME)

### Influencers Table
- `id` (UUID, Primary Key)
- `user_id` (UUID, Foreign Key → users.id)
- `reach` (INT)
- `verified` (BOOLEAN)
- `email` (VARCHAR)

### Brands Table
- `id` (UUID, Primary Key)
- `user_id` (UUID, Foreign Key → users.id)
- `name` (VARCHAR)
- `email` (VARCHAR)
- `phone_number` (VARCHAR)
- `tag` (VARCHAR)
- `location` (VARCHAR)
- `event_start` (DATE)
- `event_end` (DATE)

## 🔐 Authentication Flow

1. **Signup**: User creates account with role (brand/influencer)
2. **Login**: User authenticates and receives JWT token
3. **Protected Routes**: Include `Authorization: Bearer {token}` header
4. **Token Validation**: System validates JWT and checks user permissions

## 📁 Project Structure

```
backend/
├── main.py                 # FastAPI application entry point
├── database.py            # Database connection and configuration
├── requirements.txt       # Python dependencies
├── .env                  # Environment variables (create this)
├── models/               # SQLAlchemy database models
│   ├── __init__.py
│   ├── user.py
│   ├── influencer.py
│   └── brand.py
├── schemas/              # Pydantic schemas for validation
│   ├── __init__.py
│   ├── user_schema.py
│   ├── influencer_schema.py
│   └── brand_schema.py
├── routers/              # API route handlers
│   ├── __init__.py
│   ├── auth_router.py
│   ├── influencer_router.py
│   └── brand_router.py
└── utils/                # Utility functions
    ├── __init__.py
    ├── auth_utils.py
    └── token_utils.py
```

## 🚨 Common Issues

### Database Connection Error
- Ensure MySQL server is running
- Check `DATABASE_URL` in `.env` file
- Verify database credentials

### Import Errors
- Make sure virtual environment is activated
- Run `pip install -r requirements.txt`
- Check Python path and module imports

### JWT Token Issues
- Verify `JWT_SECRET` is set in `.env`
- Check token expiration time
- Ensure proper Authorization header format

## 🔧 Development

### Adding New Endpoints
1. Create route in appropriate router file
2. Add Pydantic schema for validation
3. Update database model if needed
4. Test with Postman

### Database Migrations
- Tables are auto-created on startup
- For schema changes, update models and restart server

## 📝 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | MySQL connection string | Required |
| `JWT_SECRET` | Secret key for JWT tokens | `secret123` |
| `JWT_ALGORITHM` | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration time | `1440` |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions:
- Check the API documentation at `/docs`
- Review the code comments
- Test endpoints with Postman
- Check server logs for error details

---

**Happy Coding! 🚀**
