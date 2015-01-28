import confluence
import re
from itertools import groupby

def get_itissues():
    """Test."""

    itissues_page = "IT ISSUES 2015"
    space = 'PROJ'
    #space = 'Green'

    server = confluence.connect()
    token = confluence.login(server, 'admin', 'fanjie427')
    #token = confluence.login(server, 'gyao', 'vagrant1.9')

    itissues = confluence.get_list_from_pagetable(space=space, name=itissues_page, skip_th=True, server=server, token=token)

    grouped_itissues = []
    for key, group in groupby(itissues, lambda x: '['+str(x[7])+']'+str(x[3])):
        grouped_itissues = grouped_itissues + \
                           [ {'key': key, 'events': list(group)}]

    #for i in grouped_itissues:
        #print i['key']
        #f = i['events'][0][7]
        #s = i['events'][0][3]
        #print s
        #print "%s has %s events" %(i['key'], len(i['events']))
        #for e in i['events']:
        #    print "%-8s : %s" %(e[2], e[6])
    return grouped_itissues


def get_open_itissues():

    itissues = get_itissues()

    open_itissues = []

    for i in itissues:
        if i['events'][0][2] != 'Resolved':
            #print i['events'][0][2]
            open_itissues = open_itissues + [i]

    #for i in open_itissues:
    #    print "%s : [%s]%s" %(i['key'], i['events'][0][7], i['events'][0][3])

    return open_itissues


def get_closed_itissues():

    itissues = get_itissues()

    closed_itissues = []

    for i in itissues:
        if i['events'][0][2] == 'Resolved':
            #print i['events'][0][2]
            closed_itissues = closed_itissues + [i]

    #for i in closed_itissues:
    #    print "key = %s, firstalert = %s, summary = %s" %(i['key'], i['events'][0][7], i['events'][0][3])

    return closed_itissues

def update_itissues(itissue, skip_th=True):

    name = "Confluence Table"
    space = 'PROJ'

    server = confluence.connect()
    token = confluence.login(server, 'admin', 'fanjie427')

    itissues = get_itissues()

    update = False

    table_data = ''

    for i in itissues:
        table_data = table_data + '<tr>'
        if i[7] == itissue[7]: #Date & Time of First Alert:
            for j in itissue:
                table_data = table_data + '<td>' + j + '</td>'
                update = True
        else:
            for j in i:
                table_data = table_data + '<td>' + j + '</td>'
        table_data = table_data + '</tr>'

    if not update:
        new_line  = '<tr>'
        for j in itissue:
            new_line = new_line + '<td>' + j + '</td>'
        new_line = new_line + '</tr>'
        table_data = new_line + table_data

    page = confluence.get_page(space=space, name=name, server=server, token=token)
    content = page['content']

    if skip_th:
        #page['content'] = content.replace('</th></tr>*</tbody>', '</th></tr>%s</tbody>' % table_data)
        page['content'] = re.sub(r'</th></tr>(.*)</tbody>', '</th></tr>' + table_data + '</tbody>', content)
    else:
        #page['content'] = content.replace('<tbody>*</tbody>', '<tbody>%s</tbody>' % table_data)
        page['content'] = re.sub(r'<tbody>(.*)</tbody>','<tbody>' + table_data + '</tbody>',content)

    return confluence.update_page(page, server=server, token=token)


def resolve_itissue(itissue):

    itissue[2] = 'Resolved'
    return update_itissues(itissue)

def reopen_itissue(itissue):

    itissue[2] = 'Reopen'
    return update_itissues(itissue)

if __name__ == "__main__":

    itissues = get_open_itissues()
    #itissues = get_closed_itissues()
    for i in itissues:
        print i['key']
        for e in i['events']:
            print e
    #reopen_itissue(itissue)
    #resolve_itissue(itissue)
    #itissue[2] = 'New'
    #itissue[7] = '2015-01-14 03:08:47 AEST'
    #update_itissues(itissue)