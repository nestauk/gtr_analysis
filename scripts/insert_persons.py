#! /usr/bin/env python

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


@ratelim.patient(20, 5)  # 4 calls per second
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
