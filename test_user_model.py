import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RentCrew.settings')
django.setup()

from company.models import User, UserManager

# Test creating a user with email
try:
    user = User.objects.create_user(
        email='test@example.com',
        password='testpassword',
        first_name='Test',
        last_name='User',
        role='tester'
    )
    print(f"Successfully created user with email: {user.email}")
    
    # Test authentication
    from django.contrib.auth import authenticate
    auth_user = authenticate(email='test@example.com', password='testpassword')
    if auth_user:
        print(f"Successfully authenticated user: {auth_user.email}")
    else:
        print("Authentication failed")
        
except Exception as e:
    print(f"Error: {e}")