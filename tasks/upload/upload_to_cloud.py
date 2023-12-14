import boto3
from botocore.exceptions import NoCredentialsError

class S3Uploader:
    """
    Uploads files to Amazon S3.
    """

    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.s3 = boto3.client('s3')

    def upload_file(self, file_path, s3_file_name):
        """
        Uploads a file to Amazon S3.
        """
        try:
            self.s3.upload_file(file_path, self.bucket_name, s3_file_name)
            print(f"File {file_path} uploaded to {self.bucket_name}/{s3_file_name}")
        except FileNotFoundError:
            print("The file was not found")
        except NoCredentialsError:
            print("Credentials not available")

s3_uploader = S3Uploader('your_bucket_name')
s3_uploader.upload_file('/path/to/your/file.txt', 's3_file_name.txt')
