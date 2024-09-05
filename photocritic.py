import os
from base64 import b64encode
from openai import AsyncOpenAI
import chainlit as cl


# OpenAI setup
cl.instrument_openai()
token = os.environ["GITHUB_TOKEN"]
settings = {
    "model": "gpt-4o",
    "temperature": 0.9,
    "top_p": 0.8
}

client = AsyncOpenAI(base_url="https://models.inference.ai.azure.com", api_key=token)
#client= AsyncOpenAI()

# Helper function from https://github.com/GianfrancoCorrea/gpt-4-vision-chat/
def process_image(image):
    # Accessing the bytes of a specific image
    
    imagepath = image[0].path

    with open(imagepath, "rb") as image_file:
        image_base64 = b64encode(image_file.read()).decode('utf-8')

    # check the size of the image, max 1mb
    if len(image_base64) > 1000000:
        return "too_large"
        
    return image_base64

@cl.on_message

async def on_message(msg: cl.Message):

    if not msg.elements:
        stream = await client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a digital photo critic. You will provide helpful feedback on photographs on how to improve them."
                },
                {
                    "role": "user",
                    "content": msg.content
                }
            ],
            stream=True,
            **settings
        )
    else:
        # Processing images exclusively
        images = [file for file in msg.elements if "image" in file.mime]
        base64_image = process_image(images)
        print(msg.content)
        # Generate response
        stream = await client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a digital photo critic. You will provide helpful feedback on photographs on how to improve them.",
                    
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": msg.content
                        },
                        {
                             "type": "image_url",
                             #"image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                             "image_url": {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg",},
                        }
                    ]                    
                }
            ],
            stream=True,
            **settings
        )


    new_message = cl.Message(content="")

    async for part in stream:
        if token := part.choices[0].delta.content or "":
            await new_message.stream_token(token)

    await new_message.update()


    #await cl.Message(content=response.choices[0].message.content).send()


@cl.on_chat_start
async def start():

    # Attach the image to the message
    await cl.Message(
        content="Hello! I'm the GPT-4o Photo Critic! How can I help?",
    ).send()


'''
async def main(msg: cl.Message):
    message_history = cl.user_session.get("message_history")
    message_history.append({"role": "user", "content": message.content})

    msg = cl.Message(content="")
    await msg.send()
'''
