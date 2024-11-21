from io import BytesIO
from ftplib import FTP
from typing import List


class FTPService:
    def __init__(self, host: str, port: str, username: str, password: str):
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    def connect(self) -> FTP:
        """
        Connects to the FTP server and returns the connection.

        :return: An active FTP connection
        """
        ftp = FTP()
        ftp.connect(self.host, self.port)
        ftp.login(user=self.username, passwd=self.password)
        return ftp

    def list_files_in_directory(self, directory: str) -> List[str]:
        """
        Lists all files and directories in the specified FTP directory.

        :param directory: Directory path on the FTP server
        :return: List of file and directory paths
        """
        with self.connect() as ftp:
            ftp.cwd(directory)
            return ftp.nlst()

    def download_file(self, file_path: str) -> BytesIO:
        """
        Downloads a file from the FTP server and returns it as a BytesIO object.

        :param file_path: Path to the file on the FTP server
        :return: File content as BytesIO
        """
        with self.connect() as ftp:
            bio = BytesIO()
            ftp.retrbinary(f"RETR {file_path}", bio.write)
            bio.seek(0)
            return bio
