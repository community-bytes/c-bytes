import csv
import os
import requests
from urllib.parse import urlparse
import pdb

def download_file(url, save_path):
    url = f"https:{url}"
    try:
        response = requests.get(url, stream=True)
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        return save_path
    except:
        return ''

def main():
    # Input and output CSV files
    input_csv = 'csv/output.csv'
    output_csv = 'csv/updated_output.csv'
    
    # Create a directory to save the files
    if not os.path.exists('downloaded_files'):
        os.makedirs('downloaded_files')
    
    with open(input_csv, mode='r', newline='', encoding='utf-8') as infile, \
         open(output_csv, mode='w', newline='', encoding='utf-8') as outfile:
         
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames
        
        # Add "local_urls" to fieldnames if it doesn't exist
        if 'local_urls' not in fieldnames:
            fieldnames.append('local_urls')
        
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        max_count = 1000
        count = 0
        for row in reader:
            if count >= max_count:
                break
            file_urls = row['file_urls'].split(", ")
            local_paths = []
            for url in file_urls:
                filename = os.path.basename(urlparse(url).path)
                local_path = download_file(url, os.path.join('downloaded_files', filename))
                local_paths.append(local_path)
            
            row['local_urls'] = ", ".join(local_paths)
            writer.writerow(row)
            count +=1

if __name__ == "__main__":
    main()
