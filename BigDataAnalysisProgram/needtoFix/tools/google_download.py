import zipfile
import os

# os.chdir('../')

# def data_download(on):
#     if on is True:
#         URL = ""

#         path_to_zip_file = ''
#         dictionary_to_extract_to = '../'

#         with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
#             zip_ref.extractall(dictionary_to_extract_to)

# import requests

# def download_file_from_google_drive(id, destination):
#     URL = "https://drive.google.com/file/d/1c8oMk-ByAvQxcDV5ZGT5rQMe9pLfvINL/view?usp=sharing"

#     session = requests.Session()

#     response = session.get(URL, params = { 'id' : id }, stream = True)
#     token = get_confirm_token(response)

#     if token:
#         params = { 'id' : id, 'confirm' : token }
#         response = session.get(URL, params = params, stream = True)

#     save_response_content(response, destination)    

# def get_confirm_token(response):
#     for key, value in response.cookies.items():
#         if key.startswith('download_warning'):
#             return value

#     return None

# def save_response_content(response, destination):
#     CHUNK_SIZE = 32768

#     with open(destination, "wb") as f:
#         for chunk in response.iter_content(CHUNK_SIZE):
#             if chunk: # filter out keep-alive new chunks
#                 f.write(chunk)

# if __name__ == "__main__":
#     file_id = '1c8oMk-ByAvQxcDV5ZGT5rQMe9pLfvINL'
#     destination = '../tools.zip'
#     download_file_from_google_drive(file_id, destination)


# from google_drive_downloader import GoogleDriveDownloader as gdd

# gdd.download_file_from_google_drive(file_id='1c8oMk-ByAvQxcDV5ZGT5rQMe9pLfvINL',
#                                     dest_path='../data/raw_data.zip')

import requests

def download_file_from_google_drive(id, destination):
    def get_confirm_token(response):
        for key, value in response.cookies.items():
            if key.startswith('download_warning'):
                return value

        return None

    def save_response_content(response, destination):
        CHUNK_SIZE = 32768

        with open(destination, "wb") as f:
            for chunk in response.iter_content(CHUNK_SIZE):
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)

    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)    


if __name__ == "__main__":
    import sys
    if len(sys.argv) is not 3:
        print("Usage: python google_drive.py drive_file_id destination_file_path")
    else:
        # TAKE ID FROM SHAREABLE LINK
        file_id = sys.argv[1]
        # DESTINATION FILE ON YOUR DISK
        destination = sys.argv[2]
        download_file_from_google_drive(file_id, destination)