from openai import OpenAI
import os

from slides_functions import *

# Initialize the OpenAI client
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
print("API key set")



# # Define the functions to be called
# def create_textbox_with_text(unique_elementID, textheight, textwidth, xpos, ypos, text_string):
#     print(f"Creating textbox with text: {text_string}")
#     # Your actual implementation here

# def reposition_element(element_id, textheight, textwidth, xpos, ypos, text_string):
#     print(f"Repositioning element: {element_id}")
#     # Your actual implementation here

# def create_ellipse_with_text(unique_elementID, textheight, textwidth, xpos, ypos, text_string):
#     print(f"Creating ellipse with text: {text_string}")
#     # Your actual implementation here

# def create_cloud_with_text(unique_elementID, textheight, textwidth, xpos, ypos, text_string):
#     print(f"Creating cloud with text: {text_string}")
#     # Your actual implementation here

# def create_ellipse_without_text(unique_elementID, shapeheight, shapewidth, xpos, ypos):
#     print("Creating ellipse without text")
#     # Your actual implementation here

# def create_cloud_without_text(unique_elementID, shapeheight, shapewidth, xpos, ypos):
#     print("Creating cloud without text")
#     # Your actual implementation here

# GPT Function calling setup
functions = [
    {
        "name": "create_textbox_with_text",
        "description": "Create a textbox with specified text",
        "parameters": {
            "type": "object",
            "properties": {
                "unique_elementID": {"type": "string"},
                "textheight": {"type": "integer"},
                "textwidth": {"type": "integer"},
                "xpos": {"type": "integer"},
                "ypos": {"type": "integer"},
                "text_string": {"type": "string"}
            },
            "required": ["unique_elementID", "textheight", "textwidth", "xpos", "ypos", "text_string"]
        }
    },
    {
        "name": "reposition_element",
        "description": "Reposition an existing element",
        "parameters": {
            "type": "object",
            "properties": {
                "element_id": {"type": "string"},
                "textheight": {"type": "integer"},
                "textwidth": {"type": "integer"},
                "xpos": {"type": "integer"},
                "ypos": {"type": "integer"},
                "text_string": {"type": "string"}
            },
            "required": ["element_id", "textheight", "textwidth", "xpos", "ypos", "text_string"]
        }
    },
    {
        "name": "create_ellipse_with_text",
        "description": "Create an ellipse with specified text",
        "parameters": {
            "type": "object",
            "properties": {
                "unique_elementID": {"type": "string"},
                "textheight": {"type": "integer"},
                "textwidth": {"type": "integer"},
                "xpos": {"type": "integer"},
                "ypos": {"type": "integer"},
                "text_string": {"type": "string"}
            },
            "required": ["unique_elementID", "textheight", "textwidth", "xpos", "ypos", "text_string"]
        }
    },
    {
        "name": "create_cloud_with_text",
        "description": "Create a cloud shape with specified text",
        "parameters": {
            "type": "object",
            "properties": {
                "unique_elementID": {"type": "string"},
                "textheight": {"type": "integer"},
                "textwidth": {"type": "integer"},
                "xpos": {"type": "integer"},
                "ypos": {"type": "integer"},
                "text_string": {"type": "string"}
            },
            "required": ["unique_elementID", "textheight", "textwidth", "xpos", "ypos", "text_string"]
        }
    },
    {
        "name": "create_ellipse_without_text",
        "description": "Create an ellipse without text",
        "parameters": {
            "type": "object",
            "properties": {
                "unique_elementID": {"type": "string"},
                "shapeheight": {"type": "integer"},
                "shapewidth": {"type": "integer"},
                "xpos": {"type": "integer"},
                "ypos": {"type": "integer"}
            },
            "required": ["unique_elementID", "shapeheight", "shapewidth", "xpos", "ypos"]
        }
    },
    {
        "name": "create_cloud_without_text",
        "description": "Create a cloud shape without text",
        "parameters": {
            "type": "object",
            "properties": {
                "unique_elementID": {"type": "string"},
                "shapeheight": {"type": "integer"},
                "shapewidth": {"type": "integer"},
                "xpos": {"type": "integer"},
                "ypos": {"type": "integer"}
            },
            "required": ["unique_elementID", "shapeheight", "shapewidth", "xpos", "ypos"]
        }
    },
    {
            "name": "create_image",
            "description": "Create the Pear VC logo image",
            "parameters": {
                "type": "object",
                "properties": {
                    "imheight": {"type": "integer"},
                    "imwidth": {"type": "integer"},
                    "xpos": {"type": "integer"},
                    "ypos": {"type": "integer"}
                },
            },
            "required": ["imheight", "imwidth", "xpos", "ypos"]
    }
]
# Use alphanumeric keys (e.g., "A", "B", "C", etc.) for each instruction.

def call_openai_function(prompt):
    # prompt = "The dimensions of the slide are 600 x pixels and 300 y pixels. " + prompt

    dimension_prompt = "The dimensions of the slide are 400 x pixels and 200 y pixels."

    meta_prompt = """You have been provided with a long block of transcripted text that contains multiple instructions to edit graphics. Your task is to break this long block into a series of simple, one-line instructions, each corresponding to a single action.
Output the result as a series of sentences, each starting with a new line.
Ensure each line is a distinct and manageable action.
Note that the dimensions of the slide are 400 x pixels and 200 y pixels.

Input: Add a text box with the text Welcome to PearHacks x OpenAI in the center and add a cloud which says Happy to be here

Expected output:

Add a text box with the text 'Welcome to PearHacks x OpenAI' in the center
Add a cloud which says 'Happy to be here'

Here is the prompt that you are processing:

""" + prompt
    
    print(f"Calling OpenAI function with prompt: {prompt}")

    response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that helps create Google Slides."},
                {"role": "user",
                 "content": meta_prompt }
                ]
            )
    print("Received response from OpenAI")

    print(response)

    try:
        newline_response = response.choices[0].message.content

        newline_response = newline_response.split("\n")

        for i in range(len(newline_response)):
            print(f"Prompt {i+1}: {newline_response[i]}")
            call_prompt(newline_response[i])
    except Exception as e:
        print(f"An error occurred: {e}")


def call_prompt(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini", 
        messages=[
            {"role": "system", "content": "You are a helpful assistant that helps create Google Slides."},
            {"role": "user", "content": prompt}
        ],
        functions=functions,
        function_call="auto"
    )
    print("Received response from OpenAI")
    
    # Extract function call from response
    message = response.choices[0].message
    if message.function_call:
        function_name = message.function_call.name
        arguments = message.function_call.arguments
        
        print(f"Function call: {function_name}")
        print(f"Arguments: {arguments}")

        # Parse arguments from the string returned by OpenAI
        args = eval(arguments)

        # Call the appropriate function
        if function_name == "create_textbox_with_text":
            create_textbox_with_text(**args)
        elif function_name == "reposition_element":
            reposition_element(**args)
        elif function_name == "create_ellipse_with_text":
            create_ellipse_with_text(**args)
        elif function_name == "create_cloud_with_text":
            create_cloud_with_text(**args)
        elif function_name == "create_ellipse_without_text":
            create_ellipse_without_text(**args)
        elif function_name == "create_cloud_without_text":
            create_cloud_without_text(**args)
        elif function_name == "create_image":
            create_image(**args)
        else:
            print("No function call in the response")
            print("Response content:", message.content)

# # Example prompt that the user could provide
# user_prompt = "Create a rectangle shape with text 'Welcome to the presentation' on the first page of the presentation."
# 
# try:
#     call_openai_function(user_prompt)
# except Exception as e:
#     print(f"An error occurred: {e}")
# 
# print("Script finished")
