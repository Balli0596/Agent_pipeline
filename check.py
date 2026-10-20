from google import genai
import os

client = genai.Client(
    api_key="AIzaSyCEKcbRVTQsGmNNoq22UyPPOS90mqetSVo"
)

response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents="Reply with OK."
)

print(response.text)