import requests
from bs4 import BeautifulSoup
import csv

base_url = "https://discourse.mcneel.com/tag/grasshopper"
csv_filename = 'grasshopper_posts_title.csv'

with open(csv_filename, 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Title', 'Post Link'])

    page = 1  # Start with the first page
    while True:
        url = f"{base_url}?page={page}"
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml')
            posts = soup.find_all('tr', class_='topic-list-item')

            if not posts:
                break  # No more pages to scrape

            for post in posts:
                title = post.find('a', class_='title raw-link raw-topic-link').text
                post_url = post.find('a', class_='title raw-link raw-topic-link')['href']
                full_post_url =post_url

                csv_writer.writerow([title, full_post_url])

            #page += 1  # Move to the next page
        else:
            print(f"Failed to retrieve the page. Status code: {response.status_code}")
            break

print("Data scraped and saved to 'grasshopper_posts_title.csv'")
