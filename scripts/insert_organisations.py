#! /usr/bin/env python

# -*- coding: utf-8 -*-

# Copyright (c) 2016 Nesta

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import gtr
import sqlalchemy

from datetime import datetime as dt
from db_init import Organisation, get_configs
from os import remove
from random import randint
from sqlalchemy.orm import sessionmaker
from time import sleep

# Read in user configs
conf = get_configs()

# Assign to local variables
user = conf['user']
host = conf['host']
port = conf['port']
passw = conf['passw']
schema = conf['schema']
database = conf['database']


def add_orgs_to_list(data):
    """Loops through JSON and appends a new Organisation object to a list
    based on its key.
    """

    orgs_list = []

    for org in data:
        orgs_list.append(Organisation(
            addresses=org.get('addresses'),
            created=dt.fromtimestamp(org.get('created') / 1000),
            href=org.get('href'),
            id=org.get('id'),
            links=org.get('links'),
            name=org.get('name')))

    session = SessionFactory()
    [session.add(org) for org in orgs_list]
    session.commit()

connection_string = 'postgresql://{}:{}@{}:{}/{}'.format(user,
                                                         passw,
                                                         host,
                                                         port,
                                                         database)

db = sqlalchemy.create_engine(connection_string)
engine = db.connect()
meta = sqlalchemy.MetaData(engine, schema="gtr")
SessionFactory = sessionmaker(engine)


def main():
    s = gtr.Organisations()
    user_agent_string = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) \
                         AppleWebKit/600.3.18 (KHTML, like Gecko) \
                         Version/8.0.3 Safari/600.3.18')
    s.session.headers.update({'User-Agent': user_agent_string})

    print("Gathering organisations")

    # Save current apge number to temp file
    with open('temp', 'w') as f:
        f.write('1')

    # Get the first page of results
    # using max items per page
    page = 1
    results = s.orgs("", s=100, p=page)
    total_pages = results.json()["totalPages"]    # Total number of pages to loop through
    print('Pages to read = {}'.format(total_pages))
    print('Reading page {}'.format(page))
    data = results.json()["organisation"]               # Save the returned JSON to data
    add_orgs_to_list(data)                         # Add the returned data to the DB

    page += 1
    while page <= total_pages:
        with open('temp', 'w') as f:
            f.write(str(page))
        print('Reading page {}'.format(page))
        results = s.orgs("", s=100, p=page)
        data = results.json()["organisation"]
        add_orgs_to_list(data)
        sleep(randint(1, 7))
        page += 1

    remove('temp')

if __name__ == '__main__':
    main()
