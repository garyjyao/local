#!/usr/bin/env python

import confluence_itissues

open_itissues = confluence_itissues.get_open_itissues()
closed_itissues = confluence_itissues.get_closed_itissues()

print "Content-Type: text/html"
print
print """\
<html>
<head>
<title>IT Issues</title>
<link rel="stylesheet" href="style.css"/>
<script src="confluence_itissue.js"></script>
</head>
<body>
<form action="itissues1.py" method="post" onsubmit="submit.disabled = true; return true;">
<fieldset><legend>IT Issues Announcement</legend>
<label for="status" class="required">Issue Status:</label>
<input type="radio" name="status" value="New" checked="checked" onclick="toggleSummary('New')" /> New
<input type="radio" name="status" value="Update" onclick="toggleSummary('Update')" /> Update
<input type="radio" name="status" value="Resolved" onclick="toggleSummary('Resolved')" /> Resolved
<input type="radio" name="status" value="Reopen" onclick="toggleSummary('Reopen')" /> Reopen <br/>
"""

#<input type="radio" name="status" value="New" checked="checked" onclick="document.getElementById('postmortem').style.display='none',document.getElementById('summary_new').style.display='block',document.getElementById('summary_open').style.display='none'" /> New

#<label for="summary" class="required">Issue Summary (5-6 words):</label> <input type="text" name="summary" size="40"/><br/>
print """<label for="summary" class="required">Issue Summary (5-6 words):</label>"""
#show new itissue input box
print """<div id="summary_new" style="display:block;">
            <input type="text" name="summary" size="40"/>
            <br/>
        </div>"""

#show open itissue dropdown
print """<div id="summary_open" style="display:none;">"""
print """<select name="summary">"""
for i in open_itissues:
    print "<option value=\"", i['key'], "\" onChange=changeIssueOnDisplay(",
    public = i['events'][0][4]
    sites = i['events'][0][5]
    comments = i['events'][0][6]
    firstalert = i['events'][0][7]
    resolution = i['events'][0][8]
    impact = i['events'][0][9]
    cause = i['events'][0][10]
    handler = i['events'][0][11]
    print '"', public, '","', sites, '","', comments, '","', firstalert, '","', resolution, '","', impact, '","', cause, '","', handler, '") >', i['key'], '</option>'

print """</select>"""
print """<br/></div>"""

#show closed itissue dropdown
print """<div id="summary_closed" style="display:none;">"""
print """<select name="summary">"""
for i in closed_itissues:
    print "<option value=\"", i['key'], "\" onChange=changeIssueOnDisplay(",
    public = i['events'][0][4]
    sites = i['events'][0][5]
    comments = i['events'][0][6]
    firstalert = i['events'][0][7]
    resolution = i['events'][0][8]
    impact = i['events'][0][9]
    cause = i['events'][0][10]
    handler = i['events'][0][11]
    print '"', public, '","', sites, '","', comments, '","', firstalert, '","', resolution, '","', impact, '","', cause, '","', handler, '") >', i['key'], '</option>'
print """</select>"""
print """<br/></div>"""

print """\
<label for="public" class="required">Public facing sites impacted?</label>
<input type="radio" name="public" value="Yes" checked="checked" /> Yes
<input type="radio" name="public" value="No" /> No<br/>
<label for="sites" class="required">Sites affected:</label> <select name="sites" multiple="multiple" size="15">
<option value="N/A" selected="selected">N/A</option>
<option value="wotif.com">wotif.com</option>
<option value="wotif.com/flights">wotif.com/flights</option>
<option value="wotif.com/packages">wotif.com/packages</option>
<option value="lastminute.com.au">lastminute.com.au</option>
<option value="travel.com.au">travel.com.au</option>
<option value="asiawebdirect.com">asiawebdirect.com</option>
<option value="latestays.com">latestays.com</option>
<option value="Asia Portals">Asia Portals</option>
<option value="Asia Matrix Display">Asia Matrix Display</option>
<option value="godo.com.au / godo.co.nz">godo.com.au / godo.co.nz</option>
<option value="Arnold CWT">Arnold CWT</option>
<option value="Arnold Tramada">Arnold Tramada</option>
<option value="Arnold UOS">Arnold UOS</option>
<option value="Arnold Wotcorp">Arnold Wotcorp</option>
</select><br/>
<label for="comments" class="required">Summary / Comments:</label> <textarea rows="5" cols="50" name="comments"></textarea><br/>
<label for="firstalert" class="required">Date &amp; Time of First Alert:</label> <input type="text" id="firstalert" name="firstalert" size="40"/><br/>
<label for="resolution">Date &amp; Time of Resolution:</label> <input type="text" name="resolution" size="40" value="TBA"/><br/>
<label for="impact">Technical Impact:</label> <textarea rows="5" cols="50" name="impact">Under investigation</textarea><br/>
<label for="cause">Cause:</label> <textarea rows="5" cols="50" name="cause">Under investigation</textarea><br/>
<label for="handler">Being Handled By:</label> <input type="text" name="handler" value="Group Infrastructure" size="40"/><br/>
<div id="postmortem" style="display:none;">
&nbsp;&nbsp;A Post Mortem is required when:<br/>
&nbsp;&nbsp;&nbsp;&nbsp;- Downtime or booking flow failing;<br/>
&nbsp;&nbsp;&nbsp;&nbsp;- Significantly reduced bookings;<br/>
&nbsp;&nbsp;&nbsp;&nbsp;- User experience or brand reputation negatively impacted;<br/>
&nbsp;&nbsp;&nbsp;&nbsp;- Revenue system offline for >1 hour or >500 offline bookings;<br/>
&nbsp;&nbsp;&nbsp;&nbsp;- Actions items required for any reason e.g. after a "close call".<br/><br/>
<label for="postmortem">Auto-create Post Mortem now?</label>
<input type="radio" name="postmortem" value="Yes" /> Yes
<input type="radio" name="postmortem" value="No" checked="checked" /> No<br/>
</div>
<label>(* == Required field)</label><br/>
<input type="submit" value="Send it!" name="submit"/>
</fieldset>
</form>
<p>Version 1.1: Auto-create Confluence Post Mortem</p>
<a href="index.html">Original Form</a>
</body>
</html>
<script type="text/javascript">
today = new Date();
year = today.getFullYear();
month = today.getMonth() + 1;
if (month <= 9)
    month = '0' + month;
date = today.getDate();
if (date <= 9)
    date = '0' + date;
hour = today.getHours();
if (hour <= 9)
    hour = '0' + hour;
minute = today.getMinutes();
if (minute <= 9)
    minute = '0' + minute;
second = today.getSeconds();
if (second <= 9)
    second = '0' + second;
tzoffset = ((new Date()).getTimezoneOffset() * -1)/60;
if (tzoffset == 10) {
tzname = 'AEST';
} else if (tzoffset == 7) {
tzname = ' Thailand Time';
} else if (tzoffset == 11 ) {
tzname = 'ADST';
} else {
if (tzoffset > 0) {
tzname = 'GMT+' + tzoffset.toString();
} else if (tzoffset < 0) {
tzname = 'GMT' + tzoffset.toString();
} else {
tzname = 'GMT';
}
}
datestring = year + '-' + month.toString() + '-' + date.toString() + ' ' + hour.toString() + ':' + minute.toString() + ':' + second.toString() + ' ' + tzname;
document.getElementById('firstalert').value = datestring;

function toggleSummary(state) {
    if  (state == 'New') {
        document.getElementById('postmortem').style.display='none';
        document.getElementById('summary_new').style.display='block';
        document.getElementById('summary_open').style.display='none';
        document.getElementById('summary_closed').style.display='none';
    } else if (state == 'Update') {
        document.getElementById('postmortem').style.display='none';
        document.getElementById('summary_new').style.display='none';
        document.getElementById('summary_open').style.display='block';
        document.getElementById('summary_closed').style.display='none';
    } else if (state == 'Resolved') {
        document.getElementById('postmortem').style.display='block';
        document.getElementById('summary_new').style.display='none';
        document.getElementById('summary_open').style.display='block';
        document.getElementById('summary_closed').style.display='none';
    }  else if (state == 'Reopen') {
        document.getElementById('postmortem').style.display='none';
        document.getElementById('summary_new').style.display='none';
        document.getElementById('summary_open').style.display='none';
        document.getElementById('summary_closed').style.display='block';
    }
}

function changeIssueOnDisplay(public, sites, comments, firstalert, resolution, impact, cause, handler) {
    document.getElementById('public').value = public;
    document.getElementById('comments').value = comments;
    document.getElementById('firstalert').value = firstalert;
    document.getElementById('resolution').value = resolution;
    document.getElementById('impact').value = impact;
    document.getElementById('cause').value = cause;
    document.getElementById('handler').value = handler;
}
</script>
"""

