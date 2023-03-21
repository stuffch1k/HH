import requests

API_URL = 'https://api.hh.ru/{}'
HEADER = {"User-Agent": "HHRu_Parser/1.0 (volkov03dima@gmail.com)"}

class Query():
    PR=[]
    
    def get_all_profession(self):
        it_pr= requests.get(API_URL.format('professional_roles'), headers=HEADER).json()['categories'][7]['roles'] 
        for p in it_pr:
            self.PR.append(p['id'])
        return self.PR
    
    def get_resp(self, date_from, date_to, page=0):
        params = {
            'professional_role': self.PR,
            'per_page': 100,
            'page': page,
            'date_from': date_from.strftime('%Y-%m-%dT%H:%M:%S%z'),
            'date_to': date_to.strftime('%Y-%m-%dT%H:%M:%S%z'),
        }
        return requests.get(API_URL.format('vacancies'), headers=HEADER, params=params).json()
    
    def get_post_skills(self, post_id):
        full_info = requests.get(API_URL.format('vacancies') + '/' + post_id, headers=HEADER).json()
        if 'error' in full_info or 'errors' in full_info:
            print(full_info)
            return
        return  full_info['key_skills'], full_info['professional_roles']

    
     