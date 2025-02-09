import requests
import json
import dotenv

class AI_shortening:
    def __init__(self,job_description):
        self.job_description = job_description
        
    def get_response(self):
            dotenv.load_dotenv()
            ai_key=dotenv.get_key('.env','OPEN_AI_KEY')

            response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {ai_key}",
            },
            data=json.dumps({
                "model": "deepseek/deepseek-r1-distill-llama-70b:free", 
                "messages": [
                {
                    "role": "user",
                    "content": f"i need you to summarize the following into 20 words: {self.job_description}"
                }
                ]
            })
            )
            if response.status_code == 200:
                reply = response.json().get('choices', [{}])[0].get('message', {}).get('content', 'No reply found')
                return(reply)
            else:
                return(f"Error: {response.status_code}, {response.text}")