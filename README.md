# Tally-XML-to-Excel-Converter

Description:

This project provides a solution to process Tally Daybook XML files and generate a structured Excel spreadsheet based on the transactions. The generated Excel file includes only transactions where the voucher type is "Receipt".

Features:

XML Parsing: Extracts transaction details from the input XML file.
Excel Generation: Creates an Excel file in the specified format.
API: A FastAPI-based REST API endpoint to upload an XML file and receive the processed Excel file in response.



Project Structure:

main.py: Contains the FastAPI application and endpoint for XML processing.
requirements.txt: Lists all required packages, including FastAPI and pandas.
sample XML file: A sample XML file for testing purposes.



Testing with Postman:

Set the request method to POST.
URL: http://127.0.0.1:8000/generate-response/
In the body section, select form-data and upload your XML file with the key named file.
Output: The response will be an Excel file that includes only "Receipt" transactions with the specified structure.


Technologies Used:

Python
FastAPI: For creating the API.
pandas: For handling and generating the Excel files.
xml.etree.ElementTree: For parsing XML files.