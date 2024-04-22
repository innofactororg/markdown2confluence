import json
import logging
import requests
from requests.auth import HTTPBasicAuth
from config.get_config import get_config

CONFIG = get_config()


#
# Function for create page with CONTENT
#


def create_page(title, content, parent_page_id, login, password):

    # descripe json query
    newPageJSONQueryString = """
    {
        "type": "page",
        "title": "DEFAULT PAGE TITLE",
        "ancestors": [
            {
            "id": 111
            }
        ],
        "space": {
            "key": "DEFAULT KEY"
        },
        "body": {
            "storage": {
                "value": "DEFAULT PAGE CONTENT",
                "representation": "storage"
            }
        }
    }
    """

    # load json from string
    newPagejsonQuery = json.loads(newPageJSONQueryString)

    # the key of Confluence space for content publishing
    newPagejsonQuery['space']['key'] = CONFIG["confluence_space"]

    # check of input of the ParentPageID
    if parent_page_id is None:
        # this is the root of out pages tree
        newPagejsonQuery['ancestors'][0]['id'] = CONFIG["confluence_parent_page_id"]
    else:
        newPagejsonQuery['ancestors'][0]['id'] = str(
            parent_page_id)  # this is the branch of our tree

    # add search pattern to the title for the ability to find and delete this page in the future
    newPagejsonQuery['title'] = title + "  " + \
        str(CONFIG["confluence_search_pattern"])
    # add content if the page from the input parameter
    newPagejsonQuery['body']['storage']['value'] = "<p style=\"background-color:#e7be17;\">This page is autogenerated. Make changes in the GitHub repository: " + \
        "<b><a href=\"https://github.com\">My project</a></b></p>" + content
    # TO DO "<p>This page is autogenerated. Make changes in the GilLab repository: <\p>" +

    logging.info("Create new page: " + newPagejsonQuery['title'])
    logging.debug("with content: " +
                  newPagejsonQuery['body']['storage']['value'])
    logging.debug(json.dumps(newPagejsonQuery, indent=4, sort_keys=True))

    # make call to create new page
    logging.debug("Calling URL: " + str(CONFIG["confluence_url"]) + "content/")

    response = requests.post(
        url=CONFIG["confluence_url"] + "content/",
        json=newPagejsonQuery,
        auth=HTTPBasicAuth(login, password),
        verify=True)

    logging.debug(response.status_code)
    if response.status_code == 200:
        logging.info("Created successfully")
    logging.debug(json.dumps(json.loads(
        response.text), indent=4, sort_keys=True))

    # return new page id
    logging.debug("Returning created page id: " +
                  json.loads(response.text)['id'])
    return json.loads(response.text)['id']


#
# Function for searching pages with SEARCH TEST in the title
#
def search_pages(login, password):
    # make call using Confluence query language
    # GET /rest/api/search?cql=text~%7B%22SEARCH%20PATTERN%22%7D+and+type=page+and+space=%2212345%22&limit=1000 HTTP/1.1" 200
    # "cqlQuery": "parent=301176119 and text~{\"SEARCH PATTERN\"} and type=page and space=\"12345\""

    logging.debug("Calling URL: " + str(CONFIG["confluence_url"]) + "search?cql=parent=" + str(CONFIG["confluence_parent_page_id"]) +
                  "+and+text~{\"" + str(CONFIG["confluence_search_pattern"]) +
                  "\"}+and+type=page+and+space=\"" +
                  str(CONFIG["confluence_space"]) +
                  "\"&limit=1000")

    response = requests.get(
        url=str(CONFIG["confluence_url"]) + "search?cql=text~{\"" + str(CONFIG["confluence_search_pattern"]) +
        "\"}+and+type=page+and+space=\"" +
        str(CONFIG["confluence_space"]) +
        "\"&limit=1000",
        auth=HTTPBasicAuth(login, password),
        verify=True)

    logging.debug(response.status_code)
    logging.debug(json.dumps(json.loads(
        response.text), indent=4, sort_keys=True))

    # extract page's IDs from response JSON
    results = json.loads(response.text)
    foundPages = []

    for result in results['results']:
        foundPages.append(result['content']['id'])  # add found page id
        logging.info("Found page: " + result['content']['id'] +
                     " with title: " + result['content']['title'])

    logging.debug("Found pages in space " + str(CONFIG["confluence_space"]) + " and parent page: " +
                  str(CONFIG["confluence_parent_page_id"]) + " and search text: " +
                  str(CONFIG["confluence_search_pattern"]) + ": " + str(foundPages))

    return foundPages


#
# Function for deleting pages
#
def delete_pages(pages_id_list, login, password):

    deletedPages = []

    for page in pages_id_list:
        logging.info("Delete page: " + str(page))
        logging.debug("Calling URL: " +
                      str(CONFIG["confluence_url"]) + "content/" + str(page))
        response = requests.delete(
            url=str(CONFIG["confluence_url"]) + "content/" + str(page),
            auth=HTTPBasicAuth(login, password),
            verify=True)
        logging.debug("Delete status code: " + str(response.status_code))
        if response.status_code == 204:
            logging.info("Deleted successfully")

    return deletedPages

#
# Function for attaching file
#


def attach_file(page_id, attached_file, login, password):
    """
    Attach a file to a Confluence page.

    Args:
        page_id (str): ID of the Confluence page to attach the file to.
        attached_file (file): The file to be attached.
        login (str): The login username for authentication.
        password (str): The login password for authentication.

    Returns:
        str: The ID of the attached file or None if the attachment failed.
    """

    # Construct the API endpoint URL
    api_url = f"{CONFIG['confluence_url']}content/{page_id}/child/attachment"

    # Log the API call
    logging.debug(f"Calling URL: {api_url}")

    # Set up file and comment data, headers, and disable SSL verification
    attached_file_structure = {'file': attached_file}
    attached_values = {'comment': 'File was attached by the script'}
    attached_header = {
        "Accept": "application/json",
        "X-Atlassian-Token": "nocheck"  # Disable token check to avoid 403 status code
    }

    # Make the POST request to attach the file
    response = requests.post(
        url=api_url,
        files=attached_file_structure,
        data=attached_values,
        auth=HTTPBasicAuth(login, password),
        headers=attached_header,
        verify=True  # Not recommended in production
    )

    # Log the response status code
    logging.debug(response.status_code)

    if response.status_code == 200:
        # Log success and parse JSON response
        logging.info("File was attached successfully")
        response_data = json.loads(response.text)
        logging.debug(json.dumps(response_data, indent=4, sort_keys=True))

        # Extract and return the ID of the attached file
        attached_file_id = response_data['results'][0]['id']
        logging.debug(f"Returning attached file id: {attached_file_id}")
        return attached_file_id
    else:
        # Log failure and return None
        logging.error("File has not been attached")
        return None

    if response.status_code == 200:
        # Log success and parse JSON response
        logging.info("File was attached successfully")
        response_data = json.loads(response.text)
        logging.debug(json.dumps(response_data, indent=4, sort_keys=True))

        # Extract and return the ID of the attached file
        attached_file_id = response_data['results'][0]['id']
        logging.debug(f"Returning attached file id: {attached_file_id}")
        return attached_file_id
    else:
        # Log failure and return None
        logging.error("File has not been attached")
        return None