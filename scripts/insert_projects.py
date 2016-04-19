#! /usr/bin/env python

import gtr
import ratelim
import sqlalchemy
import string

from datetime import datetime as dt
from db_init import Project, get_configs
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


@ratelim.greedy(10, 10)  # One call every second
def add_projects_to_list(data):
    """Loops through JSON and appends a new Project object to a list
    based on its key.
    """

    project_list = []

    for project in data:
        project_list.append(Project(
            abstract_texts=project.get('abstractText'),
            created=dt.fromtimestamp(project.get("created") / 1000),  # Java timestamp
            grant_cats=project.get('grantCategory'),
            health_categories=project.get('healthCategories'),
            href=project.get("href"),
            id=project.get('id'),
            identifiers=project.get('identifiers'),
            lead_org_dpts=project.get('leadOrganisationDepartment'),
            links=project.get("links"),
            potential_impacts=project.get('potentialImpact'),
            research_activities=project.get('researchActivities'),
            research_subjects=project.get('researchSubjects'),
            research_topics=project.get('researchTopics'),
            status=project.get('status'),
            tech_abstracts=project.get('techAbstractText'),
            titles=project.get('title')))

    session = SessionFactory()
    [session.add(project) for project in project_list]
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
    s = gtr.Projects()
    user_agent_string = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) \
                         AppleWebKit/600.3.18 (KHTML, like Gecko) \
                         Version/8.0.3 Safari/600.3.18')
    s.session.headers.update({'User-Agent': user_agent_string})

    print("Gathering projects")
    # Get the first page of results
    # using max items per page
    results = s.project("", s=100, p=1)
    total_pages = results.json()["totalPages"]    # Total number of pages to loop through
    print('Pages to read = {}'.format(total_pages))
    print('Reading page 1')
    data = results.json()["project"]               # Save the returned JSON to data
    add_projects_to_list(data)          # Add the returned data to the DB

    page = 2
    while page <= total_pages:
        print('Reading page {}'.format(page))
        results = s.project("", s=100, p=page)
        data = results.json()["project"]
        add_projects_to_list(data)
        page += 1

if __name__ == '__main__':
    main()
