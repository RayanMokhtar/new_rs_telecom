import requests
from bs4 import BeautifulSoup
import re
import csv
from linkedIn import fetch_job_listings

def get_html(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except Exception as e:
        return None

def parse_html(html):
    results = {'taille': None, 'secteur': None, 'chiffre_d_affaires': None, 'lien_site': None}
    try:
        soup = BeautifulSoup(html, 'html.parser')

        # Récupération de la taille de l'entreprise
        size_div = soup.find('div', class_='css-18pwhsj e1wnkr790', text='Taille de l\'entreprise')
        if size_div:
            next_size_div = size_div.find_next_sibling('div')
            if next_size_div:
                size_content = next_size_div.get_text(strip=True)
                results['taille'] = size_content
            else:
                print("Aucun div trouvé après le div 'Taille de l'entreprise'.")

        # Récupération du secteur
        sector_div = soup.find('div', class_='css-18pwhsj e1wnkr790', text='Secteur')
        if sector_div and sector_div.find_next_sibling('div'):
            results['secteur'] = sector_div.find_next_sibling('div').get_text(strip=True)

        # Récupération du chiffre d'affaires
        revenue_div = soup.find('div', class_='css-18pwhsj e1wnkr790', text='Chiffre d\'affaires')
        if revenue_div and revenue_div.find_next_sibling('div'):
            results['chiffre_d_affaires'] = revenue_div.find_next_sibling('div').get_text(strip=True)

        # Récupération du lien du site
        link_div = soup.find('div', class_='css-18pwhsj e1wnkr790', text='Site Web')
        if link_div:
            next_link_div = link_div.find_next_sibling('div')
            if next_link_div:
                link_tag = next_link_div.find('a')
                if link_tag:
                    results['lien_site'] = link_tag['href']
                else:
                    print("Aucun lien trouvé après le div 'Site Web'.")
            else:
                print("Aucun div trouvé après le div 'Site Web'.")

    except Exception as e:
        print(f"Erreur lors du parsing HTML: {e}")
    
    return results

def extract_p_elements(html):
    results = {'nombre_employes': None}
    try:
        soup = BeautifulSoup(html, 'html.parser')
        target_div = soup.find('div', class_="css-brv7kd eu4oa1w0")
        if target_div:
            p_elements = target_div.find_all('p')
            if len(p_elements) >= 2:
                numbers_only = re.findall(r'\d+', p_elements[1].get_text(strip=True))
                results['nombre_employes'] = ''.join(numbers_only) + ' employés'
    except Exception as e:
        pass
    return results

def create_company_url(company_name):
    base_url = "https://fr.indeed.com/cmp/"
    return base_url + company_name.replace(" ", "-")


def read_csv_data(filename):
    try:
        with open(filename, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            return list(reader)
    except FileNotFoundError:
        return []

def update_or_add_entries(existing_data, new_entries):
    updated_data = {entry['nom']: entry for entry in existing_data}
    for new_entry in new_entries:
        updated_data[new_entry['nom']] = new_entry
    return list(updated_data.values())

# def write_to_csv(data, filename='company_data.csv', delimiter=';'):
#     fieldnames = ['nom', 'nombre_offres', 'taille', 'secteur', 'chiffre_d_affaires', 'nombre_employes']
#     with open(filename, mode='w', newline='', encoding='utf-8') as file:
#         dict_writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=delimiter)
#         dict_writer.writeheader()
#         dict_writer.writerows(data)
#         print(f"Données écrites avec succès dans {filename}.")

def write_to_csv(data, filename='leade_data.csv', delimiter=';'):
    # S'assurer que les données à écrire ne sont pas vides ds ce cas de figure
    if not data:
        print("Aucune donnée à écrire dans le fichier.")
        return
    
    try:
        # Ouverture du fichier en mode ajout ('a') avec gestion d'erreur
        with open(filename, 'a', newline='', encoding='utf-8') as output_file:
            dict_writer = csv.DictWriter(output_file, fieldnames=data[0].keys(), delimiter=delimiter)
            
            # Vérification de l'existence du fichier pour écrire ou non l'en-tête
            output_file.seek(0, 2)  # Se déplace à la fin du fichier
            if output_file.tell() == 0:  # Vérifie si le fichier est vide
                dict_writer.writeheader()  # Écrit l'en-tête si le fichier est vide
            
            dict_writer.writerows(data)
            print(f"Données ajoutées avec succès dans {filename}.")
    
    except IOError as e:
        print(f"Erreur lors de l'ouverture ou de l'écriture dans le fichier {filename}: {e}")

# Main execution
keywords = "devops"
location = "Ville de Paris, Île-de-France, France"
company_counts = fetch_job_listings(keywords, location)


existing_data = read_csv_data('leade_data.csv')
print(existing_data[:3])  # Imprime les trois premières entrées pour vérifier
new_data = []
for company, count in company_counts.items():
    url = create_company_url(company)
    html_content = get_html(url)
    if html_content:
        parsed_data = parse_html(html_content)
        employee_data = extract_p_elements(html_content)
        row_data = {
            'nom': company,
            'nombre_offres': count,
            'taille': parsed_data['taille'],
            'secteur': parsed_data['secteur'],
            'chiffre_d_affaires': parsed_data['chiffre_d_affaires'],
            'lien_site': parsed_data['lien_site']  # Ajout du lien du site
        }
        new_data.append(row_data)

# Mettre à jour les données existantes avec les nouvelles entrées
updated_data = update_or_add_entries(existing_data, new_data)
write_to_csv(updated_data)
