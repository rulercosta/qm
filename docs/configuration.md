# Environment Configuration

## Environment Variables

Key environment variables:
```properties
FLASK_ENV=production     # Application environment
LOGS=true               # Enable/disable console logging
LOG_LEVEL=INFO          # Logging verbosity
DATABASE_URL=...        # Database connection string
```

## Setting Up Environment

1. Create a `.env` file in the project root directory
2. Add required environment variables:
```env
FLASK_ENV=development
SECRET_KEY=your_secret_key
SESSION_TYPE=redis
REDIS_HOST=localhost
REDIS_PORT=6379
```
