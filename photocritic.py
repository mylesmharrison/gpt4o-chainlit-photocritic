import os
import chainlit as cl
from openai import OpenAI, AsyncOpenAI
from base64 import b64encode

token = os.environ["GITHUB_TOKEN"]
settings = {
    "model": "gpt-4o",
    "temperature": 0.9,
    "top_p": 0.8
}

client = AsyncOpenAI(base_url="https://models.inference.ai.azure.com", api_key=token)

# Helper function from https://github.com/GianfrancoCorrea/gpt-4-vision-chat/
def process_image(imagepath):
    # Accessing the bytes of a specific image
    
    with open(imagepath, "rb") as image_file:
        image_base64 = b64encode(image_file.read()).decode('utf-8')

    # check the size of the image, max 1mb
    if len(image_base64) > 1000000:
        return "too_large"
        
    return image_base64

@cl.on_chat_start
async def start():

    cl.user_session.set(
        "message_history",
        [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role":"assistant",
                "content":"Hello and welcome!"
            }

        ],
    )

    new_message = cl.Message(content="Hello and welcome")
    await new_message.send()

@cl.on_message
async def onmessage(msg: cl.Message):

    # Get the message history
    message_history = cl.user_session.get("message_history")

    # Check if the chat message has an image attached
    
    if msg.elements:
        climage = msg.elements[0]
        #climage = cl.Image(path="./sample.jpg", name="image1", display="inline")
        base64_image = process_image(climage.path)
    
    # Append to appropriate history
    message_history.append({"role": "user", "content": msg.content})

    # Set up response
    response_msg = cl.Message(content="") 
    stream = None\

    stream = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=message_history,    
        stream=True
    )
    
    message_history.append({"role": "system", "content": response_msg.content})
    
    async for part in stream:
        if token := part.choices[0].delta.content:
            await response_msg.stream_token(token)
    await response_msg.update()