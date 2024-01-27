from flask import Flask, request, jsonify
import google.generativeai as genai
import os
import dotenv
import trafilatura
dotenv.load_dotenv()
import json

# flask cors  
from flask_cors import CORS
gemini_api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key = gemini_api_key)
app = Flask(__name__)

CORS(app)
allowed_origins = ["*"]

@app.route('/')
def hello_world():
    return 'Hello, World! -v2'



def genAiQuestion(urls):
    text = '''Act as a Security analyst:

this  is the tearm and condition :
```
'''
    # for url in urls:
    #     print(url)
    #     html = trafilatura.fetch_url(url)
    #     text += trafilatura.extract(html)
    #     text += '\n'
    print(urls)
    html = trafilatura.fetch_url(urls[0])
    text += trafilatura.extract(html)
    text += '\n'

    text += '''```
    Provide the JSON format containing the top highlighted point (most critical in the context of the users) (atleast 5 or more) along with its concern rating on a scale of 1-3, where 3 signifies the most concerning point and 1 is the least concern. Additionally, offer a brief description of that point.

(JSON format example:
    {
    "privacyPolicy": [
      {
        "point": "Minimum Age Requirement",
        "concernRating": 2,
        "brief": "Users must be at least 13 years old or meet the minimum age requirement in their country to use the Services. Users under 18 require parental or legal guardian permission."
      },
      {
        "point": "Registration and Access",
        "concernRating": 3,
        "brief": "Users must provide accurate and complete information for account registration. Sharing account credentials or using the Services on behalf of others requires proper authorization."
      }
    ]
  })
    ''' 
    
    print(len(text))
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(text)
    return response.text

@app.route('/getAnalysis', methods=['POST'])
def getAnalysis():
    # terms_link = request.json['terms-url']
    print(1)
    privacy_link = request.json['privacy_url']
    print(privacy_link)
    urls = [ privacy_link]
    response = genAiQuestion(urls)
    response = response.replace('`',"")
    response = json.loads(response.replace('\n', '').replace('\\"', '"'))

    return jsonify({'response': response})

@app.route('/test1', methods=['POST'])
def test():
    data = {
  "response": {
    "termsAndConditions": [
      {
        "brief": "OpenAI collects various types of personal information including name, contact information, IP address, device identifiers, account credentials, payment card information, transaction history, Content, Social Information, and Technical Information.",
        "concernRating": 3,
        "point": "Personal Information Collection"
      },
      {
        "brief": "OpenAI uses personal information for various purposes, including providing, maintaining, and improving the Services, research, communication, developing new programs and services, fraud prevention, protection against legal liability, and compliance with legal obligations.",
        "concernRating": 3,
        "point": "Use of Personal Information"
      },
      {
        "brief": "OpenAI may disclose personal information to vendors, service providers, business affiliates, government authorities, industry peers, or other third parties for legal reasons, fraud prevention, or other legitimate business purposes.",
        "concernRating": 2,
        "point": "Disclosure of Personal Information"
      },
      {
        "brief": "Users may have certain rights, such as accessing, updating, or deleting their personal information, depending on their location and applicable laws. OpenAI provides options for exercising these rights through their account or by contacting privacy.openai.com.",
        "concernRating": 2,
        "point": "User Rights and Access"
      },
      {
        "brief": "OpenAI implements security measures to protect personal information from unauthorized access or disclosure. However, no internet transmission is completely secure, and OpenAI is not responsible for circumventing security measures.",
        "concernRating": 2,
        "point": "Data Security and Retention"
      }
    ]
  }
}



    return jsonify({'response': data})

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")