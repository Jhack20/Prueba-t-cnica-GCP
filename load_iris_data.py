from sklearn.datasets import load_iris
import pandas as pd
from google.cloud import storage
import os

PROJECT_ID = 'project_id'
BUCKET_NAME = 'bucket_name'
GCS_PATH = 'iris_dataset/iris_data.csv'
LOCAL_PATH = 'iris_data.csv'

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Sube un archivo al bucket"""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)
    print(f"Archivo {source_file_name} subido a {destination_blob_name}.")

def save_iris_dataset(local_path):
    """Guarda el dataset Iris como CSV"""
    iris = load_iris()
    df = pd.DataFrame(data= iris.data, columns= iris.feature_names)
    df['target'] = iris.target
    df.to_csv(local_path, index=False)
    print(f"Dataset Iris guardado localmente como {local_path}.")

if __name__ == "__main__":
    save_iris_dataset(LOCAL_PATH)
    upload_blob(BUCKET_NAME, LOCAL_PATH, GCS_PATH)
