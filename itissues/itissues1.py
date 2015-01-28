#!/usr/bin/env python

import cgi
import cgitb
import MimeWriter
import sys
import smtplib
import base64
import StringIO
import time
import re
import os
import post_mortem

cgitb.enable()

print "Content-type: text/html"
print

form = cgi.FieldStorage()

status = form.getvalue("status")
summary = form.getvalue("summary")
public = form.getvalue("public")
sites = ", ".join(form.getlist("sites"))
comments = form.getvalue("comments")
firstalert = form.getvalue("firstalert")
resolution = form.getvalue("resolution") or "TBA"
impact = form.getvalue("impact") or "Under investigation"
cause = form.getvalue("cause") or "Under investigation"
handler = form.getvalue("handler") or "Group Infrastructure"
postmortem = form.getvalue("postmortem")
#sender = os.environ['REMOTE_USER']
sender = 'admin'

if not summary:
    print "Error: summary is required!"
    sys.exit()

if not comments:
    print "Error: comments are required!"
    sys.exit()

if not firstalert:
    print "Error: first alert is required!"
    sys.exit()

html_comments = re.sub(r'\n', '<br/>', comments)
html_impact = re.sub(r'\n', '<br/>', impact)
html_cause = re.sub(r'\n', '<br/>', cause)

if status == "Update":
  subject = '[Update]*** IT Issues Announcement: %s ***' % summary
elif status == "Resolved":
  subject = '[Resolved]*** IT Issues Announcement: %s ***' % summary
elif status == "Reopen":
  subject = '[Reopen]*** IT Issues Announcement: %s ***' % summary
else:
  subject = '*** IT Issues Announcement: %s ***' % summary
  
to_addr = 'garyjyao@gmail.com'
from_addr = 'garyjyao@gmail.com'
reply_addr = 'garyjyao@gmail.com'
errors_addr = 'garyjyao@gmail.com'

plain_part = '''IT Issues Announcement: %s

Are public facing Wotif Group sites impacted? %s

Sites affected: %s

Summary:
%s

Date & Time of First Alert:
%s

Date & Time of Resolution:
%s

Technical Impact:
%s

Cause:
%s

Being Handled By:
%s

Notification Sent By: %s
''' % (
    summary, public, sites, comments,
    firstalert, resolution, impact, cause, handler,
    sender
)

html_part = '''<p><b>IT Issues Announcement: %s</b></p>
<p><b>Are public facing Wotif Group sites impacted?</b> %s</p>
<p><b>Sites affected:</b> %s</p>
<p><b>Summary:</b><br/>%s</p>
<p><b>Date &amp; Time of First Alert:</b><br/>%s</p>
<p><b>Date &amp; Time of Resolution:</b><br/>%s</p>
<p><b>Technical Impact:</b><br/>%s</p>
<p><b>Cause:</b><br/>%s</p>
<p><b>Being Handled By:</b><br/>%s</p>
<p>Notification Sent By: %s</p>
''' % (
    summary, public, sites, html_comments,
    firstalert, resolution, html_impact, html_cause, handler,
    sender
)

message = StringIO.StringIO()
writer = MimeWriter.MimeWriter(message)
writer.addheader('Subject', subject)
writer.addheader('To', to_addr)
writer.addheader('From', from_addr)
writer.addheader('Reply-To', reply_addr)
writer.addheader('Errors-To', errors_addr)
writer.startmultipartbody('alternative')

# start off with a text/plain part
part = writer.nextpart()
body = part.startbody('text/plain')
body.write(plain_part)

part = writer.nextpart()
body = part.startbody('text/html')
body.write(html_part)

# finish off
writer.lastpart()

# send the mail
# Hubtransport should be used for external mail this will not authenticate
# smtp = smtplib.SMTP('hubtransport.wotifgroup.com')
smtp=smtplib.SMTP('smtp.gmail.com:587')
smtp.ehlo()
smtp.starttls()
smtp.login('garyjyao','Apple1.9')
smtp.sendmail(from_addr, to_addr, message.getvalue())
smtp.quit()

print "Email sent!"

post_mortem.create_confluence_itissues_page(cgi.escape(subject), cgi.escape(status), cgi.escape(summary), cgi.escape(public), cgi.escape(sites), cgi.escape(comments),
                                        cgi.escape(firstalert), cgi.escape(resolution), cgi.escape(impact), cgi.escape(cause), cgi.escape(handler), 
                                        html_part, sender)

if postmortem=="Yes":
   post_mortem.create_confluence_postmortem_page(cgi.escape(summary), cgi.escape(public), cgi.escape(sites), cgi.escape(comments),
                                     cgi.escape(firstalert), cgi.escape(resolution), cgi.escape(impact),
                                     cgi.escape(cause), cgi.escape(handler), sender)
