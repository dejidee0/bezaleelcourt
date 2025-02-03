from django.core.management import call_command
from django.contrib.auth.models import User

def create_superuser():
    try:
        User.objects.create_superuser('admin', 'admin@gmail.com', 'bezaleelcourt12345@')
        print("Superuser created successfully!")
    except Exception as e:
        print(f"Error creating superuser: {e}")

if __name__ == '__main__':
    create_superuser()