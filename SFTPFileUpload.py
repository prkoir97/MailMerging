import os
import paramiko
from config import password_key

def upload_to_sftp(local_file_path, remote_file_path, hostname, username, password):
    transport = paramiko.Transport((hostname, 22))
    transport.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(transport)

    sftp.put(local_file_path, remote_file_path)

    sftp.close()
    transport.close()

def main():
    # Define SFTP server details
    hostname = "mailmerge.couchdrop.io"
    username = "prkoir97"
    password = (password_key)
    remote_directory = "../MailMerging"

    # Define local directories containing output letters and records
    letters_directory = "../MailMerging/OutputLetters"
    records_directory = "../MailMerging/OutputRecords"

    # Upload text files from the letters directory
    for filename in os.listdir(letters_directory):
        if filename.endswith(".txt"):
            local_file_path = os.path.join(letters_directory, filename)
            remote_file_path = os.path.join(remote_directory, filename)

            # Upload the file to the SFTP server
            upload_to_sftp(local_file_path, remote_file_path, hostname, username, password)
            print(f"Uploaded {filename} to SFTP server.")

    # Upload the TSV file from the records directory
    tsv_file = "Enrollments_20240320152235.tsv"
    local_file_path = os.path.join(records_directory, tsv_file)
    remote_file_path = os.path.join(remote_directory, tsv_file)

    # Upload the file to the SFTP server
    upload_to_sftp(local_file_path, remote_file_path, hostname, username, password)
    print(f"Uploaded {tsv_file} to SFTP server.")

if __name__ == "__main__":
    main()
