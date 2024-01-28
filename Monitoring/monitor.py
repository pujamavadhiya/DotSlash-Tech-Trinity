# take the link form the tor-link.txt


with open('tor-link.txt', 'r') as f:
    data = f.read()
    data = data.split('\n')

list_of_urls = []
for i in data:
    if i != '':
        list_of_urls.append(i)
import requests
import json
import os
import dotenv
from bs4 import BeautifulSoup
import google.generativeai as genai

dotenv.load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

proxies = {"http": "socks5h://localhost:9050", "https": "socks5h://localhost:9050"}
headers = {"User-Agent": "Mozilla/5.0"}

with open('tor-link.txt', 'r') as f:
    data = f.read().splitlines()

list_of_urls = [i for i in data if i]

def genAiQuestion(url):
    try:
        r = requests.get(url, proxies=proxies, headers=headers)
        r.raise_for_status()  # Raise HTTPError for bad requests
        html = r.content.decode("utf-8")
        soup = BeautifulSoup(html, 'html.parser')
        docs = soup.get_text()

        text = '''Act as a Security analyst: In this data find is there any data leak or not...'''
        text += docs

        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(text)
        
        # Ensure valid JSON before parsing
        response = json.loads(response.replace('\n', '').replace('\\"', '"'))
        print(response)

    except requests.RequestException as e:
        print(f"Error accessing {url}: {e}")

# Process the URLs
for url in list_of_urls[:5]:  # Adjust the range as needed
    genAiQuestion(url)
