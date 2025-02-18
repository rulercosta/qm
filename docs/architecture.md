# Architecture Overview

## Core Utilities

The application uses two main utility managers for different concerns:

### PathManager (`app/utils/paths.py`)
Handles filesystem and directory structure:
- Template locations
- Static files
- Log directories
- Safe path resolution

```python
from app.utils.paths import paths

# Examples
template_path = paths.get_template_path('pages', 'verify.jinja')
static_file = paths.get_static_path('images', 'logo.png')
logs_dir = paths.logs_path
```

### Settings (`app/utils/settings.py`)
Manages application configuration and behavior:
- Environment settings (dev/prod/test)
- Database configuration
- Logging preferences
- Feature flags

```python
from app.utils.settings import settings

# Examples
if settings.debug:
    # Development-specific code
    pass

db_url = settings.db_url
logging_enabled = settings.logging_enabled
```

### Key Differences

| Feature | PathManager | Settings |
|---------|------------|----------|
| Purpose | File system management | Application configuration |
| Handles | Directory structures, file paths | Environment variables, behavior flags |
| Examples | Template paths, static files | Database URLs, log levels |
| When to use | File operations, path resolution | App behavior, configuration |
