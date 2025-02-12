import aiohttp
import json
import dotenv
import asyncio
from typing import Optional

class AI_shortening:
    def __init__(self, job_descript):
        self.job_descript = job_descript
        dotenv.load_dotenv()
        self.ai_key = dotenv.get_key('.env', 'OPEN_AI_KEY')
        
    async def get_response(self) -> str:
        """
        Asynchronously get the AI-shortened response.
        Returns the summarized job description when complete.
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url="https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.ai_key}",
                    },
                    json={
                        "model": "sophosympatheia/rogue-rose-103b-v0.2:free",
                        "messages": [
                            {
                                "role": "user",
                                "content": f"{self.job_descript},Summarize the job in that string with this exact template,ignore the information about the company, do not deviate from it in any way 'Company:(Company name) Wage:(Wage) Description:(description of job)' DO NOT ADD ANYTHING OUTSIDE OF THAT TEMPLATE"
                            }
                        ]
                    }
                ) as response:
                    if response.status == 200:
                        response_data = await response.json()
                        reply = response_data.get('choices', [{}])[0].get('message', {}).get('content', 'No reply found')
                        return reply
                    else:
                        response_text = await response.text()
                        return f"Error: {response.status}, {response_text}"
                        
        except Exception as e:
            return f"Error making API request: {str(e)}"
