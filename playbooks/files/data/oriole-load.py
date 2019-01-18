#!/usr/bin/env python3

import xml.etree.ElementTree as ET
import requests
import json
import uuid

headers={'x-okapi-tenant': 'diku', 'content-type': 'application/json'}
payload = {'username': 'diku_admin', 'password': 'admin'}
response = requests.post('http://localhost:9130/authn/login', data=json.dumps(payload), headers=headers)
token = response.headers['x-okapi-token']

api_url = 'http://localhost:9130/oriole-resources'
headers['x-okapi-token'] = token

# Parse XML
tree = ET.parse('data.xml')
root = tree.getroot()

for child in root:
    id = str(uuid.uuid4())
    jhu_id_elem = child.find('metalib_id')
    jhu_id = jhu_id_elem.text if jhu_id_elem is not None else ''

    title_elem = child.find('title_full')
    if title_elem is None:
        title_elem = child.find('title_display')
    title = title_elem.text if title_elem is not None else ''

    url_elem = child.find('link_native_home')
    url = url_elem.text if url_elem is not None else ''

    description_elem = child.find('description')
    description = description_elem.text if description_elem is not None else ''

    payload = {'id': id, 'title': title, 'url': url, 'description': description}
    #print(payload)
    response = requests.post(api_url, headers=headers, data=json.dumps(payload))
