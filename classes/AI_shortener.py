import aiohttp
import json
import dotenv
import asyncio
from typing import Optional
from openai import OpenAI

class AI_shortening:
    def __init__(self, job_descript):
        self.job_descript = job_descript
        dotenv.load_dotenv()
        self.ai_key = dotenv.get_key('.env', 'OPEN_AI_KEY')
        
    async def get_response(self) -> str:
        print('generating ...')
        """
        Asynchronously get the AI-shortened response.
        Returns the summarized job description when complete.
        """
        print('generating ...')
        try:
            
            client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key= self.ai_key,
                )

            completion = client.chat.completions.create(
                extra_headers={

                },
                extra_body={},
                model="deepseek/deepseek-r1-distill-llama-70b:free",
                messages=[
                    {
                    "role": "user",
                    "content": f"{self.job_descript} summarize the job with the following template, DO NOT DEVIATE FROM THE TEMPLATE: Company:() Wage:() Description:()"
                    }
                ]
                )
            print(f"Raw API response: {completion}")
            return completion.choices[0].message.content

                        
        except Exception as e:
            return f"Error making API request: {str(e)}"




