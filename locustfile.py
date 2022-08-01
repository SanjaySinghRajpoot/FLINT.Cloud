from locust import HttpUser, TaskSet, task, constant
import zipfile
import os
import string
import random
import requests
import json
from pathlib import Path

class TestApiGCBMExample(HttpUser):
    def create_new_sim(self):
        res = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        data = {"title": res}
        new_response = self.client.post("/gcbm/new",data=data)
        return res

    def test_upload(self, title):
        upload_files = (
            self.yield_disturbances_files() 
            + self.yield_classifiers_files()
            + self.yield_db_file() 
            + self.yield_miscellaneous_files()
        )

        upload_response = self.client.post('/gcbm/upload', files=upload_files, data={'title' : title})

    def yield_disturbances_files(self):
        """ This fixture yields a list of classifiers files to be uploaded to the server via \
            gcbm/upload endpoint. Check the local_run.postman_collection in local/rest_api_gcbm """
        disturbances_files_dir = "/home/namyalg/FLINT.Cloud/GCBM_New_Demo_Run/disturbances"
        files = []

        for file in os.listdir(disturbances_files_dir):
            if file.endswith(".tiff"):
                temp = (
                    "disturbances",
                    (
                        file,
                        open(disturbances_files_dir + "/" + file, "rb"),
                        "image/tiff",
                    ),
                )
                files.append(temp)
        return files

    def yield_classifiers_files(self):
        """ This fixture yields a list of classifiers files to be uploaded to the server via \
            gcbm/upload endpoint. Check the local_run.postman_collection in local/rest_api_gcbm """
        classifiers_files_dir = "/home/namyalg/FLINT.Cloud/GCBM_New_Demo_Run/classifiers"

        files = []

        for file in os.listdir(classifiers_files_dir):
            if file.endswith(".tiff"):
                temp = (
                    "classifiers",
                    (
                        file,
                        open(classifiers_files_dir + "/" + file, "rb"),
                        "image/tiff",
                    ),
                )
                files.append(temp)
        return files

    def yield_db_file(self):
        """ This fixture yields a db file to be uploaded to the server via \
            gcbm/upload endpoint. Check the local_run.postman_collection in local/rest_api_gcbm """
        
        db_dir = "/home/namyalg/FLINT.Cloud/GCBM_New_Demo_Run/db"

        files = []

        for file in os.listdir(db_dir):
            if file.endswith(".db"):
                temp = (
                    "db",
                    (file, open(db_dir + "/" + file, "rb"), "application/octet-stream"),
                )
                files.append(temp)

        return files

    def yield_miscellaneous_files(self):
        """ This fixture yields a list of classifiers files to be uploaded to the server via \
            gcbm/upload endpoint. Check the local_run.postman_collection in local/rest_api_gcbm """
        
        miscellaneous_files_dir = "/home/namyalg/FLINT.Cloud/GCBM_New_Demo_Run/miscellaneous"

        files = []

        for file in os.listdir(miscellaneous_files_dir):
            if file.endswith(".tiff"):
                temp = (
                    "miscellaneous",
                    (
                        file,
                        open(miscellaneous_files_dir + "/" + file, "rb"),
                        "image/tiff",
                    ),
                )
                files.append(temp)

        return files

    def start_sim(self, title):
        data = {
            "title": title,
        }
        self.client.post("/gcbm/dynamic", data=data)

    @task(1)
    def run_sim(self):
        title = self.create_new_sim()
        self.test_upload(title)
        self.start_sim(title)
