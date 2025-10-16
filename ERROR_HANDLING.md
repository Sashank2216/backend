# Error Handling Guide

This document provides a comprehensive guide to all error scenarios in the Brand-Influencer Connector Backend, including HTTP status codes, error messages, and troubleshooting steps.

## 📋 Error Categories

### 🔴 HTTP Status Codes Used

| Status Code | Meaning | When It Occurs |
|-------------|---------|----------------|
| `200` | OK | Successful request |
| `400` | Bad Request | Invalid input data, validation errors |
| `401` | Unauthorized | Missing/invalid authentication |
| `403` | Forbidden | Insufficient permissions |
| `404` | Not Found | Resource doesn't exist |
| `422` | Unprocessable Entity | Pydantic validation errors |
| `500` | Internal Server Error | Server-side errors |

## 🔐 Authentication Errors

### 1. Missing Authorization Header
**Status Code**: `401 Unauthorized`
**Error Message**: `"Missing authorization header"`

**When it happens**:
- Calling protected endpoints without `Authorization` header
- Empty or null authorization header

**Example**:
```json
{
  "detail": "Missing authorization header"
}
```

**How to fix**:
```bash
# Add Authorization header
Authorization: Bearer your_jwt_token_here
```

### 2. Invalid Authorization Header Format
**Status Code**: `401 Unauthorized`
**Error Message**: `"Invalid authorization header"`

**When it happens**:
- Authorization header doesn't follow `Bearer token` format
- Missing "Bearer" prefix
- Malformed header structure

**Example**:
```json
{
  "detail": "Invalid authorization header"
}
```

**How to fix**:
```bash
# Correct format
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...

# Wrong formats
Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...  # Missing Bearer
Authorization: Bearer  # Missing token
```

### 3. Invalid or Expired Token
**Status Code**: `401 Unauthorized`
**Error Message**: `"Invalid or expired token"`

**When it happens**:
- JWT token is malformed
- Token has expired
- Token signature is invalid
- Wrong JWT secret used

**Example**:
```json
{
  "detail": "Invalid or expired token"
}
```

**How to fix**:
1. Get a new token by logging in again
2. Check token expiration time
3. Verify JWT_SECRET in environment variables

### 4. User Not Found
**Status Code**: `401 Unauthorized`
**Error Message**: `"User not found"`

**When it happens**:
- Token is valid but user ID doesn't exist in database
- User was deleted after token was issued

**Example**:
```json
{
  "detail": "User not found"
}
```

**How to fix**:
- Login again to get a fresh token
- Check if user account still exists

## 👤 User Registration Errors

### 1. Invalid Role
**Status Code**: `400 Bad Request`
**Error Message**: `"role must be 'brand' or 'influencer'"`

**When it happens**:
- Role field contains invalid value
- Role is not exactly "brand" or "influencer"

**Example**:
```json
{
  "detail": "role must be 'brand' or 'influencer'"
}
```

**How to fix**:
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "password123",
  "tag": "fitness",
  "location": "Los Angeles",
  "role": "influencer"  // Must be exactly "brand" or "influencer"
}
```

### 2. Email Already Exists
**Status Code**: `400 Bad Request`
**Error Message**: `"Email already exists"`

**When it happens**:
- Trying to register with an email that's already in use
- Case-insensitive email matching

**Example**:
```json
{
  "detail": "Email already exists"
}
```

**How to fix**:
- Use a different email address
- Login with existing account instead

### 3. Invalid Login Credentials
**Status Code**: `401 Unauthorized`
**Error Message**: `"Invalid credentials"`

**When it happens**:
- Wrong email or password
- User doesn't exist
- Password hash doesn't match

**Example**:
```json
{
  "detail": "Invalid credentials"
}
```

**How to fix**:
- Verify email and password
- Check for typos
- Ensure user exists in database

## 🚫 Permission Errors

### 1. Only Influencers Can Access Suggestions
**Status Code**: `403 Forbidden`
**Error Message**: `"Only influencers can access suggestions"`

**When it happens**:
- Brand user tries to access `/influencers/suggestions`
- User role is not "influencer"

**Example**:
```json
{
  "detail": "Only influencers can access suggestions"
}
```

**How to fix**:
- Only influencer accounts can use this endpoint
- Brand users should use `/brands/trending` instead

### 2. Only Brand Users Can Request Verification
**Status Code**: `403 Forbidden`
**Error Message**: `"Only brand users can request verification (MVP)"`

**When it happens**:
- Influencer tries to verify their own reach
- User role is not "brand"

**Example**:
```json
{
  "detail": "Only brand users can request verification (MVP)"
}
```

**How to fix**:
- Only brand accounts can verify influencer reach
- This is by design for MVP

### 3. Only Influencer Role Can Update Profile
**Status Code**: `403 Forbidden`
**Error Message**: `"Only influencer role can update influencer profile"`

**When it happens**:
- Brand user tries to update influencer profile
- Wrong user type for the endpoint

**Example**:
```json
{
  "detail": "Only influencer role can update influencer profile"
}
```

**How to fix**:
- Use correct endpoint for your user type
- Influencers use `/influencers/{id}/update`
- Brands use `/brands/{id}/update`

### 4. Cannot Update Another User's Profile
**Status Code**: `403 Forbidden`
**Error Message**: `"Cannot update another influencer"` or `"Cannot update another brand"`

**When it happens**:
- User tries to update someone else's profile
- Token user ID doesn't match profile user ID

**Example**:
```json
{
  "detail": "Cannot update another influencer"
}
```

**How to fix**:
- Use your own user ID in the URL
- Ensure you're authenticated as the profile owner

### 5. Only Brand Users Can Update Brand Profile
**Status Code**: `403 Forbidden`
**Error Message**: `"Only brand users can update brand profile"`

**When it happens**:
- Influencer tries to update brand profile
- Wrong user type for brand endpoints

**Example**:
```json
{
  "detail": "Only brand users can update brand profile"
}
```

**How to fix**:
- Use correct endpoint for your user type
- Ensure you're registered as a brand

## 🔍 Resource Not Found Errors

### 1. Influencer Not Found
**Status Code**: `404 Not Found`
**Error Message**: `"Influencer not found"`

**When it happens**:
- Trying to verify reach for non-existent influencer
- Invalid influencer ID in URL

**Example**:
```json
{
  "detail": "Influencer not found"
}
```

**How to fix**:
- Verify the influencer ID exists
- Check URL parameters

## 📝 Validation Errors

### 1. Pydantic Validation Errors
**Status Code**: `422 Unprocessable Entity`

**When it happens**:
- Invalid email format
- Missing required fields
- Wrong data types
- Field length violations

**Example**:
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "field required",
      "type": "value_error.missing"
    },
    {
      "loc": ["body", "email"],
      "msg": "value is not a valid email address",
      "type": "value_error.email"
    }
  ]
}
```

**Common validation errors**:

#### Missing Required Fields
```json
{
  "detail": [
    {
      "loc": ["body", "name"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

#### Invalid Email Format
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "value is not a valid email address",
      "type": "value_error.email"
    }
  ]
}
```

#### Wrong Data Type
```json
{
  "detail": [
    {
      "loc": ["body", "reach"],
      "msg": "value is not a valid integer",
      "type": "type_error.integer"
    }
  ]
}
```

## 🗄️ Database Errors

### 1. Connection Errors
**Status Code**: `500 Internal Server Error`

**When it happens**:
- MySQL server is down
- Wrong database credentials
- Network connectivity issues
- Database doesn't exist

**Common error messages**:
- `"Can't connect to MySQL server"`
- `"Access denied for user"`
- `"Unknown database"`

**How to fix**:
1. Check MySQL server status
2. Verify DATABASE_URL in .env file
3. Ensure database exists
4. Check network connectivity

### 2. Foreign Key Constraint Errors
**Status Code**: `500 Internal Server Error`

**When it happens**:
- Trying to create brand/influencer with non-existent user_id
- Database integrity violations

**How to fix**:
- Ensure user exists before creating profile
- Use valid user_id from signup response

## 🔧 Environment Configuration Errors

### 1. Missing Environment Variables
**Status Code**: `500 Internal Server Error`

**When it happens**:
- DATABASE_URL not set
- JWT_SECRET not configured
- Missing .env file

**Error messages**:
- `"DATABASE_URL environment variable not set. See .env"`
- `"JWT_SECRET not found"`

**How to fix**:
1. Create `.env` file in project root
2. Add required environment variables:
```env
DATABASE_URL=mysql+pymysql://username:password@localhost:3306/database_name
JWT_SECRET=your-secret-key-here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
```

## 🧪 Testing Error Scenarios

### Test Authentication Errors
```bash
# Missing Authorization header
curl -X GET http://127.0.0.1:8000/influencers/suggestions

# Invalid token format
curl -X GET http://127.0.0.1:8000/influencers/suggestions \
  -H "Authorization: invalid-token"

# Expired token
curl -X GET http://127.0.0.1:8000/influencers/suggestions \
  -H "Authorization: Bearer expired_token_here"
```

### Test Validation Errors
```bash
# Missing required fields
curl -X POST http://127.0.0.1:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com"}'

# Invalid email format
curl -X POST http://127.0.0.1:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"name": "Test", "email": "invalid-email", "password": "123", "role": "influencer"}'
```

### Test Permission Errors
```bash
# Brand trying to access influencer suggestions
curl -X GET http://127.0.0.1:8000/influencers/suggestions \
  -H "Authorization: Bearer brand_token_here"

# Influencer trying to verify their own reach
curl -X POST http://127.0.0.1:8000/influencers/user_id/verify-reach \
  -H "Authorization: Bearer influencer_token_here"
```

## 🛠️ Error Handling Best Practices

### 1. Client-Side Error Handling
```javascript
// Example JavaScript error handling
try {
  const response = await fetch('/api/influencers/suggestions', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  
  if (!response.ok) {
    const error = await response.json();
    
    switch (response.status) {
      case 401:
        // Redirect to login
        window.location.href = '/login';
        break;
      case 403:
        // Show permission error
        alert('You do not have permission to access this feature');
        break;
      case 404:
        // Show not found error
        alert('Resource not found');
        break;
      default:
        // Show generic error
        alert(`Error: ${error.detail}`);
    }
  }
} catch (error) {
  console.error('Network error:', error);
}
```

### 2. Postman Error Testing
1. **Set up environment variables** for tokens
2. **Create test cases** for each error scenario
3. **Use Pre-request Scripts** to generate invalid tokens
4. **Add Tests** to verify error responses

### 3. Logging and Monitoring
- Monitor 4xx errors for client issues
- Monitor 5xx errors for server issues
- Log authentication failures
- Track validation error patterns

## 📊 Error Response Format

All errors follow this consistent format:
```json
{
  "detail": "Error message here"
}
```

For validation errors (422):
```json
{
  "detail": [
    {
      "loc": ["field", "path"],
      "msg": "Error message",
      "type": "error_type"
    }
  ]
}
```

## 🚨 Quick Troubleshooting Checklist

### Authentication Issues
- [ ] Check Authorization header format
- [ ] Verify token is not expired
- [ ] Ensure user exists in database
- [ ] Check JWT_SECRET configuration

### Permission Issues
- [ ] Verify user role matches endpoint requirements
- [ ] Check if user owns the resource being accessed
- [ ] Ensure correct endpoint for user type

### Validation Issues
- [ ] Check required fields are provided
- [ ] Verify email format is valid
- [ ] Ensure data types match schema
- [ ] Check field length limits

### Database Issues
- [ ] Verify MySQL server is running
- [ ] Check DATABASE_URL configuration
- [ ] Ensure database exists
- [ ] Verify user permissions

---

**Remember**: Always check the server logs for detailed error information during development!
