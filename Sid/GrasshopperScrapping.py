import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin

# Inside your main script (e.g., main.py)
import subprocess

base_url = "https://discourse.mcneel.com/c/grasshopper/2"  # Adjust the URL to match the category
csv_filename = 'grasshopper_posts.csv'

def scrape_page(url, csv_writer):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        posts = soup.find_all('tr', class_='topic-list-item')

        for post in posts:
            title = post.find('a', class_='title raw-link raw-topic-link').text
            relative_post_url = post.find('a', class_='title raw-link raw-topic-link')['href']
            post_url = urljoin(base_url, relative_post_url)

            post_response = requests.get(post_url)
            if post_response.status_code != 200:
                continue

            post_soup = BeautifulSoup(post_response.text, 'lxml')

            content = ""
            content_div = post_soup.find('div', class_='regular contents')
            if content_div:
                for paragraph in content_div.find_all('p'):
                    content += paragraph.get_text(strip=True) + "\n"

            image_links = [img['src'] for img in post_soup.find_all('img')]

            csv_writer.writerow([title, content, ', '.join(image_links)])

        return True
    else:
        return False

with open(csv_filename, 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Title', 'Content', 'Image Links'])

    page = 0
    while True:
        url = f"{base_url}?page={page}"
        if not scrape_page(url, csv_writer):
            break  # Stop if the page couldn't be retrieved

        page += 1  # Move to the next page

print("Data scraped and saved to 'grasshopper_posts.csv'")
subprocess.run(['python', 'create_html.py'])
