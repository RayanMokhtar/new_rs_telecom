import requests
import os

# Récupérer la valeur de la variable d'environnement PATH
path = os.environ.get('PATH')

# Afficher la valeur de PATH
print(path)

# api_key = 'mBn0CD251-gpu1PNU9xzLw'
# headers = {'Authorization': 'Bearer ' + api_key}
# api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin/company/job'
# params = {
#     'job_type': 'anything',
#     'experience_level': 'anything', 
#     'when': 'anytime',
#     'flexibility': 'remote',
#     'geo_id': '106383538', # geo id de la ville paris + mobilité en idf 
#     'keyword': 'Ingénieur DevOps',
   
# }

# response = requests.get(api_endpoint, params=params, headers=headers)

# mission=response.json()
# if response.status_code == 200:
#     print("log 1 La requête a réussi.")
#     print("Code de réponse et du lead :", response.status_code)
#     print("Contenu de la réponse :", response.json())
# elif response.status_code == 404:
#     print("La requête a échoué et dans ce cas aucune ressource n'a été trouvée.")
#     print("Code de réponse:", response.status_code)
# else:
#     print("La requête a échoué avec le code de statut :", response.status_code)

# '''partie récupération des données de l'entreprise '''

# api_key2 = 'mBn0CD251-gpu1PNU9xzLw'
# headers2 = {'Authorization': 'Bearer ' + api_key2}
# api_endpoint2 = 'https://nubela.co/proxycurl/api/linkedin/company'

# # Récupération de l'URL de l'entreprise à partir de la réponse précédente
# company_urls = []

# # Parcourir tous les emplois
# for job in mission['job']:
#     # Ajouter l'URL de l'entreprise à la liste
#     company_urls.append(job['company_url'])
#     print(job['company_url'])


# for i in company_urls:
#     params2 = {
#     'url': str(i),
#     'use_cache': 'if-present',
#   }

#     response2 = requests.get(api_endpoint2,
#                         params=params2,
#                         headers=headers2)

#     if response2.status_code == 200:    
#         print("\n \n ****** infos de l'entreprise ***** \n La requête a réussi.")
#         print("Code de réponse:", response2.status_code)
#         print("Contenu de la réponse :", response2.json())
#     else:
#         print("La requête a échoué avec le code de statut :", response2.status_code)

