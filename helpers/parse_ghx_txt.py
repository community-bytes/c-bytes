import os
import csv
import xml.etree.ElementTree as ET
import pdb
# Load the XML file
def load_xml(file_path):
    try:
        tree = ET.parse(file_path)
        return tree.getroot()
    except Exception as e:
        print(f"Error loading XML from {file_path}: {e}")
        return None

# Extract object chunk details and their counts
def extract_object_details_with_count(root):
    object_chunks_details_count = {}
    for chunk in root.findall('.//chunk'):
        name_element = chunk.find(".//item[@name='Name']")
        if name_element is not None:
            object_name = name_element.text
            object_chunks_details_count[object_name] = object_chunks_details_count.get(object_name, 0) + 1
    return object_chunks_details_count

# Main function
def main():
    csv_file_path = "csv/parsed_output.csv"

    if not os.path.exists(csv_file_path):
        print(f"Error: The CSV file '{csv_file_path}' does not exist.")
        return

    with open(csv_file_path, 'r') as file:
        rows = list(csv.reader(file))
        header = rows[0]
        rows = rows[1:]

        idx_parsed_url = header.index('parsed_urls')

        # Ensure required columns exist in the header and append an empty value for each row
        if 'component_names' not in header:
            header.append('component_names')
            for row in rows:
                row.append('')
        if 'components_count' not in header:
            header.append('components_count')
            for row in rows:
                row.append('')

        idx_comp_names = header.index('component_names')
        idx_comp_counts = header.index('components_count')

        for row in rows:
            parsed_url = row[idx_parsed_url]
            if os.path.exists(parsed_url) and parsed_url.endswith(('.xml', '.ghx')):
                print(f"Processing XML file from CSV: {parsed_url}")

                root = load_xml(parsed_url)
                if root:
                    details_count = extract_object_details_with_count(root)
                    if details_count:
                        print(f"Extracted details from {parsed_url}")
                        try:
                            row[idx_comp_names] = ",".join(details_count.keys())
                            row[idx_comp_counts] = ",".join(map(str, details_count.values()))
                        except:
                            row[idx_comp_names] = ""
                            row[idx_comp_counts] = ""

                    else:
                        print(f"No details extracted from {parsed_url}")
                else:
                    print(f"Failed to load XML from {parsed_url}")

    # Write back updated rows to the CSV
    with open(csv_file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(rows)

if __name__ == '__main__':
    main()
