import requests
import json
import os
import pandas as pd
import re
import pdb

def extract_image_urls(cooked_text):
    """Extract image URLs from the 'cooked' field."""
    image_urls = re.findall(r'<img src="([^"]+)"', cooked_text)
    return ", ".join(image_urls)

def extract_file_urls(cooked_text):
    """Extract attached file URLs from the 'cooked' field."""
    file_urls = re.findall(r'<a class="attachment" href="([^"]+)"', cooked_text)
    return ", ".join(file_urls)

def parse_json_df(data):
    """Parse JSON data to DataFrame and extract necessary fields and URLs."""
    df = pd.json_normalize(data)
    df = df[['id', 'name', 'username', 'cooked']].rename(columns={'cooked': 'text'})
    df['image_urls'] = df['text'].apply(extract_image_urls)
    df['file_urls'] = df['text'].apply(extract_file_urls)
    return df

def fetch_data(url, params):
    """Send a GET request and return the JSON data if successful."""
    response = requests.get(url, params=params)
    if response.status_code == 200:
        print("Request was successful!")
        return response.json()
    else:
        print("Request failed with status code", response.status_code)
        print("Response Text:", response.text)
        return None

def save_to_csv(df, filename='output.csv'):
    """Save DataFrame to a CSV file."""
    if os.path.exists(filename) and os.path.getsize(filename) > 0:
        df.to_csv(filename, mode='a', header=False, index=False)
    else:
        df.to_csv(filename, mode='w', header=True, index=False)
    print(f"Data has been appended to {filename}")

import json
import os

def save_to_json(data, directory='jsons', filename='response.json'):
    """Save data to a JSON file."""
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_path = os.path.join(directory, filename)
    
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        with open(file_path, 'r+') as f:
            existing_data = json.load(f)
            if isinstance(existing_data, list) and isinstance(data, list):
                existing_data.extend(data)
                f.seek(0)
                json.dump(existing_data, f)
                f.truncate()
            elif isinstance(existing_data, dict) and isinstance(data, dict):
                existing_data.update(data)
                f.seek(0)
                json.dump(existing_data, f)
                f.truncate()
            else:
                print("Error: Existing data and new data are not compatible for appending.")
                return
    else:
        with open(file_path, 'w') as f:
            json.dump(data, f)
    
    print(f"Response JSON has been appended to {file_path}")


if __name__ == "__main__":

    url_topics = f"https://discourse.mcneel.com/top.json"
    params_topics = {"period": "all"}
    response = fetch_data(url_topics, params_topics)
    topic_list = response.get('topic_list')
    topics = topic_list.get('topics')
    topic_ids = []
    for topic in topics:
        topic_ids.append(topic.get('id'))

    max_count = 10
    count = 0
    for topic_id in topic_ids:
        if count >= max_count:
            print (count)
            break
        url = f"https://discourse.mcneel.com/t/{topic_id}.json"
        params = {}
        response = fetch_data(url, params)
        post_stream = response.get('post_stream')
        data = post_stream.get('posts')

        if data:
            df = parse_json_df(data)
            save_to_csv(df)
            save_to_json(data)
        count += 1
