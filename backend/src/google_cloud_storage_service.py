from google.cloud import storage

from config import google_storage_cred_file, google_bucket_name, prices_blob_name, classes_blob_name
from constants import pricing_options_path, class_name_lookup_path


class GoogleCloudStorageService:
    #storage_client = storage.Client.from_service_account_json(google_storage_cred_file)
    storage_client = storage.Client()
    bucket = storage_client.bucket(google_bucket_name)

    def _init_(self):
        pass

    def fetch_prices(self):
        prices_blob = self.bucket.blob(prices_blob_name)
        prices_blob.download_to_filename(pricing_options_path)

    def save_prices(self):
        prices_blob = self.bucket.blob(prices_blob_name)
        prices_blob.upload_from_filename(pricing_options_path)
        print('saved')

    def fetch_classes(self):
        blob = self.bucket.blob(classes_blob_name)
        blob.download_to_filename(class_name_lookup_path)

    def save_classes(self):
        prices_blob = self.bucket.blob(classes_blob_name)
        prices_blob.upload_from_filename(class_name_lookup_path)
        print('saved')
