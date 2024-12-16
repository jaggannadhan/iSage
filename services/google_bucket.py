import os, traceback
from google.cloud import storage
from google.cloud import storage_control_v2

CLOUD_PROJECT_ID =  os.getenv("CLOUD_PROJECT_ID")


class FileUploadService:
    STORAGE_CLIENT = storage.Client(CLOUD_PROJECT_ID)
    STORAGE_CONTROL_CLIENT = storage_control_v2.StorageControlClient()

    def get_bucket(self, bucket_id):
        try:
            bucket = self.STORAGE_CLIENT.get_bucket(bucket_id)
            return bucket, f"Successfully retreived cloud storage bucket: {bucket_id}"
        except Exception:
            print(traceback.format_exc())
            return False, f"Unable to retreive cloud storage bucket: {bucket_id}"
        

    def get_folder(self, bucket_id, folder_name):
        try:
            print(f"Retreving folder: {bucket_id}/{folder_name}")
            folder_path = self.STORAGE_CONTROL_CLIENT.folder_path(
                project="_", bucket=bucket_id, folder=folder_name
            )

            request = storage_control_v2.GetFolderRequest(
                name=folder_path,
            )
            response = self.STORAGE_CONTROL_CLIENT.get_folder(request=request)
            print(f"Get folder response: {response}")
            return response, f"Successfully retrived folder: {bucket_id}/{folder_name}"
        except Exception:
            print(traceback.format_exc())
            return False, f"{bucket_id}/{folder_name} does not exist!"
    

    def create_bucket(self, bucket_id):
        try:
            print(f"Creating cloud storage bucket: {bucket_id}")

            bucket = self.STORAGE_CLIENT.bucket(bucket_id)
            """Creates a bucket with hierarchical namespace enabled."""
            # bucket.iam_configuration.uniform_bucket_level_access_enabled = True
            # bucket.hierarchical_namespace_enabled = True
            bucket.create()

            return bucket, f"Sucessfully created bucket for user: {bucket_id}!"
        except Exception:
            print(traceback.format_exc())
            return False, f"Unable to create bucket for user: {bucket_id}!"
        

    def create_bucket_if_not_exists(self, bucket_id):
        try:
            print(f"In service create_bucket_if_not_exists: {bucket_id}")
            bucket, msg = self.get_bucket(bucket_id)

            if bucket:
                print("Bucket exists")
                return bucket, msg
        
            bucket, msg = self.create_bucket(bucket_id)
            return bucket, msg
        except Exception:
            print(traceback.format_exc())
            return False, f"Unable to create bucket for user: {bucket_id}!"
     
  
    def create_folder(self, bucket_id, folder_name):
        try:
            # The storage bucket path uses the global access pattern, in which the "_"
            # denotes this bucket exists in the global namespace.
            project_path = self.STORAGE_CONTROL_CLIENT.common_project_path("_")
            bucket_path = f"{project_path}/buckets/{bucket_id}"

            request = storage_control_v2.CreateFolderRequest(
                parent=bucket_path,
                folder_id=folder_name,
            )
            response = self.STORAGE_CONTROL_CLIENT.create_folder(request=request)

            print(f"Created folder: {response.name}")
            return True, f"Unable to create folder: {folder_name} in bucket: {bucket_id}!"
        except Exception:
            print(traceback.format_exc())
            return False, f"Unable to create folder: {folder_name} in bucket: {bucket_id}!"
            


    def upload_file(self, bucket_id, file):
        try: 
            fileName = file.filename
            print(f"Uploading {fileName} to Bucket: {bucket_id}")

            # Save file in temp location
            tmp_file_loc = f'/tmp/{fileName}'
            file.save(tmp_file_loc)
            print(f"File saved successfully in temp loc: {tmp_file_loc}")

            try:
                bucket, msg = self.create_bucket_if_not_exists(bucket_id)
                if not bucket:
                    print(msg)
                    raise Exception

                # Get file from bucket
                blob = bucket.blob(f"{fileName}")
                if not blob.exists():
                    blob.upload_from_filename(tmp_file_loc)
                    blob.make_public()
                    msg = f"Successfully uploaded file to {bucket_id}"
                    print(msg)
                else:
                    msg = f"File: {fileName} already exists"

                public_url = blob.public_url
                os.remove(tmp_file_loc)

                return public_url, msg
            except Exception:
                    os.remove(tmp_file_loc)
                    print(traceback.format_exc())
                    return False, f"Unable to upload file to {bucket_id}!"
            
        except Exception:
            print(traceback.format_exc())
            return False, f"Unable to upload file to {bucket_id}!"


    def write_text_to_file(self, bucket_name, file_name, content):
        try:
            print(f"Writing text to {bucket_name}/{file_name}")
            bucket, msg = self.get_bucket(bucket_name)
            if not bucket:
                return False, msg
            blob = bucket.blob(file_name)
            blob.upload_from_string(content)

            # blob.make_public()
            public_url = blob.public_url

            return public_url, f"Successfully added {file_name} to {bucket_name}!"
        except Exception:
            print(traceback.format_exc())
            return False, f"Unable write text to {file_name} in {bucket_name}!"

        
    def get_text_from_file(self, bucket_name, file_name):
        try:
            print(f"Reading text from {bucket_name}/{file_name}")
            bucket, msg = self.get_bucket(bucket_name)
            blob = bucket.get_blob(file_name)
            text = blob.download_as_string()

            if text and isinstance(text, bytes):
                return text.decode("utf-8")
            
            return False, "No text in file!"
        except Exception:
            print(traceback.format_exc())
            return False, f"Unable get text from {file_name} in {bucket_name}!"


    def delete_bucket(self, bucket_id):
        try:
            bucket, msg = self.get_bucket(bucket_id)
            if not bucket:
                return True, msg
            
            bucket.delete()
            return True, f"Bucket {bucket_id} deleted"
        except Exception:
            print(traceback.format_exc())
            return False, f"Unable to delete bucket for user: {bucket_id}!"

