from ftp_service import FTPService

import traceback
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


@app.route('/ftp/list', methods=['GET'])
def list_files():
    """
    Endpoint to list files and directories in a specific FTP directory.

    Query Params:
    - directory: Path to the FTP directory

    :return: JSON response containing the list of files and directories
    """
    directory = request.args.get('directory', '/')

    try:
        files = ftp_service.list_files_in_directory(directory)
        return jsonify({"success": True, "files": files}), 200

    except Exception as e:
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/ftp/read', methods=['GET'])
def read_file():
    """
    Endpoint to download and read a CSV or Excel file from the FTP server.

    Query Params:
    - file_path: Full path to the file on the FTP server

    :return: JSON response containing the file content as rows
    """
    file_path = request.args.get('file_path')
    if not file_path:
        return jsonify({"success": False, "error": "file_path parameter is required"}), 400

    try:
        # Baixar o arquivo do FTP
        file_content = ftp_service.download_file(file_path)

        # Ler o conteúdo com pandas
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_content)
        elif file_path.endswith('.xlsx'):
            df = pd.read_excel(file_content)
        else:
            return jsonify({"success": False, "error": "Unsupported file format"}), 400

        # Converter o DataFrame para uma lista de dicionários
        data = df.to_dict(orient='records')

        return jsonify({"success": True, "data": data}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
