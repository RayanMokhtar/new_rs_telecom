# importation des libreries
import re




def validationMail(email):
    domain_regex = r"@(.+)$"
    
    # Extraction du domaine de l'adresse e-mail
    domain = re.findall(domain_regex, email)
    
    # Liste de domaines professionnels connus (vous pouvez étendre cette liste selon vos besoins)
    professional_domains_connues = ["gmail.com", "icloud.fr", "yahoo.fr"]
    
    # Vérification si le domaine de l'adresse e-mail est dans la liste des domaines professionnels
    if domain and domain[0] in professional_domains_connues:
        return False
    else:
        return True

def validFilespdf():
    pass