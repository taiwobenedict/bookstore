from dotenv import load_dotenv
from openai import OpenAI
import os




load_dotenv()  # take environment variables from .env.


def generate_book_summary(book_title):
    client = OpenAI(
        api_key= os.getenv("OPENAI_API_KEY"),

    )

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "developer", "content": "You are a helpful assistant, that generate frictional short summary for books base on their titles whether the book exist or not. And just go straight to summary, don't tell the user wether you're familiar of the book or not"},
            {
                "role": "user",
                "content": f"Summarize this book: {book_title}"
            }
        ]
    )
    
    

    return completion.choices[0].message.content
        