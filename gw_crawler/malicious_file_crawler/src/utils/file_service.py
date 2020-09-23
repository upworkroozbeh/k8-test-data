import os
import uuid
import zipfile

from src.constants import base_unzip_path

from src.constants import zip_path
import os
import zipfile
import collections

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

download_path = file_path = base_unzip_path

bundle_zip_path = zip_path


class FileService:
    """
       File service class for do file operations like zipping unzipping.
    """
    @staticmethod
    def unzip_files(file, key=None):
        """
        Unzip :file to download_path
        """
        try:
            with zipfile.ZipFile(file, "r") as zp:
                path = download_path
                if key:
                    path = download_path + "/" + key
                zp.extractall(path, pwd=bytes(os.environ["vs_zip_pwd"], "utf-8"))
        except Exception:
            raise Exception(f"Error while unzipping file {key}")


    @staticmethod
    def zip_files(files, key=None):
        """
               Zip :from files path and store it in to download_path with key as name of zip
        """
        try:
            fname = download_path + "/" + key + ".zip"
            zipObj = zipfile.ZipFile(fname, "w")
            file_paths = FileService.get_all_file_paths(files)
            for file in file_paths:
                zipObj.write(file, file.split("/")[-1])
            zipObj.close()
        except Exception:
            return None
        else:
            return fname

    @staticmethod
    def get_file_meta(file_path):
        """
            get_file_meta :extract file name and file type
        """
        # initializing empty meta dict
        meta = {}
        try:
            meta["name"] = file_path.split("/")[-1]
            meta["extension"] = file_path.split(".")[-1]
        except Exception:
            return None
        else:
            return meta

    @staticmethod
    def get_all_file_paths(directory):
        """
              get_all_file_paths: get path for all files preset in directory
        """

        # initializing empty file paths list
        file_paths = []
        try:

            # crawling through directory and subdirectories
            for root, directories, files in os.walk(directory):
                for filename in files:
                    # join the two strings in order to form the full filepath.
                    filepath = os.path.join(root, filename)
                    file_paths.append(filepath)
                    # returning all file paths
        except Exception:
            raise Exception("Folder doesnt exist or there is error related to path")
        return file_paths
