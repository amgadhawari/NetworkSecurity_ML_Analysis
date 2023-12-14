from ftplib import FTP

class FTPUploader:
    """
    Uploads files to an FTP server.
    """

    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password

    def upload_file(self, file_path, remote_path):
        """
        Uploads a file to the specified FTP server.
        """
        with FTP(self.host, self.username, self.password) as ftp, open(file_path, 'rb') as file:
            ftp.storbinary(f'STOR {remote_path}', file)
            print(f"File {file_path} uploaded to {self.host}/{remote_path}")

# Example Usage
ftp_uploader = FTPUploader('ftp.example.com', 'your_username', 'your_password')
ftp_uploader.upload_file('/path/to/your/local_file.txt', 'remote/directory/remote_file.txt')
