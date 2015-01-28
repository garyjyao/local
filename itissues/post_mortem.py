from datetime import datetime

import confluence

def create_confluence_itissues_page(subject, status, summary, public, sites, comments,
                                    firstalert, resolution, impact, cause, handler, html_part,
                                    sender):
    """Create a post moterm page from an itissue email ."""

    server = None
    token = None
    itissues_parentpage = "Ongoing IT Issues"
    itissues_template_title = "IT ISSUES ANNOUNCEMENT TEMPLATE"
    space = 'proj'

    server = confluence.connect()
    token = confluence.login(server, 'admin', 'fanjie427')

    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    today = datetime.now().strftime('%Y-%m-%d')

    #title = "[%s] %s" % (today, subject)
    title = subject
    if confluence.page_exists(space=space, name=title,
                              server=server, token=token):
        print("Confluence page '%s' already exists!" % (title))
        return False

    itissues_template_page = confluence.get_page(space=space,
                                                 name=itissues_template_title,
                                                 server=server,
                                                 token=token)

    if not itissues_template_page:
        print("Unable to get IT ISSUES ANNOUNCEMENT TEMPLATE from confluence: [%s]" % (itissues_template_title))
        return False

    content = itissues_template_page['content']

    content = content.replace("##now##", now)
    content = content.replace("##subject##", subject)
    content = content.replace("##status##", status)
    content = content.replace("##summary##", summary)
    content = content.replace("##public##", public)
    content = content.replace("##sites##", sites)
    content = content.replace("##comments##", comments)
    content = content.replace("##firstalert##", firstalert)
    content = content.replace("##resolution##", resolution)
    content = content.replace("##impact##", impact)
    content = content.replace("##cause##", cause)
    content = content.replace("##handler##", handler)
    user_link = confluence.build_user_link(sender, server, token)
    content = content.replace("##sender##", user_link)
    content = content.replace("##html_part##", "<h2>" + subject + "</h2>" + html_part)

    new_page = confluence.add_page(space=space,
                                   name=title,
                                   wiki=False,
                                   content=content,
                                   parent=itissues_parentpage,
                                   server=server,
                                   token=token)

    confluence.add_label(
        label="itissue,ongoing",
        space=space,
        name=title,
        server=server,
        token=token)

    print("<br/>IT ISSUE Page is <a href='%s'>%s</a>" % (new_page['url'], title))
    return new_page['id']


def create_confluence_postmortem_page(summary, public, sites, comments,
                                      firstalert, resolution, impact, cause, handler,
                                      sender):
    """Create a post moterm page from an itissue email ."""

    server = None
    token = None
    postmortem_parentpage = "Open Post Mortems"
    postmortem_template_title = "IT Post Mortem Template"
    space = "proj"

    server = confluence.connect()
    token = confluence.login(server, 'admin', 'fanjie427')

    today = datetime.now().strftime('%d%m%Y')

    title = "PM0XXX - %s - %s" % (today, summary)
    if confluence.page_exists(space=space, name=title,
                              server=server, token=token):
        print("Confluence page '%s' already exists!" % (title))
        return False

    postmortem_template_page = confluence.get_page(space=space,
                                                   name=postmortem_template_title,
                                                   server=server,
                                                   token=token)

    if not postmortem_template_page:
        print("Unable to get IT Post Mortem template from confluence: [%s]" % (postmortem_template_title))
        return False

    content = postmortem_template_page['content']

    content = content.replace("##public##", public)
    content = content.replace("##sites##", sites)
    content = content.replace("##comments##", comments)
    content = content.replace("##firstalert##", firstalert)
    content = content.replace("##resolution##", resolution)
    content = content.replace("##impact##", impact)
    content = content.replace("##cause##", cause)
    content = content.replace("##handler##", handler)
    user_link = confluence.build_user_link(sender, server, token)
    content = content.replace("##sender##", user_link)

    new_page = confluence.add_page(space=space,
                                   name=title,
                                   wiki=False,
                                   content=content,
                                   parent=postmortem_parentpage,
                                   server=server,
                                   token=token)

    confluence.add_label(
        label="postmortem,open",
        space=space,
        name=title,
        server=server,
        token=token)

    print("<br/>POST MORTEM Page is <a href='%s'>%s</a>" % (new_page['url'], title))
    return new_page['id']

    # if __name__ == "__main__":