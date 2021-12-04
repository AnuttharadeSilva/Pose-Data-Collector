from Google import Create_Service
from googleapiclient.http import MediaFileUpload
import csv


class Upload:
    def upload_data(self, file_name):
        CLIENT_SECRET_FILE = 'client_secret_file.json'
        API_NAME = 'drive'
        API_VERSION = 'v3'
        SCOPES = ['https://www.googleapis.com/auth/drive']

        service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
        # print(dir(service))

        folder_id = '1vYRblFCOq-V2A1ZnTIwD8INLlrw2k-g0'

        file_names = [file_name+'.csv', file_name+'.zip']
        mime_types = ['text/csv', 'application/zip']

        for filename, mimetype in zip(file_names, mime_types):
            file_metadata = {'name': filename, 'parents': [folder_id]}

            media = MediaFileUpload('datasets/{0}'.format(filename), mimetype=mimetype)
            service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()