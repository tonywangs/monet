from openai import OpenAI
import os

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
            "required": ["presentation_id", "page_id", "unique_elementID", "textheight", "textwidth", "xpos", "ypos", "text_string"]
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
            "required": ["presentation_id", "page_id", "element_id", "textheight", "textwidth", "xpos", "ypos", "text_string"]
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
            "required": ["presentation_id", "page_id", "unique_elementID", "textheight", "textwidth", "xpos", "ypos", "text_string"]
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
            "required": ["presentation_id", "page_id", "unique_elementID", "textheight", "textwidth", "xpos", "ypos", "text_string"]
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
            "required": ["presentation_id", "page_id", "unique_elementID", "shapeheight", "shapewidth", "xpos", "ypos"]
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
            "required": ["presentation_id", "page_id", "unique_elementID", "shapeheight", "shapewidth", "xpos", "ypos"]
        }
    }
]

def call_openai_function(prompt):
    print(f"Calling OpenAI function with prompt: {prompt}")
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
        else:
            print("No function call in the response")
            print("Response content:", message.content)

# Example prompt that the user could provide
user_prompt = "Create a rectangle shape with text 'Welcome to the presentation' on the first page of the presentation."

try:
    call_openai_function(user_prompt)
except Exception as e:
    print(f"An error occurred: {e}")

print("Script finished")
