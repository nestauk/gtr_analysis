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
import ratelim
import sqlalchemy
import string

from datetime import datetime as dt
from db_init import Person, get_configs
from sqlalchemy.orm import sessionmaker

# Read in user configs
conf = get_configs()

# Assign to local variables
user = conf['user']
host = conf['host']
port = conf['port']
passw = conf['passw']
schema = conf['schema']
database = conf['database']


@ratelim.patient(10, 10)  # One call every second
def add_persons_to_list(data):
    """Loops through JSON and appends a new Person object to a list
    based on their key.
    """

    user_list = []
    for person in data:
        user_list.append(Person(created=dt.fromtimestamp(
            person["created"] / 1000),  # Java timestamp
            first_name=string.capwords(person["firstName"]),
            href=person["href"],
            id=person['id'],
            links=person["links"],
            surname=string.capwords(person["surname"])))

    session = SessionFactory()
    [session.add(person) for person in user_list]
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
    s = gtr.Persons()
    user_agent_string = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) \
                         AppleWebKit/600.3.18 (KHTML, like Gecko) \
                         Version/8.0.3 Safari/600.3.18')
    s.session.headers.update({'User-Agent': user_agent_string})

    print("Gathering persons")
    # Get the first page of results
    # using max items per page
    results = s.persons("", s=100, p=1)
    total_pages = results.json()["totalPages"]    # Total number of pages to loop through
    print('Pages to read = {}'.format(total_pages))
    print('Reading page 1')
    data = results.json()["person"]               # Save the returned JSON to data
    add_persons_to_list(data)          # Add the returned data to the DB

    page = 2
    while page <= total_pages:
        print('Reading page {}'.format(page))
        results = s.persons("", s=100, p=page)
        data = results.json()["person"]
        add_persons_to_list(data)
        page += 1

if __name__ == '__main__':
    main()
