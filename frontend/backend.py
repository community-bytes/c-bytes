from flask import Flask, request, jsonify
from sentence_transformers import SentenceTransformer, util
from flask_cors import CORS
import numpy as np

import json
app = Flask(__name__)
CORS(app) 

# Load a pre-trained model
model = SentenceTransformer('all-MiniLM-L6-v2')
f = open('../data/output.json','r')
parsed_data = json.load(f)
titles=[]
# Access and process the content
for item in parsed_data:
    topics = item.get("topics")
    title = topics.get("title")
    titles.append(title)
    post_count = topics.get("postcount")
    views = topics.get("views")
    likes = topics.get("likes")
    
    # print("Title:", title)
    # print("Post Count:", post_count)
    # print("Views:", views)
    # print("Likes:", likes)
    # print("Posts:")

    # posts = topics.get("posts")
    # for post_id, post_data in posts.items():
    #     content = post_data.get("content")
    #     print("Post ID:", post_id)
    #     print("Content:", content)
    #     print("\n")
# Closing file
f.close()

@app.route('/compute_similarity', methods=['POST'])
def compute_similarity():
    try:
        # Get the input text from the request
        data = request.get_json()
        input_text = data['input_text']
        index =0
        max_similar=-1

        # Define a reference sentence
        for reference_sentence,i in enumerate(titles):

            # Encode the input and reference sentences using the pre-trained model
            input_embedding = model.encode(input_text, convert_to_tensor=True)
            reference_embedding = model.encode(reference_sentence, convert_to_tensor=True)

            # Compute cosine similarity between the two sentence embeddings
            cosine_similarity = util.cos_sim(input_embedding, reference_embedding)
            tensor_on_cpu = cosine_similarity.to('cpu')

            # Extract the value as a Python float
            value = tensor_on_cpu.item()
            if(value>max_similar):
                index=i
                max_similar=value

        # print(value)
        # print("hellp",type(cosine_similarity))
        # print(cosine_similarity,input_text)
        return jsonify({'cosine_similarity': max_similar, "index":index})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
