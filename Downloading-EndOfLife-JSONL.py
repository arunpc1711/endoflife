import json
import requests

def get_list_of_all_products(product):
    url = f"https://endoflife.date/api/{product}.json"
    headers = {
        "Accept": "application/json"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Request failed with status code: {response.status_code}")
        return None

def format_for_glue():
    # Get all products
    products = get_list_of_all_products("all")
    
    # Create a file for Glue crawler
    with open('glue_formatted_data.jsonl', 'w') as f:
        for product in products:
            # Get details for each product
            product_details = get_list_of_all_products(product)
            
            if product_details:
                # Ensure product_details is a list
                if not isinstance(product_details, list):
                    product_details = [product_details]
                
                # Write each product detail as a separate JSON line
                for detail in product_details:
                    # Add product name to each record
                    detail['product_name'] = product
                    
                    # Convert to JSON string and write to file
                    json_line = json.dumps(detail) + '\n'
                    f.write(json_line)

if __name__ == "__main__":
    format_for_glue()
    print("Data has been formatted for AWS Glue crawler and saved to glue_formatted_data.jsonl")
