# End of Life Software Catalog Creator

This Python script creates a comprehensive catalog of end-of-life software by collecting data from [endoflife.date](https://endoflife.date) API. The data is downloaded and stored in JSONL (JSON Lines) format, making it suitable for analysis, tracking, and integration with data processing tools.

## Features

- Fetches a complete list of software products from the endoflife.date API
- Retrieves detailed end-of-life information for each product
- Exports data in JSONL format, optimized for AWS Glue and other data processing services
- Adds product name to each record for easy identification and filtering

## Requirements

- Python 3.6+
- `requests` library

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/eol-software-catalog.git
cd eol-software-catalog
```

2. Install required packages:
```bash
pip install requests
```

## Usage

Simply run the script:

```bash
python eol_catalog_creator.py
```

The script will:
1. Fetch the list of all products tracked by endoflife.date
2. For each product, retrieve its detailed end-of-life information
3. Format the data as JSONL
4. Save the output to `glue_formatted_data.jsonl` in the current directory

## Output Format

The output file contains each record as a separate line in JSON format. Each record includes:
- Standard fields from the endoflife.date API for that product version
- An additional `product_name` field that identifies which product the record belongs to

Example line from the output file:
```json
{"cycle": "22.04 LTS", "releaseDate": "2022-04-21", "support": "2027-04-21", "eol": "2032-04-21", "latest": "22.04.3", "link": "https://wiki.ubuntu.com/JammyJellyfish/ReleaseNotes", "lts": true, "product_name": "ubuntu"}
```

## Integration with AWS

### AWS Glue Crawler

This data is formatted specifically to work with AWS Glue Crawler:

1. Upload the generated JSONL file to an S3 bucket
2. Configure an AWS Glue Crawler to process the file
3. Run the crawler to create a schema in the AWS Glue Data Catalog
4. Query the data using Amazon Athena

### Sample Athena Queries

Once your data is in AWS Glue Data Catalog, you can run queries like:

```sql
-- Find all products reaching EOL in the next year
SELECT product_name, cycle, eol 
FROM eol_software_catalog 
WHERE eol BETWEEN CURRENT_DATE AND DATE_ADD('year', 1, CURRENT_DATE)
ORDER BY eol;

-- Check support status for a specific product
SELECT cycle, releaseDate, support, eol, latest 
FROM eol_software_catalog 
WHERE product_name = 'windows'
ORDER BY releaseDate DESC;
```

## License

MIT

## Acknowledgements

This project uses the public API provided by [endoflife.date](https://endoflife.date), a community-maintained project to track end-of-life dates for various software products.
