# -*- coding:utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import os
import jinja2
from jinja2 import Template
import requests
from collections import defaultdict

def main():
    if not os.path.exists('e'):
        os.mkdir('e')
    url='https://spreadsheets.google.com/feeds/list/1rA9sAf2t_JU6PZ6ENsnnJYsPvXWKPFe14E0vPzCHQSM/od6/public/values?alt=json'
    res=requests.get(url).json()
    events=defaultdict(list)
    for e in res['feed']['entry']:
        event_id=e['gsx$id']['$t']
        events[event_id].append({'event_id':e['gsx$id']['$t'],
                                'title':e['gsx$title']['$t'],
                                'time':e['gsx$time']['$t'],
                                'place':e['gsx$place']['$t'],
                                'introduction':e['gsx$introduction']['$t'],
                                'remark':e.get('gsx$remark',{}).get('$t','')})
    for event_id in events:
        events[event_id]=list(enumerate(events[event_id]))
    template=Template(open('eventtemplate.html').read())

    for id, details in events.iteritems():
        
        a_dir='e/%s'% id
        a_fn='%s/index.html' % a_dir
        
        if not os.path.exists(a_dir):
            os.mkdir(a_dir)
        open(a_fn,'w').write(template.render(details=details))


if __name__ == '__main__':
    main();




