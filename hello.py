import os
from dotenv import load_dotenv
from anthropic import Anthropic

# Load the API key from .env
load_dotenv()

# Create the Anthropic client (it picks up ANTHROPIC_API_KEY from environment)
client = Anthropic()

# Make a single message call
response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "In one sentence, what is retrieval-augmented generation?"}
    ]
)

# Print the text of the response
print(response.content[0].text)