import requests
from bs4 import BeautifulSoup

def extract_job_links(linkedin_url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        response = requests.get(linkedin_url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            job_links = []
            job_cards = soup.find_all('div', class_='base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card job-search-card--active')
            for job_card in job_cards:
                link = job_card.find('a', class_='base-card__full-link')['href']
                job_links.append(link)
            return job_links
        else:
            print(f'Failed to retrieve LinkedIn page. Status code: {response.status_code}')
            return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []



import requests
from bs4 import BeautifulSoup

def fetch_job_listings(keywords, location, time_frame):
    # URL de base pour la recherche d'offres d'emploi sur LinkedIn
    base_url = "https://www.linkedin.com/jobs/search/"
    
    # Préparation des paramètres de recherche
    time_options = {
        'mois dernier': 'r2592000',  # 30 jours
        'semaine dernière': 'r604800',  # 7 jours
        'dernières 24h': 'r86400'  # 24 heures
    }

    params = {
        "keywords": keywords,
        "location": location,
        "f_TPR": time_options[time_frame],
        "distance": '25'
    }

    # Construction de l'URL avec les paramètres
    response = requests.get(base_url, params=params)
    api_url = response.url

    # Vérifie si la requête a réussi
    if response.status_code == 200:
        # Analyse de la réponse HTML avec BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Recherche des balises contenant les noms des entreprises
        company_tags = soup.find_all("h4", class_="base-search-card__subtitle")
        
        # Extraction des noms des entreprises
        company_names = [tag.text.strip() for tag in company_tags]
        
        # Recherche des balises contenant les noms des offres d'emploi
        job_title_tags = soup.find_all('h3', class_='base-search-card__title')
        
        # Extraction des noms des offres d'emploi
        job_names = [tag.text.strip() for tag in job_title_tags]
        
        # Vérification pour s'assurer que nous avons le même nombre de noms d'entreprises et d'offres
        if len(company_names) != len(job_names):
            print("Warning: Le nombre de noms d'entreprises ne correspond pas au nombre de noms d'offres d'emploi.")
        
        # Création d'une liste de tuples (entreprise, offre)
        company_job_pairs = list(zip(company_names, job_names))
        
        # Création d'un dictionnaire pour compter les occurrences de chaque nom d'entreprise
        company_counts = {}
        for name in company_names:
            if name in company_counts:
                company_counts[name] += 1
            else:
                company_counts[name] = 1
        
        # Retourne les paires entreprise/offre, le dictionnaire des occurrences des noms d'entreprise et l'URL LinkedIn
        return company_job_pairs, company_counts, api_url
    else:
        # Si la requête échoue, affiche le code de statut et retourne un dictionnaire vide et l'URL
        print("La requête a échoué avec le code de statut :", response.status_code)
        return [], {}, api_url



import requests
from bs4 import BeautifulSoup
import random
import time

# Liste de différents User-Agents
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
]

def get_html_special(url):
    headers = {
        'User-Agent': random.choice(user_agents),
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1'
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            print(f'Failed to retrieve {url}. Status code: {response.status_code}')
            return None
    except Exception as e:
        print(f"An error occurred while fetching {url}: {e}")
        return None
    finally:
        # Attente aléatoire pour éviter de se faire bloquer
        time.sleep(random.uniform(1, 5))


###################################################################
import re
def extract_company_name_from_url(url):
    # Rechercher la partie après "at-" et avant le premier chiffre
    match = re.search(r'at-([^-]+)-(\d+)', url)
    if match:
        company_name = match.group(1).replace('-', ' ')
        return company_name
    return None


def extract_job_description(html_content):
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        job_description_section = soup.find('section', class_='show-more-less-html')
        if job_description_section:
            job_description = job_description_section.get_text(separator="\n", strip=True)
            return job_description
        else:
            return "No job description found."
    except Exception as e:
        print(f"An error occurred while parsing job description: {e}")
        return "Error extracting job description."


# linkedin_url = "https://www.linkedin.com/jobs/search?keywords=devsecops&location=France"
# filtered_links = extract_all_links(linkedin_url)

# for link in filtered_links:
#     print(f"Processing URL: {link}")
#     html_content = get_html(link)
#     if html_content:
#         job_description = extract_job_description(html_content)
#         print(f"Job Description for {link}:\n{job_description}\n{'='*80}\n")


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import random

# Liste des user agents
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
]

# Fonction pour créer un driver avec des options aléatoires
def create_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Exécute le navigateur en mode headless (sans interface graphique)
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument(f'user-agent={random.choice(user_agents)}')
    return webdriver.Chrome(options=options)

# Initialiser le driver globalement
driver = create_driver()

def fetch_job_listings_selenium(keywords, location, time_frame):
    # URL de base pour la recherche d'offres d'emploi sur LinkedIn
    base_url = "https://www.linkedin.com/jobs/search/"

    # Préparation des paramètres de recherche
    time_options = {
        'mois dernier': 'r2592000',  # 30 jours
        'semaine dernière': 'r604800',  # 7 jours
        'dernières 24h': 'r86400'  # 24 heures
    }

    params = {
        "keywords": keywords,
        "location": location,
        "f_TPR": time_options[time_frame],
        "distance": '25'
    }

    # Construction de l'URL avec les paramètres
    search_url = f"{base_url}?keywords={params['keywords']}&location={params['location']}&f_TPR={params['f_TPR']}&distance={params['distance']}"
    driver.get(search_url)

    # Attente de quelques secondes pour que la page se charge complètement
    time.sleep(random.uniform(5, 10))

    # Analyse de la réponse HTML avec BeautifulSoup
    soup = BeautifulSoup(driver.page_source, "html.parser")
    
    # Recherche des balises contenant les informations des offres d'emploi
    job_cards = soup.find_all("div", class_="base-search-card")

    company_job_pairs = []

    for job_card in job_cards:
        job_id = job_card.get("data-entity-urn")
        job_title_tag = job_card.find("h3", class_="base-search-card__title")
        company_tag = job_card.find("h4", class_="base-search-card__subtitle")
        
        if job_id and job_title_tag and company_tag:
            job_title = job_title_tag.text.strip()
            company_name = company_tag.text.strip()
            company_job_pairs.append((company_name, job_title, job_id))
            
    
    # Création d'un dictionnaire pour compter les occurrences de chaque nom d'entreprise
    company_counts = {}
    for name, _, _ in company_job_pairs:
        if name in company_counts:
            company_counts[name] += 1
        else:
            company_counts[name] = 1
    
    return company_job_pairs, company_counts, search_url

def fetch_and_display_job_details_from_search_url(search_url):
    driver.get(search_url)
    time.sleep(random.uniform(5, 10))  # Attente pour que la page se charge complètement

    job_elements = driver.find_elements(By.CSS_SELECTOR, "ul.jobs-search__results-list li")
    job_details = []

    for index in range(len(job_elements)):
        success = False
        while not success:
            try:
                # Rechercher à nouveau les éléments pour éviter l'erreur de référence obsolète
                
                job_elements = driver.find_elements(By.CSS_SELECTOR, "ul.jobs-search__results-list li")
                job_link = job_elements[index].find_element(By.CSS_SELECTOR, "a.base-card__full-link")
                driver.execute_script("arguments[0].click();", job_link)  # Clic sur le lien 
                time.sleep(random.uniform(5, 10))  # Attente pour que la page de détails se charge*
                error_counter = 0

                soup = BeautifulSoup(driver.page_source, 'html.parser')
                recruiter_div = soup.find('div', class_='message-the-recruiter')
                recruiter_name_tag = recruiter_div.find('span', class_='sr-only') if recruiter_div else None
                recruiter_name = recruiter_name_tag.text.strip() if recruiter_name_tag else None
                recruiter_profile_link = recruiter_div.find('a', class_='message-the-recruiter__cta')['href'] if recruiter_div else None

                job_description_div = soup.find('div', class_='show-more-less-html__markup')
                job_description = job_description_div.text.strip() if job_description_div else None

                job_details.append((recruiter_name, job_description, recruiter_profile_link))
                success = True

                driver.back()
                time.sleep(random.uniform(5, 10))  # Attendre pour que la page de résultats se recharge

            except Exception as e:
                print(f"Error processing job {index + 1}: {e}")
                error_counter += 1
                if error_counter > 3:
                    print("Error limit exceeded. Stopping the process.")
                    return job_details
                time.sleep(random.uniform(5, 10))  # Attendre avant de réessayer
                continue
    
    return job_details




from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import random
from fake_useragent import UserAgent

def configure_driver():
    ua = UserAgent()
    user_agent = ua.random
    options = Options()
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    return driver

def get_linkedin_company_info(company_name, max_attempts=4):
    attempt = 0
    company_info = {}

    while attempt < max_attempts:
        attempt += 1
        try:
            driver = configure_driver()

            # Recherche Google pour trouver la page LinkedIn de l'entreprise
            search_url = f"https://www.google.com/search?q={company_name}+site:linkedin.com/company"
            driver.get(search_url)
            time.sleep(random.uniform(5, 10))  # Attendre que la page charge

            # Cliquer sur le premier résultat de recherche
            search_results = driver.find_elements(By.CSS_SELECTOR, 'div.yuRUbf a')
            if search_results:
                company_url = search_results[0].get_attribute('href')
                print(f"Company URL found: {company_url}")
                driver.get(company_url)
                time.sleep(random.uniform(5, 10))  # Attendre que la page charge

                # Essayer de cliquer sur l'onglet "À propos" (About) si nécessaire
                try:
                    about_tab = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//a[@data-control-name='page_member_main_nav_about_tab']"))
                    )
                    driver.execute_script("arguments[0].click();", about_tab)
                    time.sleep(random.uniform(5, 10))  # Attendre que la page charge
                except Exception as e:
                    print("About tab not found or not clickable:", e)

                # Scraper la page LinkedIn de l'entreprise
                soup = BeautifulSoup(driver.page_source, 'html.parser')

                # Trouver la section "À propos"
                try:
                    about_section = driver.find_element(By.XPATH, "//h2[contains(text(),'À propos')]")
                    driver.execute_script("arguments[0].scrollIntoView(true);", about_section)
                    print("About section found")
                except Exception as e:
                    print("About section not found. Exiting.")
                    driver.quit()
                    continue

                # Trouver le conteneur de contenu principal
                content_container = soup.find('div', class_='core-section-container__content break-words')
                if not content_container:
                    print("Content container not found. Exiting.")
                    driver.quit()
                    continue
                else:
                    print("Content container found")

                # Extraire et afficher les informations
                def extract_info(label, data_test_id):
                    dt_element = content_container.find('div', {'data-test-id': data_test_id})
                    if dt_element:
                        print(f"{label} element found")
                        dd_element = dt_element.find('dd')
                        if dd_element:
                            info = dd_element.get_text(strip=True)
                            print(f"{label}: {info}")
                            return info
                    print(f"{label} element not found")
                    return None

                company_info['site_web'] = extract_info('Site web', 'about-us__website')
                company_info['secteur'] = extract_info('Secteur', 'about-us__industry')
                company_info['taille'] = extract_info('Taille de l’entreprise', 'about-us__size')
                company_info['siege_social'] = extract_info('Siège social', 'about-us__headquarters')
                company_info['type'] = extract_info('Type', 'about-us__organizationType')
                company_info['fondee_en'] = extract_info('Fondée en', 'about-us__foundedOn')
                company_info['specialisations'] = extract_info('Domaines', 'about-us__specialties')

                # Vérifier si toutes les informations nécessaires ont été récupérées
                if 'site_web' in company_info and 'taille' in company_info and 'secteur' in company_info:
                    driver.quit()
                    return company_info
            else:
                print("Company URL not found.")

            driver.quit()
        except Exception as e:
            print(f"Attempt {attempt} failed: {e}")
            time.sleep(random.uniform(5, 10))  # Attendre avant de réessayer

    # Si toutes les tentatives échouent, chercher une similitude dans la base de données
    return search_in_database(company_name)

from test.models import Leads
from django.db.models import Q
def search_in_database(company_name):
    try:
        company_info = Leads.objects.filter(Q(nom__icontains=company_name)).first()
        if company_info:
            return {
                'site_web': company_info.secteur_activite,
                'secteur': company_info.secteur_activite,
                'taille': company_info.taille_entreprise,
                'siege_social': 'non mentionné',
                'type': 'non mentionné',
                'fondee_en': 'non mentionné',
                'specialisations': 'non mentionné'
            }
    except Exception as e:
        print(f"Database search failed: {e}")
    
    return {
        'site_web': 'non mentionné',
        'secteur': 'non mentionné',
        'taille': 'non mentionné',
        'siege_social': 'non mentionné',
        'type': 'non mentionné',
        'fondee_en': 'non mentionné',
        'specialisations': 'non mentionné'
    }
