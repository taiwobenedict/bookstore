from dotenv import load_dotenv
from openai import OpenAI
import os




load_dotenv()  # take environment variables from .env.


def generate_book_summary(book_title):
    client = OpenAI(
        api_key= os.getenv("OPENAI_API_KEY"),
        project= os.getenv("OPENAI_PROJECT_KEY")
    )

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "developer", "content": "You are a helpful assistant, that formulate short summary for books by their titles"},
            {
                "role": "user",
                "content": f"Summarize this book: {book_title}"
            }
        ]
    )

    return completion.choices[0].message
        