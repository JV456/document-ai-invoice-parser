# Document AI Invoice Parser

`document-ai-invoice-parser` is a Python project that leverages Google Cloud Document AI to process invoices from PDF files and convert the extracted data into JSON format. This tool is designed to streamline the process of extracting and organizing invoice data for further analysis or integration into other systems.

## Features

- Extracts and processes text from PDF invoices using Google Cloud Document AI.
- Converts extracted text into structured JSON format.
- Handles key invoice details such as company information, addresses, itemized charges, totals, and bank details.

## Prerequisites

- Python 3.6 or higher
- Google Cloud account
- Google Cloud SDK
- Document AI API enabled on your Google Cloud project
- A Document AI processor created in your Google Cloud project

## Installation

1. **Clone the repository:**

   ```sh
   git clone https://github.com/your-username/document-ai-invoice-parser.git
   cd document-ai-invoice-parser
2. **Create and activate a virtual environment:**
   ```sh
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
3. **Install the required dependencies:**
   ```sh
   pip install -r requirements.txt
4. **Set up Google Cloud credentials:**
   Ensure you have a credentials.json file with your Google Cloud service account credentials. Set the environment variable to point to this file:
   ```sh
   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/credentials.json"

## Usage Example

### Integrating with a Database

You can easily integrate the extracted invoice data into a database for further analysis or reporting. Here's an example of how to insert the JSON data into a PostgreSQL database using Python:
   ```python
   import psycopg2

   # Connect to the database
   conn = psycopg2.connect(database="your_database", user="your_username", password="your_password", host="your_host", port="your_port")
   cur = conn.cursor()

   # Insert JSON data into the database
   cur.execute("INSERT INTO invoices (data) VALUES (%s)", (json_data,))
   conn.commit()

   # Close the connection
   cur.close()
   conn.close()
 ```

## Generating Report
   You can use the extracted invoice data to generate custom reports or visualizations. Here's an example of how to generate a simple report using Python and          matplotlib:
   ```python
   import matplotlib.pyplot as plt

   # Extract invoice totals
   totals = [invoice['Totals']['Total'] for invoice in invoices]

   # Generate a bar chart of total invoice amounts
   plt.bar(range(len(totals)), totals)
   plt.xlabel('Invoice')
   plt.ylabel('Total Amount')
   plt.title('Invoice Total Amounts')
   plt.show()
   ```

## Roadmap

Here are some potential future enhancements and features planned for `document-ai-invoice-parser`:

- Add support for processing multiple invoices in batch mode.
- Implement a web interface for uploading and processing PDF invoices.
- Integrate with popular accounting or ERP systems for automatic data entry.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgements

This project is made possible thanks to the following resources and tools:

- [Google Cloud Document AI](https://cloud.google.com/document-ai): For providing powerful document processing capabilities.
- [Python](https://www.python.org/): The programming language used to develop this project.
- [Google Cloud SDK](https://cloud.google.com/sdk): For managing Google Cloud resources from the command line.
- [GitHub](https://github.com/): For hosting the project repository and facilitating collaboration.
- [Markdown Guide](https://www.markdownguide.org/): For providing a comprehensive guide on Markdown syntax.
