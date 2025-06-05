import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospitalmanagement.settings')
django.setup()

from django.contrib.auth.models import User, Group
from hospital.views import ADMIN_GROUP

def create_admin(username, password, email, first_name, last_name):
    try:
        # Create user
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        
        # Create admin group if it doesn't exist
        admin_group, _ = Group.objects.get_or_create(name=ADMIN_GROUP)
        
        # Add user to admin group
        user.groups.add(admin_group)
        
        print(f"Admin account created successfully for {username}")
        return True
    except Exception as e:
        print(f"Error creating admin account: {str(e)}")
        return False

# Create admin account with your desired credentials
create_admin(
    username='hospitaladmin',  # You can change this
    password='Admin@123',      # You can change this
    email='hospital@admin.com',
    first_name='Hospital',
    last_name='Administrator'
) 