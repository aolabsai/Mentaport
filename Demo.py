# Python standard libraries
import ast

# Third-party libraries
import requests
import numpy as np
from openai import OpenAI
from config import openai_apikey

# AO
import ao_pyth as ao
import ao_core as ao # private package, to run our code locally, useful for advanced debugging; ao_pyth is enough for most use cases
from config import ao_apikey


def llm_call(input_message): #llm call method 
    client = OpenAI(api_key = openai_apikey)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  
        messages=[
            {"role": "user", "content": input_message}
        ],
        temperature=0.1
    )
    local_response = response.choices[0].message.content
    return local_response


def get_youtube_data(video_id="dQw4w9WgXcQ"):
    # constructed using grok: https://x.com/i/grok/share/W2HgoXmN638QUOJNKaqtnKiS2
    # refer to that if unsure how to generate your own YT API key
    google_apikey = "AIzaSyDj7CVAywnsHlgqt-FzdvfF1sI3MnXspdM"
    url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={google_apikey}"

    response = requests.get(url)
    data = response.json()

    description = data["items"][0]["snippet"]["description"]
    all_data = data
    print(description)
    return description, all_data


# Initialize AO agent architecture with X input neurons, X hidden neurons (by default), 5 output neurons. 

# Input consists of 3 features (all binary): -- we should think of more
# 1. if cross platform --> video title or description mentions TikTok or IG
# 2. if compilation --> mentions compilation or similar words
# 3. if ad --> includes affiliate links or others to sketchy e-commerce sites
# 
# -- come up with more input types/channels of data!
#
# The 5 output neurons correspond to the likelihood of infringement (scale 1-5).
arch = ao.Arch(arch_i="[1, 1, 1]", arch_z="[5]", api_key=ao_apikey, kennel_id="Mentaport_demo") 


# Create an agent with the given architecture
agent = ao.Agent(arch, uid="Scanner_01", save_meta=True)
agent.api_reset_compatibility = True # to enable similar behavior in local core with reset states as ao_python when running cross-compatible scripts


# Setting a baseline by pre-training example patterns that are known to be fraudulent. 
# -> Likelihood of fraud (scale 1-5)
training_data = [
    ([1, 1, 1], [1, 1, 1, 1, 1]),     # Highest fraud likelihood
    ([1, 1, 0], [1, 1, 1, 0, 0]),
    ([1, 0, 0], [1, 0, 0, 0, 0]),
    ([0, 0, 0], [0, 0, 0, 0, 0]),
]
###Uncomment to train the agent on baseline
for inp, label in training_data:
    agent.next_state(INPUT=inp, LABEL=label, unsequenced=True)  # Reset states are added automatically if unsequenced=True and when agent.api_reset_compatibility is True


# yt_description, yt_data = get_youtube_data("LiTDxKx25MY")
# yt_description, yt_data = get_youtube_data("Fu-eP0YRQTI")
yt_description = get_youtube_data("SUBk89F3giM")

# Extracting features for input (using an LLM here - we can use other APIs)
input_to_agent = ast.literal_eval(llm_call(f"""I am attaching a youtube video to this chat. Fill out this list with 1 OR 0 of length 3 then return the list only. Format: 
#          [mentions non-youtube social media platform like TikTok or instagram, seems like a compilation of content, seems like an ad] {yt_description} 
                       """))
print("LLM response: ", input_to_agent)
print(type(input_to_agent))

## Simple manual feature extraction examples
# tiktok_mention = [1] if "TikTok" in yt_description else [0]
# compilation = [1] if "compilation" in yt_description else [0]
# print(tiktok_mention)


# Predicting the likelihood of infringement based on the input
agent_response = agent.next_state(input_to_agent, unsequenced=True)
print("agent response: ", agent_response)
ones = sum(agent_response)
print("Predicted likelihood of infringement: ", ones / len(agent_response) * 100, "%")


# Closing the Learning Loop - passing feedback to the system to drive learning
res = input("Closing the Learning Loop-- was this input-pattern actually infringement (Y or N)?  ")
if res == "Y":
    agent.next_state(input_to_agent, [1, 1, 1, 1, 1], unsequenced=True)
else:
    agent.next_state(input_to_agent, [0, 0, 0, 0, 0], unsequenced=True)


# To verify the learning, predict infringement again on the SAME input-pattern
agent_response = agent.next_state(input_to_agent, unsequenced=True)
print("agent response: ", agent_response)
ones = sum(agent_response)
print("AFTER LEARNING, predicted likelihood of infringement: ", ones / len(agent_response) * 100, "%")
