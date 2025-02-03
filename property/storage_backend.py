import uuid
from django.core.files.storage import Storage
from io import BytesIO
from supabase import create_client
from django.conf import settings
import mimetypes

class SupabaseStorage(Storage):
    def __init__(self):
        self.client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
        self.bucket = settings.SUPABASE_STORAGE_BUCKET

    def _open(self, name, mode="rb"):
        response = self.client.storage.from_(self.bucket).download(name)
        return response

    def _save(self, name, content):
        file_data = content.read()  # Read file as bytes
        directory, filename = name.rsplit("/", 1)

        new_filename = f"{filename.split('.')[0]}_{uuid.uuid4()}.{filename.split('.')[-1]}"
        new_name = f"{directory}/{new_filename}"

        # Upload to Supabase
        response = self.client.storage.from_(self.bucket).upload(
            path=new_name,  # File path in storage
            file=file_data,  # Pass BytesIO object
            file_options={"content-type": content.content_type}
        )

        if not response:
            raise ValueError("File upload failed.")

        return self.url(name=new_name)
    
    def exists(self, name):
        files = self.client.storage.from_(self.bucket).list()
        return any(file['name'] == name for file in files)

    def url(self, name):
        return f"{settings.SUPABASE_URL}/storage/v1/object/public/{self.bucket}/{name}"
