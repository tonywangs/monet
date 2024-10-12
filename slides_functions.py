import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
import json

SCOPES = ["https://www.googleapis.com/auth/presentations"]

presentation_id = "1KJTodHq2WmQwTAgOV-QClp88CRYGd9PQtp_qQtgUmZs"
page_id = "My4thpage"


# this should be default ran at the start of opening the app
def create_slide():
    """
    Creates the Presentation the user has access to.
    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.\n
    """
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
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
        # print(f"Created slide with ID:{(create_slide_response.get('objectId'))}")
    except HttpError as error:
        print(f"An error occurred: {error}")
        print("Slides not created")
        return error

    return response


def create_textbox_with_text(
    unique_elementID, textheight, textwidth, xpos, ypos, text_string
):
    """
    Creates the textbox with text, the user has access to.
    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
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
        body = {"requests": requests}
        response = (
            service.presentations()
            .batchUpdate(presentationId=presentation_id, body=body)
            .execute()
        )
        create_shape_response = response.get("replies")[0].get("createtextboxwithtext")
        # print(f"Created textbox with ID:{(create_shape_response.get('objectId'))}")
    except HttpError as error:
        print(f"An error occurred: {error}")

        return error

    return response


def reposition_element(element_id, textheight, textwidth, xpos, ypos, text_string):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # pylint: disable=maybe-no-member
    try:
        service = build("slides", "v1", credentials=creds)
        # Create a new square textbox, using the supplied element ID.
        element_id = element_id
        heightpt = {"magnitude": textheight, "unit": "PT"}
        widthpt = {"magnitude": textwidth, "unit": "PT"}
        # Create a request to update the element's position
        requests = [
            {
                "updatePageElementTransform": {
                    "objectId": element_id,
                    "transform": {
                        "scaleX": 1,
                        "scaleY": 1,
                        "translateX": xpos,
                        "translateY": ypos,
                        "unit": "PT",
                    },
                    "applyMode": "RELATIVE",
                }
            }
        ]

        # # Optionally resize the element
        # if textwidth and textheight:
        #     requests.append(
        #         {
        #             "updatePageElementProperties": {
        #                 "objectId": element_id,
        #                 "pageElementProperties": {
        #                     "size": {
        #                         "height": {"magnitude": textheight, "unit": "PT"},
        #                         "width": {"magnitude": textwidth, "unit": "PT"},
        #                     }
        #                 },
        #                 "fields": "size",
        #             }
        #         }
        #     )
        body = {"requests": requests}
        response = (
            service.presentations()
            .batchUpdate(presentationId=presentation_id, body=body)
            .execute()
        )
        create_shape_response = response.get("replies")[0].get("reposition")
        # print(f"reposition:{(create_shape_response.get('objectId'))}")
    except HttpError as error:
        print(f"An error occurred: {error}")

        return response


# same as above but puts text in a shape that is not a textbox.
# need to give shape input from given list of shapes
def create_shape_with_text(
    unique_elementID, textheight, textwidth, xpos, ypos, text_string, shape
):
    """
    Creates the textbox with text, the user has access to.
    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
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
                    "shapeType": shape,
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
        create_shape_response = response.get("replies")[0].get("createshapewithtext")
        # print(f"Created textbox with ID:{(create_shape_response.get('objectId'))}")
    except HttpError as error:
        print(f"An error occurred: {error}")

        return error

    return response


def create_ellipse_with_text(
    unique_elementID, textheight, textwidth, xpos, ypos, text_string
):
    """
    Creates the textbox with text, the user has access to.
    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """
    shape = "ELLIPSE"
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
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
                    "shapeType": shape,
                    "shapeProperties": {
                        "shapeBackgroundFill": {
                            "solidFill": {
                                "color": {
                                    "rgbColor": {
                                        "red": 0.0,
                                        "green": 0.0,
                                        "blue": 0.0
                                    }
                                }
                            }
                        }
                    },
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
        create_shape_response = response.get("replies")[0].get("createshapewithtext")
        print(f"Created textbox with ID:{(create_shape_response.get('objectId'))}")
    except HttpError as error:
        print(f"An error occurred: {error}")

        return error

    return response


def create_cloud_with_text(
    unique_elementID, textheight, textwidth, xpos, ypos, text_string
):
    """
    Creates the textbox with text, the user has access to.
    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """
    shape = "CLOUD"
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
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
                    "shapeType": shape,
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
        create_shape_response = response.get("replies")[0].get("createshapewithtext")
        # print(f"Created textbox with ID:{(create_shape_response.get('objectId'))}")
    except HttpError as error:
        print(f"An error occurred: {error}")

        return error

    return response


def create_rectangle_without_text(
    unique_elementID, shapeheight, shapewidth, xpos, ypos
):
    """
    Creates the textbox with text, the user has access to.
    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """
    shape = "RECTANGLE"
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # pylint: disable=maybe-no-member
    try:
        service = build("slides", "v1", credentials=creds)
        # Create a new square textbox, using the supplied element ID.
        element_id = unique_elementID
        heightpt = {"magnitude": shapeheight, "unit": "PT"}
        widthpt = {"magnitude": shapewidth, "unit": "PT"}
        requests = [
            {
                "createShape": {
                    "objectId": element_id,
                    "shapeType": shape,
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
            }
        ]
        # Execute the request.
        body = {"requests": requests}
        response = (
            service.presentations()
            .batchUpdate(presentationId=presentation_id, body=body)
            .execute()
        )
        create_shape_response = response.get("replies")[0].get("createShapewithouttext")
        # print(f"Created textbox with ID:{(create_shape_response.get('objectId'))}")
    except HttpError as error:
        print(f"An error occurred: {error}")

        return error

    return response


def create_ellipse_without_text(unique_elementID, shapeheight, shapewidth, xpos, ypos):
    """
    Creates the textbox with text, the user has access to.
    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """
    shape = "ELLIPSE"
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # pylint: disable=maybe-no-member
    try:
        service = build("slides", "v1", credentials=creds)
        # Create a new square textbox, using the supplied element ID.
        element_id = unique_elementID
        heightpt = {"magnitude": shapeheight, "unit": "PT"}
        widthpt = {"magnitude": shapewidth, "unit": "PT"}
        requests = [
            {
                "createShape": {
                    "objectId": element_id,
                    "shapeType": shape,
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
            }
        ]
        # Execute the request.
        body = {"requests": requests}
        response = (
            service.presentations()
            .batchUpdate(presentationId=presentation_id, body=body)
            .execute()
        )
        create_shape_response = response.get("replies")[0].get("createShapewithouttext")
        # print(f"Created textbox with ID:{(create_shape_response.get('objectId'))}")
    except HttpError as error:
        print(f"An error occurred: {error}")

        return error

    return response


def create_cloud_without_text(unique_elementID, shapeheight, shapewidth, xpos, ypos):
    """
    Creates the textbox with text, the user has access to.
    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """
    shape = "CLOUD"
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # pylint: disable=maybe-no-member
    try:
        service = build("slides", "v1", credentials=creds)
        # Create a new square textbox, using the supplied element ID.
        element_id = unique_elementID
        heightpt = {"magnitude": shapeheight, "unit": "PT"}
        widthpt = {"magnitude": shapewidth, "unit": "PT"}
        requests = [
            {
                "createShape": {
                    "objectId": element_id,
                    "shapeType": shape,
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
            }
        ]
        # Execute the request.
        body = {"requests": requests}
        response = (
            service.presentations()
            .batchUpdate(presentationId=presentation_id, body=body)
            .execute()
        )
        create_shape_response = response.get("replies")[0].get("createShapewithouttext")
        # print(f"Created textbox with ID:{(create_shape_response.get('objectId'))}")
    except HttpError as error:
        print(f"An error occurred: {error}")

        return error

    return response


# empty shape without text
def create_shape_without_text(
    unique_elementID, shapeheight, shapewidth, xpos, ypos, shape
):
    """
    Creates the textbox with text, the user has access to.
    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # pylint: disable=maybe-no-member
    try:
        service = build("slides", "v1", credentials=creds)
        # Create a new square textbox, using the supplied element ID.
        element_id = unique_elementID
        heightpt = {"magnitude": shapeheight, "unit": "PT"}
        widthpt = {"magnitude": shapewidth, "unit": "PT"}
        requests = [
            {
                "createShape": {
                    "objectId": element_id,
                    "shapeType": shape,
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
            }
        ]
        # Execute the request.
        body = {"requests": requests}
        response = (
            service.presentations()
            .batchUpdate(presentationId=presentation_id, body=body)
            .execute()
        )
        create_shape_response = response.get("replies")[0].get("createShapewithouttext")
        # print(f"Created textbox with ID:{(create_shape_response.get('objectId'))}")
    except HttpError as error:
        print(f"An error occurred: {error}")

        return error

    return response


def create_image(imheight, imwidth, img_url, xpos, ypos):
    """
    Creates images the user has access to.
    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """

    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # pylint: disable=maybe-no-member
    try:
        service = build("slides", "v1", credentials=creds)
        # pylint: disable = invalid-name
        IMAGE_URL = img_url
        # pylint: disable=invalid-name
        requests = []
        image_id = "MyImage_11"
        heightemu = {"magnitude": imheight, "unit": "EMU"}
        widthemu = {"magnitude": imwidth, "unit": "EMU"}
        requests.append(
            {
                "createImage": {
                    "objectId": image_id,
                    "url": IMAGE_URL,
                    "elementProperties": {
                        "pageObjectId": page_id,
                        "size": {"height": heightemu, "width": widthemu},
                        "transform": {
                            "scaleX": 1,
                            "scaleY": 1,
                            "translateX": xpos,
                            "translateY": ypos,
                            "unit": "EMU",
                        },
                    },
                }
            }
        )

        # Execute the request.
        body = {"requests": requests}
        response = (
            service.presentations()
            .batchUpdate(presentationId=presentation_id, body=body)
            .execute()
        )
        create_image_response = response.get("replies")[0].get("createImage")
        # print(f"Created image with ID: {(create_image_response.get('objectId'))}")

        return response
    except HttpError as error:
        print(f"An error occurred: {error}")
        print("Images not created")
        return error


if __name__ == "__main__":
    # Put the presentation_id, Page_id of slides whose list needs
    # to be submitted.
    # create_slide()
    # create_cloud_with_text("12345", 100, 100, 10, 10, "testing cloud")
    # reposition_element("12345", -400, 100, 50, 50, "okay changin")
    # create_ellipse_with_text("23445", 100, 100, 100, 100, "testing color")

    create_image(1000000, 1000000, "https://pear-monet.s3.us-east-1.amazonaws.com/Pear_VC_logo.png?response-content-disposition=inline&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEFgaCXVzLWVhc3QtMSJHMEUCIQCw%2BxSAdfzgyJrKetCh48D1WIewvhS1AjrKjjo%2Br1%2F2LwIgBnQYjvbal85vabXpwWIRvgRZUlbxKfMvK3qBocgWThYqhAMIsP%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARADGgw5Njc5NDcxMzQzODkiDMRy%2FuLL6WychkJfMyrYAjfsttbQDFyC8aAZBBS1qinUr4btBqj4VbMgwQt42ZFedI6qwSwwVZZaBGyTXeXqmyL%2FC2YKGwW1k5llB%2FFmINcsfxJ1%2FHdglH4axZTBO0F7%2BiHcNla3t1Oo%2F2pRlEUnOiCCowk9CpqRqRQwRGZq5lMh08K9lUmPRlILEdD5%2F4ZiiYOQkLHuWdsVuXKlVTIUJjG%2BsgMOhRpQjL%2BLvOYFtSgPXvZEJb8BNRK0l5leGU0WSOdo9v7Lbj2m0mQQbHe3Ixjn1fo6dxYMwS6R58vYFTpafBbbmQYIr6sJiBjR6tfHOZKjE5qPaT69OOWU3zt3vEvnCR0KXqEmBieMWdPvpJVku1xu130MLSHqanv2Sva38dCe9ssrQm3mGxctj4ERtVK5s3UuSeI%2BBnbOAbXFRsU9wg8VY1yuL5XO5DdUpJXbxtXB9p%2BSmCWQ6%2FIYq4YfcJXqdkd8ndHPMLOBrLgGOrMCZMQ2%2BGg5kE7oFCOH4mcBBkZhmS%2FMkPa1X0WyuEmBtqCqfhghbnbVFjezrlTEV6SzpVELvgM7PQS0Yg3bEAsNaSEqO46gjagGTzIHPLK%2B3kHAgP1vN6kznaIBThrKCPQD14WTEqnOkRRClR2umesbbQqU3pyzwHD3fiMEvOKDWuvMRg3T7GZar9RyqmHqXE1TBV2fwdcyX7gzvxSJRq1DDgUUodBYAcuj5g%2FgAPPnH0EkMnPhhdv9nmZVIlvZrDb8glD8LV%2FCIbKgHDklaAAjlg1El83e6pOgbdZ2Ti7nkq8eZAxrlBkjZMp%2FVs%2FBYeVs3oUanNSOfn93XfOgr7e3vWku4Yc2TGWq8I7xpPLC9bJJW3nM7LliitzABZWWiV9eUju6Yl6dnZaTpwxgkJmo24edlA%3D%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20241012T233020Z&X-Amz-SignedHeaders=host&X-Amz-Expires=43199&X-Amz-Credential=ASIA6CXRFEW2VV4NPUCT%2F20241012%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=ecbdb2801f0de6e14b12efffe83d2680c973981f26720bccece93461eae5bc1f", 50, 50)

