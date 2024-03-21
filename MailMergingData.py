import psycopg2
from datetime import datetime

# PostgreSQL connection details
host = 'localhost'
database = 'MailMerging'
user = 'postgres'
password = 'password'
port = '5433'

# Establish connection
conn = psycopg2.connect(
    host=host,
    database=database,
    user=user,
    password=password,
    port=port
)

# Create a cursor
cursor = conn.cursor()

# Define the SQL command to create the table
create_table_sql = '''
CREATE TABLE IF NOT EXISTS MailMergingData (
    MRN BIGINT,
    Member_Name VARCHAR(255),
    Enrollment_Date DATE,
    Disenrollment_Date DATE,
    Months_Enrolled INT,
    Address VARCHAR(255),
    City VARCHAR(255),
    State VARCHAR(50),
    Zip VARCHAR(20),
    Input_File_Name VARCHAR(255),
    Letter_File_Name VARCHAR(255),
    Letter_Date_Time TIMESTAMP,
    Insert_Date TIMESTAMP -- New column to record the time of insertion
)
'''

# Execute the SQL command to create the table
cursor.execute(create_table_sql)

# Commit the transaction
conn.commit()

# Read the data from the TSV file
tsv_file_path = '../MailMerging/OutputRecords/Enrollments_20240320235206.tsv'
with open(tsv_file_path, 'r', encoding='utf-8') as tsvfile:
    # Skip the header
    next(tsvfile)
    # Insert data into the table
    for line in tsvfile:
        data = line.strip().split('\t')

        # Handle empty strings in the Disenrollment_Date column
        if data[3] == '':
            data[3] = None  # Replace empty string with None

        data.append(datetime.now())  # Add the current timestamp
        cursor.execute('''
            INSERT INTO MailMergingData
            (MRN, Member_Name, Enrollment_Date, Disenrollment_Date, Months_Enrolled, Address, City, State, Zip, Input_File_Name, Letter_File_Name, Letter_Date_Time, Insert_Date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', data)

# Commit the transaction
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()
