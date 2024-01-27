from flask import Flask, request, jsonify
import google.generativeai as genai
import os
import dotenv
import trafilatura
dotenv.load_dotenv()
import json

gemini_api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key = gemini_api_key)
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'



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
def test():
    # terms_link = request.json['terms-url']
    privacy_link = request.json['privacy-url']
    print(privacy_link)
    urls = [ privacy_link]
    response = genAiQuestion(urls)
    response = response.replace('`',"")
    response = json.loads(response.replace('\n', '').replace('\\"', '"'))

    return jsonify({'response': response})



if __name__ == '__main__':
    app.run(debug=True)