import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin

# Your earlier script here

# HTML generation script
import csv
from bs4 import BeautifulSoup



# Read the CSV file
with open('grasshopper_posts.csv', 'r', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)  # Skip the header row

    # Extract image links from the CSV
    image_links = []
    for row in csv_reader:
        image_links.extend(row[2].split(', '))

# Create an HTML page to display the images
html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Images</title>
</head>
<body>
"""

for image_link in image_links:
    html_content += f"<img src='{image_link}' alt='Image'><br>"

html_content += """
</body>
</html>
"""

# Save the HTML content to a file
with open('images.html', 'w', encoding='utf-8') as html_file:
    html_file.write(html_content)

print("HTML page created and images displayed in 'images.html'")
