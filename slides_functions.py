import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# this should be default ran at the start of opening the app
def create_slide(presentation_id, page_id):
  """
  Creates the Presentation the user has access to.
  Load pre-authorized user credentials from the environment.
  TODO(developer) - See https://developers.google.com/identity
  for guides on implementing OAuth2 for the application.\n
  """
  creds, _ = google.auth.default()
  # pylint: disable=maybe-no-member
  try:
    service = build("slides", "v1", credentials=creds)
    # Add a slide at index 1 using the predefined
    # 'TITLE_AND_TWO_COLUMNS' layout and the ID page_id.
    requests = [
        {
            "createSlide": {
                "objectId": page_id,
                "insertionIndex": "1",
                "slideLayoutReference": {
                    "predefinedLayout": "TITLE_AND_TWO_COLUMNS"
                },
            }
        }
    ]

    # If you wish to populate the slide with elements,
    # add element create requests here, using the page_id.

    # Execute the request.
    body = {"requests": requests}
    response = (
        service.presentations()
        .batchUpdate(presentationId=presentation_id, body=body)
        .execute()
    )
    create_slide_response = response.get("replies")[0].get("createSlide")
    print(f"Created slide with ID:{(create_slide_response.get('objectId'))}")
  except HttpError as error:
    print(f"An error occurred: {error}")
    print("Slides not created")
    return error

  return response

#oepnai generates unique elementID
#come up with height, width, xpos, ypos of textbox
#presentation_id should be constant

def create_textbox_with_text(presentation_id, page_id, unique_elementID, textheight, textwidth, xpos, ypos, text_string):
  """
  Creates the textbox with text, the user has access to.
  Load pre-authorized user credentials from the environment.
  TODO(developer) - See https://developers.google.com/identity
  for guides on implementing OAuth2 for the application.
  """
  creds, _ = google.auth.default() 
  # pylint: disable=maybe-no-member
  try:
    service = build("slides", "v1", credentials=creds)
    # Create a new square textbox, using the supplied element ID.
    element_id = unique_elementID
    heightpt = {"magnitude": textheight, "unit": "PT"}
    widthpt = {"magnitude": textwidth, "unit": "PT"}
    requests = [
        {
            "createShape": {
                "objectId": element_id,
                "shapeType": "TEXT_BOX",
                "elementProperties": {
                    "pageObjectId": page_id,
                    "size": {"height": heightpt, "width": widthpt},
                    "transform": {
                        "scaleX": 1,
                        "scaleY": 1,
                        "translateX": xpos,
                        "translateY": ypos,
                        "unit": "PT",
                    },
                },
            }
        },
        # Insert text into the box, using the supplied element ID.
        {
            "insertText": {
                "objectId": element_id,
                "insertionIndex": 0,
                "text": text_string,
            }
        },
    ]

    # Execute the request.
    body = {"requests": requests}
    response = (
        service.presentations()
        .batchUpdate(presentationId=presentation_id, body=body)
        .execute()
    )
    create_shape_response = response.get("replies")[0].get("createShape")
    print(f"Created textbox with ID:{(create_shape_response.get('objectId'))}")
  except HttpError as error:
    print(f"An error occurred: {error}")

    return error

  return response

#
def create_textbox_with_text(presentation_id, page_id, unique_elementID, textheight, textwidth, xpos, ypos, text_string):
  """
  Creates the textbox with text, the user has access to.
  Load pre-authorized user credentials from the environment.
  TODO(developer) - See https://developers.google.com/identity
  for guides on implementing OAuth2 for the application.
  """
  creds, _ = google.auth.default() 
  # pylint: disable=maybe-no-member
  try:
    service = build("slides", "v1", credentials=creds)
    # Create a new square textbox, using the supplied element ID.
    element_id = unique_elementID
    heightpt = {"magnitude": textheight, "unit": "PT"}
    widthpt = {"magnitude": textwidth, "unit": "PT"}
    requests = [
        {
            "createShape": {
                "objectId": element_id,
                "shapeType": "TEXT_BOX",
                "elementProperties": {
                    "pageObjectId": page_id,
                    "size": {"height": heightpt, "width": widthpt},
                    "transform": {
                        "scaleX": 1,
                        "scaleY": 1,
                        "translateX": xpos,
                        "translateY": ypos,
                        "unit": "PT",
                    },
                },
            }
        },
        # Insert text into the box, using the supplied element ID.
        {
            "insertText": {
                "objectId": element_id,
                "insertionIndex": 0,
                "text": text_string,
            }
        },
    ]

    # Execute the request.
    body = {"requests": requests}
    response = (
        service.presentations()
        .batchUpdate(presentationId=presentation_id, body=body)
        .execute()
    )
    create_shape_response = response.get("replies")[0].get("createShape")
    print(f"Created textbox with ID:{(create_shape_response.get('objectId'))}")
  except HttpError as error:
    print(f"An error occurred: {error}")

    return error

  return response



if __name__ == "__main__":
  # Put the presentation_id, Page_id of slides whose list needs
  # to be submitted.
  create_slide("12SQU9Ik-ShXecJoMtT-LlNwEPiFR7AadnxV2KiBXCnE", "My4ndpage")
