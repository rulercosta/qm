from admin.models.models import Users
from app.extensions.extensions import db

def create_admin_user():
    """Create admin user if it doesn't exist"""
    if not Users.query.filter_by(username="admin").first():
        admin_user = Users(
            username="admin",
            email="admin@localhost.com",
            password="0000",
            location="System",
            avatar_url="https://res.cloudinary.com/dmtpkmctr/image/upload/v1739182866/avatars/avatar_1.jpg"
        )
        db.session.add(admin_user)
        db.session.commit()
        return True
    return False
