import os
from django.core.files.storage import Storage
from django.core.files.base import ContentFile
from supabase import create_client, Client
import requests

# Initialize Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://your-project-url.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "your-secret-key")
SUPABASE_STORAGE_BUCKET = "media"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

class SupabaseMediaStorage(Storage):
    """Custom Django Storage for Supabase"""

    def _save(self, name, content):
        """Upload file to Supabase"""
        file_data = content.read()
        response = supabase.storage.from_(SUPABASE_STORAGE_BUCKET).upload(name, file_data)

        if response.get("error"):
            raise Exception(f"Supabase Storage Error: {response['error']}")

        return name

    def url(self, name):
        """Return the public URL of the file"""
        return f"{SUPABASE_URL}/storage/v1/object/public/{SUPABASE_STORAGE_BUCKET}/{name}"

    def exists(self, name):
        """Check if a file exists in Supabase"""
        response = supabase.storage.from_(SUPABASE_STORAGE_BUCKET).list()
        return any(file["name"] == name for file in response.get("data", []))

    def delete(self, name):
        """Delete a file from Supabase"""
        response = supabase.storage.from_(SUPABASE_STORAGE_BUCKET).remove([name])
        return response
