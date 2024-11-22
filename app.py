from ftp_service import FTPService
from utils import remove_duplicates

import os
from flask import Flask, jsonify, request
import pandas as pd


app = Flask(__name__)

FTP_CONFIG = {
    "host"      : os.getenv('FTP_HOST'),
    "port"      : int(os.getenv('FTP_PORT')),
    "username"  : os.getenv('FTP_USERNAME'),
    "password"  : os.getenv('FTP_PASSWORD')
}

ftp_service = FTPService(**FTP_CONFIG)


@app.route('/file/list', methods=['GET'])
def list_files():
    """
    List all files in a specific FTP directory.

    Retrieves a list of files stored in the specified FTP directory using the `ftp_service`.

    Returns:
        Response: A JSON response containing:
            - success (bool): Whether the operation was successful.
            - files (list): A list of file names in the directory (if successful).
            - error (str): An error message if the operation fails.

    Status Codes:
        - 200: Successfully retrieved the file list.
        - 500: An error occurred during the operation.
    """
    DIRECTORY = "my_directory"

    try:
        files = ftp_service.list_files_in_directory(DIRECTORY)
        return jsonify({"success": True, "files": files}), 200

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/file/read', methods=['GET'])
def read_file():
    """
    Read and process a specific file from the FTP directory.

    Downloads a file from the FTP server, processes its content using pandas, 
    and returns a preview of the data. Only supports `.csv` and `.xlsx` file formats.

    Query Parameters:
        target_file (str): The name of the target file to read. This parameter is required.

    Returns:
        Response: A JSON response containing:
            - success (bool): Whether the operation was successful.
            - data (list): A preview of the file content as a list of dictionaries (if successful).
            - error (str): An error message if the operation fails or an unsupported file format is provided.

    Status Codes:
        - 200: Successfully processed the file and returned the data preview.
        - 400: Bad request due to missing `target_file` parameter or unsupported file format.
        - 500: An error occurred during the operation.

    Raises:
        Exception: Any error encountered during file download or data processing.
    """
    DIRECTORY = "my_directory"

    target_file = request.args.get('target_file')
    file_path = DIRECTORY + "/" + target_file

    if not file_path:
        return jsonify({"success": False, "error": "target_file parameter is required"}), 400

    try:
        # Download file from FTP
        file_content = ftp_service.download_file(file_path)

        # Read content with pandas
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_content)

        elif file_path.endswith('.xlsx'):
            df = pd.read_excel(file_content)

        else:
            return jsonify({"success": False, "error": "Unsupported file format"}), 400

        # Remove columns with all NaN values
        df = df.dropna(axis=1, how='all')

        # Convert the DataFrame to a list of dictionaries
        data = df.to_dict(orient='records')

        return jsonify({"success": True, "data": data}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/file/column', methods=['GET'])
def get_column():
    """
    Retrieve a unique, non-empty list of values from a specific column in a file stored on the FTP server.

    Downloads the file from the FTP server, processes its content using pandas, and retrieves unique,
    non-empty values from a specified column. Supports `.csv` and `.xlsx` file formats.

    Query Parameters:
        target_file (str): The name of the file to read. This parameter is required.
        target_column (str): The name of the column to retrieve. This parameter is required.

    Returns:
        Response: A JSON response containing:
            - success (bool): Whether the operation was successful.
            - column_data (list): A list of unique, non-empty values from the specified column (if successful).
            - error (str): An error message if the operation fails, the column is not found, or the file format is unsupported.

    Status Codes:
        - 200: Successfully retrieved the column data.
        - 400: Bad request due to missing parameters or unsupported file format.
        - 404: Column not found in the file.
        - 500: An internal server error occurred.

    Raises:
        Exception: Any error encountered during file download or data processing.
    """
    DIRECTORY = "my_directory"

    target_file = request.args.get('target_file')
    target_column = request.args.get('target_column')

    if not target_file:
        return jsonify({"success": False, "error": "target_file parameter is required"}), 400

    if not target_column:
        return jsonify({"success": False, "error": "target_column parameter is required"}), 400

    file_path = DIRECTORY + "/" + target_file

    try:
        # Download file from FTP
        file_content = ftp_service.download_file(file_path)

        # Read content with pandas
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_content)

        elif file_path.endswith('.xlsx'):
            df = pd.read_excel(file_content)

        else:
            return jsonify({"success": False, "error": "Unsupported file format"}), 400

        # Check if the column exists
        if target_column not in df.columns:
            return jsonify({"success": False, "error": f"Column '{target_column}' not found"}), 404

        # Extract the column data
        column_data = df[target_column].dropna().tolist()

        no_duplicates_column_data = remove_duplicates(column_data)

        return jsonify({"success": True, "column_data": no_duplicates_column_data}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
