import os
import sys
import traceback
import requests
from bs4 import BeautifulSoup


DEFAULT_CONFLUENCE_SERVER = 'https://garyjyao.atlassian.net/wiki'
#DEFAULT_CONFLUENCE_SERVER = 'https://confluence-test.wotifgroup.com'

DEFAULT_REST_API_ENDPOINT = '/rest/api/content/'

def connect(confluence_server=DEFAULT_CONFLUENCE_SERVER):
    if sys.version_info > (3, 0):
        try:
            from xmlrpc.client import ServerProxy
            server = ServerProxy('%s/rpc/xmlrpc' % confluence_server)
        except ImportError as e:
            print("Unable to import xmlrpc.client: %s" % e)
            return False
        except Exception as e:
            print("Unable to connect to %s: %s" % (confluence_server, e))
            return False
    else:
        try:
            from xmlrpclib import Server
            server = Server('%s/rpc/xmlrpc' % confluence_server)
        except ImportError as e:
            print("Unable to import xmlrpclib: %s" % e)
            return False
        except Exception as e:
            print("Unable to connect to %s: %s" % (confluence_server, e))
            return False

    return server


def login(server, username=None, password=None):
    if not username or not password:
        print('Username or password not supplied.')
        return False
    try:
        token = server.confluence2.login(username, password)
    except Exception as e:
        print("Error login to confluence: %s" % e)
        return False

    return token


def page_exists(space=None, name=None, page_id=None, confluence_server=DEFAULT_CONFLUENCE_SERVER, server=None, token=None):
    """Check if a page exists, requires either a page_id or a space and a name."""
    if (not name and not page_id):
        print('Must provide either the space and name of the Confluence page, or its page_id (Error #1)')
        return False

    if name and not space:
        print("To retrieve a Confluence page by name, you must also specify its space")
        return False

    if server is None:
        server = connect(confluence_server)

    if token is None:
        token = login(server)

    try:
        if page_id:
            server.confluence2.getPageSummary(token, str(page_id))
        else:
            server.confluence2.getPageSummary(token, space, name)
        return True
    except Exception:
        return False


def move_page(space=None, name=None, page_id=None, new_parent_id=None, new_parent=None, confluence_server=DEFAULT_CONFLUENCE_SERVER, server=None, token=None):
    """Move a page from its current parent page to a new parent."""
    if server is None:
        server = connect(confluence_server)

    if token is None:
        token = login(server)

    check_page_exists(space=space, name=name, page_id=page_id, server=server, token=token)
    current_page = get_page(space=space, name=name, page_id=page_id, server=server, token=token)

    check_page_exists(space=space, name=new_parent, page_id=new_parent_id, server=server, token=token)
    new_parent_page = get_page(space=space, name=new_parent, page_id=new_parent_id, server=server, token=token)

    current_page['parentId'] = new_parent_page['id']
    try:
        server.confluence2.storePage(token, current_page)
        return True
    except Exception as e:
        print("Error moving page with id %s: %s" % (current_page['id'], e))



def get_page(space=None, name=None, page_id=None, confluence_server=DEFAULT_CONFLUENCE_SERVER, server=None, token=None):
    """Returns a page object (see: https://developer.atlassian.com/display/CONFDEV/Remote+Confluence+Data+Objects#RemoteConfluenceDataObjects-pagePage)
    Requires either a space and a name, or a page_id"""
    if (not name and not page_id):
        print('Supply either the space and name of the Confluence page, or its page_id (Error #1)')

    if name and not space:
        print("To retrieve a Confluence page by name, you must also specify its space")

    if server is None:
        server = connect(confluence_server)

    if token is None:
        token = login(server)

    if name:
        try:
            return server.confluence2.getPage(token, space, name)
        except Exception as e:
            print("Error retrieving page '%s:%s' from Confluence: %s" % (space, name, e))

    try:
        return server.confluence2.getPage(token, str(page_id))
    except Exception as e:
        print("Error retrieving page with id '%s' from Confluence: %s" % (page_id, e))


def rename_page(new_title, space=None, name=None, page_id=None, confluence_server=DEFAULT_CONFLUENCE_SERVER, server=None, token=None):
    if (not name and not page_id):
        print('Supply either the space and name of the Confluence page, or its page_id (Error #1)')

    if name and not space:
        print("To rename a Confluence page by name, you must also specify its space")

    if server is None:
        server = connect(confluence_server)

    if token is None:
        token = login(server)


    if page_id:
        try:
            page_object = server.confluence2.getPage(token, page_id)
            page_object['title'] = new_title
            server.confluence2.storePage(token, page_object)
            return True
        except Exception as e:
            print("Error saving page with id '%s' in Confluence: %s" % (page_id, traceback.format_exc(e)))
    else:
        try:
            page_object = server.confluence2.getPage(token, space, name)
            page_object['title'] = new_title
            server.confluence2.storePage(token, page_object)
            return True
        except Exception as e:
            print("Error saving page '%s:%s' in Confluence: %s" % (space, name, e))



def remove_page(space=None, name=None, page_id=None, confluence_server=DEFAULT_CONFLUENCE_SERVER, server=None, token=None):
    if (not name and not page_id):
        print('Supply either the space and name of the Confluence page, or its page_id (Error #1)')

    if name and not space:
        print("To remove a Confluence page by name, you must also specify its space")

    if server is None:
        server = connect(confluence_server)

    if token is None:
        token = login(server)

    if name and not page_id:
        check_page_exists(space=space, name=name, page_id=page_id, server=server, token=token)
        page_object = get_page(space, name, server=server, token=token)
        page_id = page_object['id']

    try:
        server.confluence2.removePage(token, page_id)
        return True
    except Exception as e:
        print("Error removing page with id '%s' from Confluence: %s" % (page_id, e))


def update_page(page_object, confluence_server=DEFAULT_CONFLUENCE_SERVER, server=None, token=None):
    """not tested"""
    if server is None:
        server = connect(confluence_server)

    if token is None:
        token = login(server)

    try:
        server.confluence2.storePage(token, page_object)
        return True
    except Exception as e:
        print("Error saving page with id '%s' in Confluence: %s" % (page_object['id'], e))


def add_page(space, name, content, wiki=True, parent=None, parent_id=None, confluence_server=DEFAULT_CONFLUENCE_SERVER, server=None, token=None):
    """not tested"""
    if server is None:
        server = connect_to_confluence(confluence_server)

    if token is None:
        token = login_to_confluence(server)

    new_page = {
        'title': name,
        'space': space
    }

    if wiki:
        new_page['content'] = server.confluence2.convertWikiToStorageFormat(token, content)
    else:
        new_page['content'] = content

    if parent_id:
        new_page['parentId'] = parent_id
    elif parent:
        check_page_exists(space=space, name=parent, server=server, token=token)
        parent_page = get_page(space, parent, server=server, token=token)
        new_page['parentId'] = parent_page['id']

    try:
        return server.confluence2.storePage(token, new_page)
    except Exception as e:
        print("Unable to save page '%s:%s' in Confluence: %s" % (space, name, e))


def get_attachments(page_id, confluence_server=DEFAULT_CONFLUENCE_SERVER, server=None, token=None):
    if server is None:
        server = connec(confluence_server)

    if token is None:
        token = login(server)

    return server.confluence2.getAttachments(token, page_id)


def get_attachment_data(page_id, filename, version='0', confluence_server=DEFAULT_CONFLUENCE_SERVER, server=None, token=None):
    if server is None:
        server = connect(confluence_server)

    if token is None:
        token = login(server)

    return server.confluence2.getAttachmentData(token, page_id, filename, version).data


def add_attachment(filename, space=None, parent=None, parent_id=None, comment=None, content_type='text/plain', confluence_server=DEFAULT_CONFLUENCE_SERVER, server=None, token=None):
    if (not parent and not parent_id):
        print('Supply either the space and parent name of the Confluence page, or its parent page_id (Error #1)')

    if parent and not space:
        print("To add an attachment to a Confluence page by parent name, you must also specify its space")

    if server is None:
        server = connect(confluence_server)

    if token is None:
        token = login(server)

    if not comment:
        comment = os.path.basename(filename)

    attachment = {
        'fileName': os.path.basename(filename),
        'contentType': content_type,
        'comment': comment
    }

    if parent_id:
        attachment['pageId'] = parent_id
    else:
        check_page_exists(space=space, name=parent, server=server, token=token)
        parent_object = get_page(space, parent, server=server, token=token)
        attachment['pageId'] = parent_object['id']

    if sys.version_info > (3, 0):
        try:
            from xmlrpc.client import Binary
        except ImportError as e:
            print("Unable to import xmlrpc.client: %s" % e)
    else:
        try:
            from xmlrpclib import Binary
        except ImportError as e:
            print("Unable to import xmlrpclib: %s" % e)

    try:
        f = open(filename, 'r')
        content = Binary(f.read())
        f.close()
    except Exception as e:
        print("Could not read content of downloaded attachment file '%s': %s" % (filename, e))
        return False

    try:
        server.confluence2.addAttachment(token, attachment['pageId'], attachment, content)
    except Exception as e:
        print("Could not add attachment '%s' to Confluence page '%s:%s'. Error: %s" % (filename, space, parent, e))

    print("Successfully uploaded attachment %s to %s:%s." % (filename, space, parent))


def get_labels(space=None, name=None, page_id=None, confluence_server=DEFAULT_CONFLUENCE_SERVER, server=None, token=None):
    if not name and not page_id:
        print('Supply either the space and name of the Confluence page, or its page_id (Error #1)')

    if server is None:
        server = connect(confluence_server)

    if token is None:
        token = login(server)

    check_page_exists(space=space, name=name, page_id=page_id, server=server, token=token)
    page_object = get_page(space, name, page_id, server=server, token=token)
    return server.confluence2.getLabelsById(token, page_object['id'])


def add_label(label, space=None, name=None, page_id=None, confluence_server=DEFAULT_CONFLUENCE_SERVER, server=None, token=None):
    if not name and not page_id:
        print('Supply either the space and name of the Confluence page, or its page_id (Error #1)')

    if server is None:
        server = connect(confluence_server)

    if token is None:
        token = login(server)

    check_page_exists(space=space, name=name, page_id=page_id, server=server, token=token)
    page_object = get_page(space, name, page_id, server=server, token=token)
    return server.confluence2.addLabelByName(token, label, page_object['id'])


def remove_label(label, space=None, name=None, page_id=None, confluence_server=DEFAULT_CONFLUENCE_SERVER, server=None, token=None):
    if not name and not page_id:
        print('Supply either the space and name of the Confluence page, or its page_id (Error #1)')

    if server is None:
        server = connect(confluence_server)

    if token is None:
        token = login(server)

    check_page_exists(space=space, name=name, page_id=page_id, server=server, token=token)
    page_object = get_page(space, name, page_id, server=server, token=token)
    return server.confluence2.removeLabelByName(token, label, page_object['id'])


def get_user(username, confluence_server=DEFAULT_CONFLUENCE_SERVER, server=None, token=None):

    if server is None:
        server = connect(confluence_server)

    if token is None:
        token = login(server)

    try:
        return server.confluence2.getUser(token, username)
    except Exception:
        print("Unknown confluence user '%s'" % username)


def get_user_information(username, confluence_server=DEFAULT_CONFLUENCE_SERVER, server=None, token=None):

    if server is None:
        server = connect(confluence_server)
        if server is None:
            return False

    if token is None:
        token = login(server)
        if token is None:
            return False

    return server.confluence2.getUserInformation(token, username)


def build_user_link(username, server, token):
    try:
        user = get_user(username, server=server, token=token)
        return "<ac:link><ri:user ri:userkey=\"%s\"/></ac:link>" % user['key']
    except Exception:
        return "**UNKNOWN USER!**"


def check_page_exists(space=None, name=None, page_id=None, server=None, token=None):
    if not page_exists(space, name, page_id, server=server, token=token):
        if page_id:
            print("Could not find Confluence page with id '%s'" % page_id)
        else:
            print("Could not find Confluence page with name '%s:%s'" % (space, name))


def get_pages_by_label(space_key, match_label, confluence_restapi=DEFAULT_REST_API_ENDPOINT,confluence_server=DEFAULT_CONFLUENCE_SERVER):

    confluence_username='admin'
    confluence_password='fanjie427'
    url = confluence_server + confluence_restapi
    response = requests.get(url, params={'spaceKey' : space_key}, auth=(confluence_username, confluence_password))
    if not response:
        exit()
    pages = response.json()
    match_pages = []
    while True:
        for page in pages["results"]:
            print 'Examing: ' + page["title"]
            #print page
            url = confluence_server + DEFAULT_REST_API_ENDPOINT + page["id"] +'/label'
            print url
            r = requests.get(url, params={'spaceKey' : space_key}, auth=(confluence_username, confluence_password))
            if not r: break
            labels = r.json()
            for label in labels["results"]:
                if label["name"] == match_label:
                    match_pages.append(page)
                    break

        if not ("next" in pages["_links"].keys()): break
        url = confluence_server +  pages["_links"]["next"]
        print url
        response = requests.get(url, params={'spaceKey' : space_key}, auth=(confluence_username, confluence_password))
        if not response: break
        pages = response.json()

    for page in match_pages:
        print page["title"]


def get_list_from_pagetable(space=None, name=None, page_id=None, skip_th=True, confluence_server=DEFAULT_CONFLUENCE_SERVER, server=None, token=None):
    """Returns a list object converting from the first table on a confluence page
    Requires either a space and a name, or a page_id"""
    page = get_page(space,name,page_id, confluence_server, server,token)

    soup = BeautifulSoup(page['content'])
    table = soup.table
    list = [[cell.get_text().encode("utf-8") for cell in row("td")] for row in table("tr")]
    if skip_th:
        return list[1:]
    else:
        return list


def update_list_to_pagetable(newlist=None, space=None, name=None, page_id=None, skip_th=True, confluence_server=DEFAULT_CONFLUENCE_SERVER, server=None, token=None):
    """Returns a list object converting from the first table on a confluence page
    Requires either a space and a name, or a page_id"""
    page = get_page(space,name,page_id, confluence_server, server,token)

    soup = BeautifulSoup(page['content'])
    table = soup.table
    list = [[cell.string for cell in row("td")] for row in table("tr")]


