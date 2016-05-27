
# coding: utf-8

# In[ ]:

import json
import math
import pandas as pd

from collections import Counter

# Welsh Uni IDs
unis = {
    'aberystwyth': 'E4757A6E-7326-472B-9979-B47D77A65446',
    'bangor': 'F9F1D136-12E3-4BE4-9668-0C9BC4A7C1BF',
    'cardiff_met': '8FE3A477-8A3B-4E51-AE01-4ABCE9099213',
    'cardiff': '9C10D78F-6430-4CA7-9528-B96B0762A4C6',
    'glyndwr': '845C79D4-F696-49C1-BE40-C7E9B890AE0C',
    'swansea': 'AB307619-D4FA-427E-A042-09DBEBA84669',
    'south_wales': '433B3EF1-6D06-4AE9-9ACE-3F53F971D1B4',
    'trinity': '13493226-8270-4622-954D-B861EE3241F4'
}

uni_id = [
    'E4757A6E-7326-472B-9979-B47D77A65446',
    'F9F1D136-12E3-4BE4-9668-0C9BC4A7C1BF',
    '8FE3A477-8A3B-4E51-AE01-4ABCE9099213',
    '845C79D4-F696-49C1-BE40-C7E9B890AE0C',
    'AB307619-D4FA-427E-A042-09DBEBA84669',
    '433B3EF1-6D06-4AE9-9ACE-3F53F971D1B4',
    '13493226-8270-4622-954D-B861EE3241F4',
    '9C10D78F-6430-4CA7-9528-B96B0762A4C6'
]

uni_lads = {
    'E4757A6E-7326-472B-9979-B47D77A65446': 'W06000008',
    'F9F1D136-12E3-4BE4-9668-0C9BC4A7C1BF': 'W06000002',
    '8FE3A477-8A3B-4E51-AE01-4ABCE9099213': 'W06000015',
    '845C79D4-F696-49C1-BE40-C7E9B890AE0C': 'W06000006',
    'AB307619-D4FA-427E-A042-09DBEBA84669': 'W06000011',
    '433B3EF1-6D06-4AE9-9ACE-3F53F971D1B4': 'W06000016',
    '13493226-8270-4622-954D-B861EE3241F4': 'W06000016',
    '9C10D78F-6430-4CA7-9528-B96B0762A4C6': 'W06000015'
}

with open('./project_org.json', 'r') as f:
    j = json.load(f)

topics = sorted(list(set([proj['topics'] for proj in j if not isinstance(proj['topics'], float)])))

# Filter out single organisation projects
j = [proj for proj in j if len(proj['orgs']) > 1]


# Filter out projects not involving Welsh Unis
for uni in uni_id:
    uni_projects = {uni: [proj for proj in j if (x['org_id'] == uni for x in proj['orgs'])]}

# Count LAD occurences
for proj in j:
    proj['lad_count'] = Counter(org['lad'] for org in proj['orgs'])

# Filter out projects not involving Welsh Unis
uni_projects = {}
for uni in uni_id:
    uni_projects[uni] = []
    for proj in j:
        for org in proj['orgs']:
            if org['org_id'] == uni:
                uni_projects[uni].append(proj)

lad_counts = {}
for uni in uni_id:
    uni_lad = uni_lads[uni]
    lad_counts[uni] = Counter()
    for proj in uni_projects[uni]:
        lad_counts[uni] += proj['lad_count']
    del lad_counts[uni][uni_lad]
with open('uni_collab_counts.json', 'w') as f:
    json.dump(lad_counts, f)

for topic in topics:
    lad_counts = {}
    for uni in uni_id:
        uni_lad = uni_lads[uni]
        lad_counts[uni] = Counter()
        for proj in uni_projects[uni]:
            if proj['topics'] == topic:
                lad_counts[uni] += proj['lad_count']
        del lad_counts[uni][uni_lad]
    with open('uni_{}_collab_counts.json'.format(str.lower(topic).replace(' ', '_')), 'w') as f:
        json.dump(lad_counts, f)
