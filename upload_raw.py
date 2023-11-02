import io
from io import BytesIO
import pandas as pd
from google.cloud import storage

def create_bucket(name):
    storage_client = storage.Client.from_service_account_json()
    bucket = storage_client.get_bucket()
    
    data = ''
    blob = bucket.blob(data)
    
    
if __name__ == '__main__':
    create_bucket('raw_data')