import os
import pandas as pd
import numpy as np
from datetime import datetime
from dateutil.relativedelta import relativedelta
import re

# Function to calculate the number of months enrolled based on enrollment and disenrollment dates.
def calculate_months_enrolled(enrollment_date_str, disenrollment_date_str=None):
    try:
        # Convert input date strings to datetime objects if provided
        enrollment_date = pd.to_datetime(enrollment_date_str)
        if pd.isna(disenrollment_date_str):
            disenrollment_date = pd.to_datetime("now")
        elif disenrollment_date_str:
            disenrollment_date = pd.to_datetime(disenrollment_date_str)
        else:
            disenrollment_date = pd.to_datetime("now")

        # Calculate months enrolled accurately using dateutil
        months_enrolled = (
            disenrollment_date.year - enrollment_date.year
        ) * 12 + (disenrollment_date.month - enrollment_date.month)

        if disenrollment_date.day < enrollment_date.day:
            months_enrolled -= 1

        return months_enrolled
    except Exception as e:
        print(f"Error calculating months enrolled: {e}")
        print(f"Enrollment Date: {enrollment_date_str}, Disenrollment Date: {disenrollment_date_str}")
        return None

# Function to generate personalized letters based on templates and recipient data
def generate_letter(template, data):
    letter = template.replace("[Date]", datetime.now().strftime("%Y-%m-%d"))
    for key, value in data.items():
        value_str = str(value)  # Convert value to string
        letter = letter.replace(f"[{key}]", value_str)
    return letter

# Main function to execute the mail merge process
def main():
    input_path = "../MailMerging/InputData"
    output_letter_path = "../MailMerging/OutputLetters"
    output_record_path = "../MailMerging/OutputRecords"
    template_path = "../MailMerging/LetterTemplates"

    for directory in [output_letter_path, output_record_path]:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory: {directory}")

    # Read enrolled and disenrolled templates
    enrolled_template_path = os.path.join(template_path, "EnrolledTemplate.txt")
    disenrolled_template_path = os.path.join(template_path, "DisenrolledTemplate.txt")

    with open(enrolled_template_path, "r") as enrolled_file:
        enrolled_template = enrolled_file.read()

    with open(disenrolled_template_path, "r") as disenrolled_file:
        disenrolled_template = disenrolled_file.read()

    # Define the headers for the output CSV file
    output_csv_header = [
        "MRN",
        "Member_Name",
        "Enrollment_Date",
        "Disenrollment_Date",
        "Months_Enrolled",
        "Address",
        "City",
        "State",
        "Zip",
        "Input_File_Name",
        "Letter_File_Name",
        "Letter_Date_Time",
    ]

    # Initialize a list to store all output data
    output_data = []

    # Loop through files in the input directory
    for filename in os.listdir(input_path):
        if filename.endswith(".tsv"):
            input_file_path = os.path.join(input_path, filename)
            output_file_path = os.path.join(
                output_record_path,
                f"Enrollments_{datetime.now().strftime('%Y%m%d%H%M%S')}.tsv",
            )

            # Define the regex pattern to match date-like substrings
            date_pattern = r"\d{4}_\d{2}_\d{2}"

            # Search for the date-like substring in the filename
            match = re.search(date_pattern, filename)

            # If a match is found, extract the matched date
            if match:
                date_str = match.group(0)
                year, month, day = date_str.split("_")
                enrollment_date_str = f"{year}-{month}-{day}"
            else:
                print("No date found in the filename. Skipping:", filename)
                continue  # Skip processing this file if no date is found

            # Read the input file into a DataFrame
            df = pd.read_csv(input_file_path, delimiter="\t")

            # Add enrollment date column to the DataFrame
            df["Enrollment_Date"] = enrollment_date_str

            # Loop through rows in the DataFrame
            for index, row in df.iterrows():
                mrn = row["MRN"]
                first_name = row["FirstName"]
                last_name = row["LastName"]
                email = row["Email"]
                address = row["Address"]
                city = row["City"]
                state = row["State"]
                zipcode = row["Zipcode"]
                disenrollment_date_str = row["DisenrollmentDate"]

                # Skip individuals without an address
                if pd.isnull(address):
                    print(f"Skipping {first_name} {last_name} - Address missing")
                    # Append data to output data list with "Address Missing"
                    output_data.append(
                        [
                            mrn,
                            f"{first_name} {last_name}",
                            enrollment_date_str,
                            "" if pd.isnull(disenrollment_date_str) else disenrollment_date_str,  # Disenrollment date
                            months_enrolled,  # Months Enrolled
                            "Addresss Missing",  # Address
                            city,
                            state,
                            zipcode,
                            filename,
                            "Missing Address",  # Letter File Name
                            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # Letter Date Time
                        ]
                    )
                    continue  # Skip generating the letter for this individual

                # Convert disenrollment date string to datetime object if it exists
                if not pd.isnull(disenrollment_date_str):
                    disenrollment_date = pd.to_datetime(disenrollment_date_str)
                else:
                    disenrollment_date = None

                # Calculate the number of months enrolled.
                months_enrolled = calculate_months_enrolled(
                    enrollment_date_str, disenrollment_date_str
                )

                recipient_name = (
                    f"{first_name} {last_name}"  # Generate recipient's name
                )
                letter_date_time = datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )  # Get current date and time for letter

                # Determine which template to use
                if disenrollment_date and disenrollment_date < pd.to_datetime("now"):
                    letter_template = disenrolled_template
                else:
                    letter_template = enrolled_template

                # Generate letter filename
                today_date_str = datetime.now().strftime("%Y%m%d")
                letter_file_name = f"{mrn}_{'Disenrolled' if disenrollment_date and disenrollment_date < pd.to_datetime('now') else 'Enrolled'}_{today_date_str}.txt"

                # Generate personalized letter
                letter = generate_letter(
                    letter_template,
                    {
                        "Date": datetime.now().strftime("%Y-%m-%d"),
                        "Recipient_Name": recipient_name,
                        "Address": address,
                        "City": city,
                        "State": state,
                        "Zip": zipcode,
                        "Months_Enrolled": str(months_enrolled),
                    },
                )

                # Write the letter to a file
                with open(
                    os.path.join(output_letter_path, letter_file_name), "w"
                ) as f:
                    f.write(letter)

                # Append data to output data list
                output_data.append(
                    [
                        mrn,
                        recipient_name,
                        enrollment_date_str,
                        disenrollment_date_str if disenrollment_date else "",
                        months_enrolled,
                        address,
                        city,
                        state,
                        zipcode,
                        filename,
                        letter_file_name,
                        letter_date_time,
                    ]
                )

    if output_data:  # Check if output_data is not empty
        output_array = np.array(output_data)
        print("Output Array Size:", output_array.shape)
        output_df = pd.DataFrame(output_array, columns=output_csv_header)
        output_df.to_csv(output_file_path, sep="\t", index=False)
    else:
        print("No data found to create DataFrame.")

    print("Process completed successfully!")

# Execute the main function if this script is run directly
if __name__ == "__main__":
    main()
