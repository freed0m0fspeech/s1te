import os

import requests
from bs4 import BeautifulSoup


def update_cached_data(mongoDataBase):
    query = {'_id': 0, 'testimonials': 1, 'skills': 1, 'social': 1}
    site_document = mongoDataBase.get_document(database_name='site', collection_name='portfolio',
                                               query=query)
    skills_count = 0
    for skill in site_document.get('skills', {}).values():
        skills_count += len(skill)

    site_document['skills_count'] = skills_count

    if not os.getenv('DEBUG', '0').lower() in ['true', 't', '1']:
        try:
            projects = []
            gusernames = ('pr0stre1', 'freed0m0fspeech')
            # gprojects = {}

            for gusername in gusernames:
                response = requests.get(f'https://api.github.com/users/{gusername}/repos')
                data = response.json()

                # gprojects[gusername] = {}

                for repository in data:
                    rname = repository.get('name', '')

                    if rname == '.github' or rname == f'{gusername}':
                        continue

                    # rhtml_url = repository.get('html_url', '')
                    # oravatar_url = repository.get('owner', {}).get('avatar_url', '')
                    # rdescription = repository.get('description', '')

                    # gprojects[gusername][rname] = repository
                    response = requests.get(repository.get('html_url', ''))
                    soup = BeautifulSoup(response.content, 'lxml')
                    rimage = soup.find("meta", property="og:image")['content']

                    projects.append((repository, rimage))

            projects.sort(reverse=True, key=lambda x: x[0].get('pushed_at', ''))
            site_document['projects'] = projects[:10]
            site_document['projects_count'] = len(projects)

        except Exception as e:
            print(e)

    return site_document
