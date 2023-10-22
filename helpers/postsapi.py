import requests
import json
import os
import pandas as pd
import re
import pdb

def fetch_data(url, params):
    """Send a GET request and return the JSON data if successful."""
    response = requests.get(url, params=params)
    if response.status_code == 200:
        print("Request was successful!")
        return response.json()
    print(f"Request failed with status code {response.status_code}")
    print("Response Text:", response.text)
    return None

def extract_image_urls(cooked_text):
    """Extract image URLs from the 'cooked' field."""
    return ", ".join(re.findall(r'<img src="([^"]+)"', cooked_text))

def extract_file_urls(cooked_text):
    """Extract attached file URLs from the 'cooked' field."""
    return ", ".join(re.findall(r'<a class="attachment" href="([^"]+)"', cooked_text))

def parse_json(data, is_solution=True):
    """Parse JSON data to DataFrame and extract necessary fields and URLs."""
    df = pd.json_normalize(data)
    if is_solution:
        columns = {
            'id': 'answer-id',
            'name': 'answer-name',
            'username': 'answer-username',
            'cooked': 'text'
        }
        df = df[['id', 'name', 'username', 'cooked', 'score', 'reads', 'readers_count', 'trust_level']].rename(columns=columns)
        df['image_urls'] = df['text'].apply(extract_image_urls)
        df['file_urls'] = df['text'].apply(extract_file_urls)
    else:
        df = df[['id', 'cooked']].rename(columns={'id': 'og-id', 'cooked': 'og-text'})
    return df

def save_to_csv(df, filename='csv/output.csv'):
    """Save DataFrame to a CSV file."""
    mode = 'a' if os.path.exists(filename) and os.path.getsize(filename) > 0 else 'w'
    header = mode == 'w'
    df.to_csv(filename, mode=mode, header=header, index=False)
    print(f"Data has been appended to {filename}")

def save_to_json(data, directory='jsons', filename='response.json'):
    """Save data to a JSON file."""
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_path = os.path.join(directory, filename)
    
    mode = 'r+' if os.path.exists(file_path) and os.path.getsize(file_path) > 0 else 'w'
    with open(file_path, mode) as f:
        if mode == 'r+':
            existing_data = json.load(f)
            if isinstance(existing_data, list) and isinstance(data, list):
                existing_data.extend(data)
            elif isinstance(existing_data, dict) and isinstance(data, dict):
                existing_data.update(data)
            else:
                print("Error: Existing data and new data are not compatible for appending.")
                return
            f.seek(0)
            json.dump(existing_data, f)
            f.truncate()
        else:
            json.dump(data, f)
    
    print(f"Response JSON has been appended to {file_path}")

if __name__ == "__main__":
    max_count = 80717 + 15

    for i in range(80717 - 10000, max_count):
        url = f"https://discourse.mcneel.com/t/{i}.json"
        try:
            response = fetch_data(url, params={})
        except:
            print (f"fetching of the id {i} failed")
        
        if not response or not response.get("accepted_answer"):
            continue
        
        post_stream = response.get('post_stream', {})
        data = post_stream.get('posts', [])
        
        if not data:
            continue
        
        original_post = data[0]
        topic_id = response.get("id")
        
        accepted_post_number = response.get("accepted_answer").get("post_number", 0)
        accepted_answer = None
        try:

            accepted_answer = data[accepted_post_number - 1] if accepted_post_number > 0 else None
        except:
            print(f"Retrieving the accepted answer for the id {i} failed")
        
        if accepted_answer:
            df_solution = parse_json(accepted_answer)
            df_original = parse_json(original_post, is_solution=False)
            df_topic = pd.DataFrame({'topic-id': [topic_id]})
            
            result = pd.concat([df_solution, df_original, df_topic], axis=1)
            save_to_csv(result)

