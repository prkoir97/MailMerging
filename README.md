## Mail Merging

This repository contains Python scripts designed to automate the process of generating personalized letters for enrolled and disenrolled members in a mock company. 
The system generates personalized letters for individuals according to their enrollment status, utilizing provided templates and mock recipient data and records relevant data into a PostgreSQL database. 
Additionally, it includes functionality to upload generated letters and records to an SFTP server.

### Usage

#### `MailMerging.py`
This script contains the core functionality of the mail merging application. It includes the following main functions:

1. `calculate_months_enrolled(enrollment_date_str, disenrollment_date_str=None)`: Calculates the number of months enrolled based on enrollment and disenrollment dates.
2. `generate_letter(template, data)`: Generates personalized letters based on templates and recipient data.
3. `main()`: Executes the mail merge process, including reading input data, generating letters, and saving output records.

#### `MailMergingData.py`
This script handles the creation of a PostgreSQL database table to store mail merging data and inserts data from the output records file into the table.

#### `STFPFileUpload.py`
This script facilitates the uploading of generated letters and records to an SFTP server. It includes the `upload_to_sftp()` function to upload files and the `main()` function to execute the upload process.

### Dependencies
- Python 3.x
- pandas
- numpy
- psycopg2
- paramiko

### Notes

- `OutputLetters`: Directory where generated letters are saved.
- `OutputRecords`: Directory where TSV file containing mock member data is saved.
- `LetterTemplates`: Directory containing letter templates.
- `InputData`: Directory where TSV file containing enrollment status and other mock memeber data is saved.

## Dependencies
- `os`: Operating system interfaces.
- `csv`: CSV file reading and writing.
- `numpy`: Numerical computing library.
- `pandas`: Data manipulation and analysis library.
- `datetime`: Date and time manipulation.
- `psycopg2`: PostgreSQL adapter for Python.

*** 

### Note
Make sure to adjust file paths and database connection details as per your environment before running the scripts.
