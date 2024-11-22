# FTP File Reader API

This project is a Flask-based API for interacting with an FTP server. It allows you to list directories, download files (CSV or Excel), and read their contents using Pandas.

## Features

- **List FTP Directory**: Fetch the list of files and directories in a specified FTP folder.
- **Read Files**: Download CSV or Excel files from the FTP server and return their content as JSON.
- **Retrieve Specific Column**: Extract a unique, non-empty list of values from a specified column in a CSV or Excel file stored on the FTP server.
