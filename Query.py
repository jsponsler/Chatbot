import sqlite3
from bs4 import BeautifulSoup
import openai
import os

# Database connection to retrieve the HTML content
conn = sqlite3.connect('spider.sqlite')
cursor = conn.cursor()

cursor.execute("SELECT html FROM Pages WHERE url = 'http://www.hioscar.com/faq/section/for-brokers'")
html_content = cursor.fetchone()[0]
# rows = cursor.fetchall() # Pulling all rows to concatenate

# # Concatenate the HTML content into a single string
# html_content = ''
# for row in rows:
#     html_content += str(row[0])

# Parse the HTML content and extract the body
soup = BeautifulSoup(html_content, 'html.parser')
body_content = soup.body.text

# OpenAI API credentials
openai.api_key = os.environ["OPENAI_API_KEY"]

# Function to generate a response based on a question
def generate_response(question, body_content):
    prompt = f"Context: {body_content}\nQuestion: {question}\nAnswer:"
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=824,
        n=1,
        stop=None,
        temperature=0.7,
        )
    answer = response.choices[0].text.strip()
    return answer

# Get a user question as input and generate a response
user_question = input("What would you like to know? ")
response = generate_response(user_question, body_content)
print(response)