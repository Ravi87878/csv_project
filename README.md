# csv_project

# Upload CSV File
Endpoint: POST /api/v1/csv/upload-csv/

Uploads a CSV file for querying.

## Parameters:

file: Multipart form-data containing the CSV file to upload.
Responses:

201 Created: CSV file uploaded successfully.
400 Bad Request: Invalid file format or server error.

# Query CSV Data
Endpoint: GET /api/v1/csv/{pk}/query/

Retrieves and filters CSV data based on query parameters.

## Parameters:

pk: Path parameter specifying the primary key of the CSV file.
Query parameters for filtering:
Example: name=Raj (substring match for 'name' field)
Example: total>100 (numeric comparison for 'total' field)
Example: date>2023-01-01 (date comparison for 'date' field)
Multiple parameters can be combined.
Responses:

200 OK:
Successful response with paginated filtered data.
Optionally includes aggregate values if specified in query parameters (aggregate=field_name:max).
400 Bad Request: Invalid parameters or missing CSV file.
404 Not Found: CSV file not found with the provided primary key.
Example Usage
Upload CSV File:

Use POST /api/v1/csv/{pk}/query/ endpoint in Postman.
Set pk in the path parameter and upload the CSV file using form-data.
Query CSV Data:

Use GET /api/v1/csv/{pk}/query/ endpoint in Postman.
Set pk in the path parameter.
Add query parameters (name=Raj, total>100, etc.) for filtering.
Optionally add aggregate=field_name:max to get aggregate values.
Notes:
Customize the examples (name=Raj, total>100, etc.) to match your specific query parameters and field names in the CSV.
Ensure to specify the correct endpoint paths (/api/csv/{pk}/query/) and handle responses (200 OK, 400 Bad Request, 404 Not Found) as described.
This Markdown documentation can be imported into Postman for clear and structured API documentation that developers can easily reference and use when testing or integrating with your CSV Query API.
