import os
from azure.storage.blob import BlobServiceClient
from config import connection_string

def upload_to_azure(local_file_path, blob_name, container_name, connection_string):
    # Create a BlobServiceClient using the connection string
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    # Get a container client by name
    container_client = blob_service_client.get_container_client(container_name)

    # Upload the file to Azure Blob Storage
    with open(local_file_path, "rb") as data:
        blob_client = container_client.upload_blob(name=blob_name, data=data)

    print(f"Uploaded {blob_name} to Azure Blob Storage.")

def main():
    # Define Azure Blob Storage details
    container_name = "mailmergecon"
    remote_directory = "mailmerging"

    # Define local directories containing output letters and records
    letters_directory = "../MailMerging/OutputLetters"
    records_directory = "../MailMerging/OutputRecords"

    # Upload text files from the letters directory
    for filename in os.listdir(letters_directory):
        if filename.endswith(".txt"):
            local_file_path = os.path.join(letters_directory, filename)
            blob_name = os.path.join(remote_directory, filename)

            # Upload the file to Azure Blob Storage
            upload_to_azure(local_file_path, blob_name, container_name, connection_string)

    # Upload the TSV file from the records directory
    tsv_file = "Enrollments_20240320235206.tsv"
    local_file_path = os.path.join(records_directory, tsv_file)
    blob_name = os.path.join(remote_directory, tsv_file)

    # Upload the file to Azure Blob Storage
    upload_to_azure(local_file_path, blob_name, container_name, connection_string)

if __name__ == "__main__":
    main()
