
# <img src="https://github.com/community-bytes/c-bytes/assets/9583495/098d7028-15fb-4a98-bb5a-3e6f5fde8de1" width="50"/> G-Chomp: A Grasshopper Community-Byte
Made at/for the [Chicago Innovate Hackathon 2023](https://www.chicagoinnovate.tech/hackathon)

G-Chomp is a project to collect and analyze the collective knowledge of the community using Rhino and Grasshopper on the [McNeel Forum](https://discourse.mcneel.com/).  Our current goal is to develop a dataset which can be used to tune and/or train an LLM to act as a co-pilot for an LLM-driven Grasshopper Co-pilot.  

Cesar Hidalgo, author of "Why Information Grows" coined the term "personbyte" to refer to the maximum knowledge and knowhow of an individual.  He additionally refers to the "teambyte" and "firmbyte" as extensions of this concept.  we propose the term “community-byte” as a measure of the limits of a communal store of knowledge, and “G-CHOMP” as a Grasshopper-specific community-byte.  This project seeks to transform the collective knowledge of the Rhino/Grasshopper community as represented in the Rhino community forum to make it usable and accessible in new contexts. 

# Interactive Web UI
![image](https://github.com/saumyaborwankar/c-bytes/assets/46644513/da2c7713-4efc-4b10-bb96-fea4bb801340)


---
Here are the steps we are planning:

## 1. Collect
- ### method 1: scrape the website directly
- [x] gather posts from the Rhino/McNeel forum
- [ ] gather only posts with Grasshopper Scripts attached
- ### method 2: using [Discourse OpenAPI](https://docs.discourse.org/)
- [x] gather posts from the Rhino/McNeel forum
- [ ] gather only posts with Grasshopper Scripts attached
- [x] overcome 30 post limit   
## 2. Extend
- further characterize the posts with additional attributes relating to the contents of the scripts and/or other data points
- [ ] Get the list of components in each script (using [david rutten's script parser](https://discourse.mcneel.com/t/get-grasshopper-document-object-count-without-opening-grasshopper/78311/4) or .ghx xml crawler)
- [ ] convert program to output csv
- [ ] automate use of program and link per dataset entry
- [ ] Characterize images in posts - is it a picture of the script? of the script output? neither? 
## 3. Analyze
- perform analysis of the dataset with several goals in mind: Cleaning the data, qualifying it (predicting script quality), and providing insights about the data.
- [x] Find/identify a list of Rhino/Grasshopper "stop words" - common words in posts that should be ignored when characterizing topic conversations
- [ ] Find/identify a list of Grasshopper "stop words" - the most common components that should be ignored when characterizing scripts
- [ ] qualify script quality by proxy (author? number of posts? Some keywords to include/exclude?)
- [x] identify example scripts from Omid Sajedi workshop to use as bases for development
- [x] modify example scripts with cbyte dataset (simplified or otherwise)
## 4. Document & Share
- Document our process and our findings
- [x] maintain readme to reflect progress 
- [ ] Share the dataset on [Kaggle](https://www.kaggle.com/datasets)
---

We hope/plan to pursue the following additional goals:
## 5. Apply
- [ ] Use the model to train/tune an LLM to understand the semantic connection between a description of what a script does and the contents of the script
## 6. Generate
- [ ] create new scripts using an LLM to automatically generate grasshopper components on the canvas
- [ ] possibly using/in combination with [ghPT](https://github.com/enmerk4r/GHPT)
## 7. Iterate
- [ ] analyze the quality of the scripts
- [ ] identify potential changes to improve results
- [ ] Expand the dataset

---

## Team Members:
Jerry - Chieh Jui Lee - [JERRRRY](https://github.com/JERRRRY) - [IIT](https://www.iit.edu/) (Illinois Institute of Technology) 

Jo Kamm - [jkamm](https://github.com/jkamm) - Digital Technology Lead at [Dimensional Innovations](dimin.com)

Patryk Wozniczka - [patrykwoz](https://github.com/patrykwoz) 

Saumya Borwankar - [saumyaborwankar](https://github.com/saumyaborwankar) - [IIT](https://www.iit.edu/) 

Siddhartha Upase - [IIT](https://www.iit.edu/) 

YongWon Jeong - [yjeong93](https://github.com/yjeong93) - Architectural professional 1 at [Wight&Company](https://www.wightco.com/)   

---
## Code Sources:
- [Discourse API](https://docs.discourse.org/)
- [Grasshopper file analytics tool](https://discourse.mcneel.com/t/get-grasshopper-document-object-count-without-opening-grasshopper/78311)
- [gh to ghx tool](https://bitbucket.org/RILGH/ghtoghx/src/master/)
- [Becoming AI Power-Users: A Hands-on Workshop on Machine Learning and Generative AI](https://www.chicagoinnovate.tech/courses-1/becoming-ai-power-users%3A-a-hands-on-workshop-on-machine-learning-and-generative-ai) by Seyedomid Sajedi of Thornton Thomasetti during Chicago Innovate 2023 (github link forthcoming soon)
