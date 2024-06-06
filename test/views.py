from django.shortcuts import render

# Create your views here.
import csv
from django.shortcuts import render
from .forms import CompanyForm
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import csv, re
from django.http import HttpResponse , HttpResponseRedirect



def check_name(request):
    nom = request.GET.get('nom', '')
    exists = Leads.objects.filter(nom__iexact=nom).exists()
    return JsonResponse({'exists': exists})

def check_offer_name(request):
    nom_offre = request.GET.get('nom_offre', '')
    exists = Leads.objects.filter(nom_offre__iexact=nom_offre).exists()
    return JsonResponse({'exists': exists})


def check_offer_date(request):
    date_publication_offre = request.GET.get('date_publication_offre', '')
    date = parse_date(date_publication_offre)
    exists = Leads.objects.filter(date_publication_offre=date).exists()
    return JsonResponse({'exists': exists})

##########################################################################
def add_company(request):
    return render(request, 'test/add_company.html')

#####################################################

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
import csv
from django.utils.dateparse import parse_date

@require_http_methods(["POST"])  
@csrf_protect  
def submit_form(request):
    if request.method == 'POST':
        data = request.POST

        # Extraire les données du formulaire
        nom = data.get('nom')
        nom_offre = data.get('nom_offre')
        date_publication_offre = parse_date(data.get('date_publication_offre'))

        # Utiliser update_or_create pour créer ou mettre à jour le lead
        lead, created = Leads.objects.update_or_create(
            nom=nom,
            nom_offre=nom_offre,
            date_publication_offre=date_publication_offre,
            defaults={
                'nombre_offres': data.get('nombre_offres',1),
                'localisation_du_lead': data.get('localisation',None),
                'porteur_lead': data.get('porteur_lead'),
                'url_profil_porteur_lead': data.get('url_profil_porteur_lead',None),
                'adresse_mail_de_contact': data.get('email',None),
                'telephone': data.get('telephone',None),
                'secteur_activite': data.get('secteur',None),
                'taille_entreprise': data.get('taille',None),
                'chiffre_d_affaires': data.get('chiffre_d_affaires',None),
                'source_lead': data.get('source_lead',None),
                'statut_du_lead': data.get('statut_du_lead',None ),
                'date_maj_lead': parse_date(data.get('date_maj_lead',None)),
                'remarques': data.get('remarques',None),
                'priorite': data.get('priorite',None),
                'description_job': data.get('description_job',None),
                'lien_vers_lead': data.get('lien_vers_lead',None)
            }
        )

        return JsonResponse({'success': True, 'created': created})
    return JsonResponse({'success': False}, status=400)

############################################################################""

def choix_leads(request):
    return render(request,"test/choix_leads.html")
###########################################################################""
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64

import pandas as pd
import matplotlib.pyplot as plt
import mpld3
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect

from .models import Leads
from django.db.models.functions import TruncMonth
from django.db.models import Sum, Count
import matplotlib.pyplot as plt


import urllib, base64

def visualisation_leads(request):
    entreprises = Leads.objects.values_list('nom', flat=True).distinct()
    entreprise_selectionnee = request.GET.get('entreprise')
    search_query = request.GET.get('search', '')
    page = request.GET.get('page', 1)

    leads = Leads.objects.all()
    
    if entreprise_selectionnee:
        leads = leads.filter(nom=entreprise_selectionnee)
    
    if search_query:
        leads = leads.filter(
            nom__icontains=search_query
        ) | leads.filter(
            nom_offre__icontains=search_query
        ) | leads.filter(
            localisation_du_lead__icontains=search_query
        )

    paginator = Paginator(leads, 10)  # 10 leads par page
    leads_page = paginator.get_page(page)

    context = {
        'entreprises': entreprises,
        'entreprise_selectionnee': entreprise_selectionnee,
        'leads': leads_page,
        'search_query': search_query,
    }
    return render(request, 'test/visualisationLeads.html', context)

import plotly.express as px
import plotly.graph_objects as go
from django.shortcuts import render
from django.http import JsonResponse

from django.db.models.functions import TruncMonth

def statistiques_leads(request):
    entreprise_selectionnee = request.GET.get('entreprise')
    offres = []
    charts = []

    if entreprise_selectionnee:
        offres = Leads.objects.filter(nom=entreprise_selectionnee).values('localisation_du_lead').annotate(total_offres=Sum('nombre_offres'))

        # 1. Camembert des offres par localisation
        locations = [offre['localisation_du_lead'] for offre in offres]
        counts = [offre['total_offres'] for offre in offres]
        fig = px.pie(values=counts, names=locations, title='Offres par localisation')
        charts.append(fig.to_html(full_html=False))

        # 2. Bar chart des offres par localisation
        fig = px.bar(x=locations, y=counts, labels={'x': 'Localisation', 'y': 'Nombre d\'offres'}, title='Nombre d\'offres par localisation')
        charts.append(fig.to_html(full_html=False))

    # 3. Bar chart des offres par entreprise (général)
    entreprises_offres = Leads.objects.values('nom').annotate(total_offres=Sum('nombre_offres')).order_by('-total_offres')
    entreprises = [offre['nom'] for offre in entreprises_offres]
    counts = [offre['total_offres'] for offre in entreprises_offres]
    fig = px.bar(x=entreprises, y=counts, labels={'x': 'Entreprise', 'y': 'Nombre d\'offres'}, title='Nombre d\'offres par entreprise')
    charts.append(fig.to_html(full_html=False))

    # 4. Pie chart des leads par statut (général)
    statuts_leads = Leads.objects.values('statut_du_lead').annotate(total_leads=Count('id'))
    statuts = [statut['statut_du_lead'] for statut in statuts_leads]
    counts = [statut['total_leads'] for statut in statuts_leads]
    fig = px.pie(values=counts, names=statuts, title='Répartition des leads par statut')
    charts.append(fig.to_html(full_html=False))

    # 5. Bar chart des priorités de leads (général)
    priorites_leads = Leads.objects.values('priorite').annotate(total_leads=Count('id'))
    priorites = [priorite['priorite'] for priorite in priorites_leads]
    counts = [priorite['total_leads'] for priorite in priorites_leads]
    fig = px.bar(x=priorites, y=counts, labels={'x': 'Priorité', 'y': 'Nombre de leads'}, title='Répartition des leads par priorité')
    charts.append(fig.to_html(full_html=False))

    # 6. Bar chart des leads par secteur d'activité
    secteurs_leads = Leads.objects.values('secteur_activite').annotate(total_leads=Count('id')).order_by('-total_leads')
    secteurs = [secteur['secteur_activite'] for secteur in secteurs_leads]
    counts = [secteur['total_leads'] for secteur in secteurs_leads]
    fig = px.bar(x=secteurs, y=counts, labels={'x': 'Secteur d\'activité', 'y': 'Nombre de leads'}, title='Nombre de leads par secteur d\'activité')
    charts.append(fig.to_html(full_html=False))

    # 7. Bar chart des leads par taille d'entreprise
    tailles_leads = Leads.objects.values('taille_entreprise').annotate(total_leads=Count('id')).order_by('-total_leads')
    tailles = [taille['taille_entreprise'] for taille in tailles_leads]
    counts = [taille['total_leads'] for taille in tailles_leads]
    fig = px.bar(x=tailles, y=counts, labels={'x': 'Taille d\'entreprise', 'y': 'Nombre de leads'}, title='Nombre de leads par taille d\'entreprise')
    charts.append(fig.to_html(full_html=False))

    # 8. Pie chart des leads par source
    sources_leads = Leads.objects.values('source_lead').annotate(total_leads=Count('id')).order_by('-total_leads')
    sources = [source['source_lead'] for source in sources_leads]
    counts = [source['total_leads'] for source in sources_leads]
    fig = px.pie(values=counts, names=sources, title='Répartition des leads par source')
    charts.append(fig.to_html(full_html=False))

    # # 9. Line chart des leads par mois
    # leads_par_mois = Leads.objects.annotate(month=TruncMonth('date_publication_offre')).values('month').annotate(total_leads=Count('id')).order_by('month')
    # months = [lead['month'].strftime('%Y-%m') for lead in leads_par_mois if lead['month'] is not None]
    # counts = [lead['total_leads'] for lead in leads_par_mois if lead['month'] is not None]
    # fig = px.line(x=months, y=counts, labels={'x': 'Mois', 'y': 'Nombre de leads'}, title='Nombre de leads par mois')
    # charts.append(fig.to_html(full_html=False))

    context = {
        'entreprise_selectionnee': entreprise_selectionnee,
        'offres': offres,
        'charts': charts,
    }
    return render(request, 'test/statistiquesLeads.html', context)

def get_graph(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    return uri
##################################################################
# Mise à jour du lead 




def test_base_template(request):
    return render(request, 'test/base.html')

##########################################





###################################################
from django.http import Http404
from .forms import LeadsForm
from django.shortcuts import render, get_object_or_404, redirect
@csrf_protect
def update_lead_view(request, id):
    lead = get_object_or_404(Leads, id=id)
    if request.method == 'POST':
        form = LeadsForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            return redirect('view_leads')
    else:
        form = LeadsForm(instance=lead)
    return render(request, 'test/update_lead.html', {'form': form, 'lead': lead})

def view_leads(request):
    leads = Leads.objects.all()
    updated_id = request.GET.get('updated_id')
    return render(request, 'test/leads.html', {'leads': leads, 'updated_id': updated_id})
#####################################


@require_http_methods(["POST"])
@csrf_protect
def update_lead(request):
    # Récupération des données depuis le formulaire
    nom_offre = request.POST.get('nom_offre')
    localisation = request.POST.get('localisation')
    nom = request.POST.get('nom')
    nombre_offres = request.POST.get('nombre_offres')
    email = request.POST.get('email')
    telephone = request.POST.get('telephone')
    taille = request.POST.get('taille')
    secteur = request.POST.get('secteur')
    chiffre_d_affaires = request.POST.get('chiffre_d_affaires')
    lien_site = request.POST.get('lien_site')

    path_to_csv = 'leap_data.csv'
    
    # Chargement du CSV dans un DataFrame
    df = pd.read_csv(path_to_csv, delimiter=';')
    
    # Création d'un masque pour identifier la ligne à mettre à jour
    mask = (df['nom_offre'] == nom_offre) & (df['nom_entreprise'] == nom)
    
    # Vérification si au moins une ligne correspond aux critères
    if mask.any():
        # Mise à jour des données du lead
        df.loc[mask, 'localisation'] = localisation
        df.loc[mask, 'nombre_offres'] = nombre_offres
        df.loc[mask, 'email'] = email
        df.loc[mask, 'telephone'] = telephone
        df.loc[mask, 'taille'] = taille
        df.loc[mask, 'secteur'] = secteur
        df.loc[mask, 'chiffre_d_affaires'] = chiffre_d_affaires
        df.loc[mask, 'lien_site'] = lien_site
        
        # Sauvegarde du DataFrame modifié dans le fichier CSV
        df.to_csv(path_to_csv, index=False, sep=';')
        return JsonResponse({"success": True, "message": "Lead mis à jour avec succès."})
    else:
        return JsonResponse({"success": False, "message": "Lead non trouvé pour mise à jour."})

############################################"
def display_leads(request):
    leads = Leads.objects.all()
    return render(request, 'test/display_leads.html', {'leads': leads})
###############################################"

def delete_lead(request):
    if request.method == 'POST':
        lead_id = request.POST.get('id')
        try:
            lead = Leads.objects.get(id=lead_id)
            lead.delete()
            return JsonResponse({'success': True})
        except Leads.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Lead not found'})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})

#################################################################################################################

'''cette partie de code est dédiée à la génération de lead , notamment utilisation du multi-threading  , et le script présent dans le dossier script , que fait du scraping de plusieurs sources 
'''

from django.http import JsonResponse
from threading import Thread
from .scripts.extract_companies import read_csv_data,main_extraction
import json

@require_http_methods(["POST"])
def start_scraping(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        nom = data.get('nom')
        region = data.get('region')
        keywords = data.get('keywords')
        time_frame = data.get('time_frame')

        if not nom or not region or not keywords or not time_frame:
            return JsonResponse({'status': 'error', 'message': 'Tous les champs sont obligatoires.'}, status=400)

        location = f"{nom}, {region}, France"
        print(f"Nom: {nom}, Région: {region}, Localisation: {location}, Keywords: {keywords}, Time Frame: {time_frame}")

        lien, new_data = main_extraction(keywords, location, time_frame)

        # Log the data to verify the structure
        for row in new_data:
            print("Row data:", row)

        return JsonResponse({'status': 'success', 'data': new_data, 'lien': lien}, safe=False)
    except Exception as e:
        print(f"Error in start_scraping: {e}")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
@require_http_methods(["GET"])
def company_detail(request, company_name):
    data = read_csv_data('donnees_lead.csv')
    company_data = next((item for item in data if item["nom"] == company_name), None)

    if company_data:
        print(f"Company Data: {company_data}")  # Ajouté pour vérifier les données en console
        return render(request, 'test/company_detail.html', {'company': company_data})
    else:
        return JsonResponse({'status': 'error', 'message': 'Company not found.'}, status=404)
#######################################################################################################
@require_http_methods(["GET"])
def search_city(request):
    query = request.GET.get('q', '').lower()
    try:
        df = pd.read_csv('nom_communes.csv', delimiter=';')
        df['Nom (minuscules)'] = df['Nom (minuscules)'].str.lower()
        
        # Filtrer les villes dont le nom contient la query
        filtered_df = df[df['Nom (minuscules)'].str.contains(query)]
        response_data = filtered_df[['Nom (minuscules)', 'Région']].drop_duplicates().to_dict(orient='records')
        
        return JsonResponse(response_data, safe=False)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    ###################################################################

def scrapingPage(request):
    return render(request,'test/scraping.html')
######################################################################



# @require_http_methods(["GET"])
# def search_results(request):
#     query = request.GET.get('query', '').lower()
#     search_type = request.GET.get('type', 'offre')
#     path_to_csv = 'donnees_lead.csv'
#     results = []
#     with open(path_to_csv, newline='', encoding='utf-8') as csv_file:
#         reader = csv.reader(csv_file, delimiter=";")
#         next(reader, None)  # Ignorer la première ligne du header
#         for row in reader:
#             if search_type == 'entreprise' and query in row[2].lower():
#                 results.append(row)
#             elif search_type == 'offre' and query in row[0].lower():
#                 results.append(row)

#     # Tri des résultats
#     results.sort(key=lambda x: x[0] if search_type == 'offre' else x[2])
#     return JsonResponse(results, safe=False)


###########################################################################
def matching_cv_view(request):
    return render(request, 'test/matching_cv.html')

########################################################################
''' cette partie est dédié au processus de matching de cv avec le descriptif de mission 
la vue prend des cvs récupérés par le javascript ( les cvs rentrés seront mis dans une liste , js , 
le but est de les récupérer , créer les index , puis effectuer le traitement du texte , le parsing des
cvs puis le traitement des cvs et faire le matching par  la suite à l'aide de l'instance crée par 
elastic search , qui parcout dans ces index de cvs , pour trouver le cv le plus adéquat avec un système de scoring mis en place
avec la formule TF*IDF*lengthString '''


from .scripts.traitement_text import *
es = Elasticsearch("http://localhost:9200", timeout=60)
def print_index_content(index_name):
    try:
        es = Elasticsearch("http://localhost:9200", timeout=60) 
        response = es.search(index=index_name, body={"query": {"match_all": {}}})
        
        hits = response['hits']['hits']
        print(f"Index content for '{index_name}':")
        for hit in hits:
            print(f"ID: {hit['_id']}")
            print(f"Source: {hit['_source']}")
            print("------------")
    
    except Exception as e:
        print(f"Error: {e}")


from elasticsearch import Elasticsearch, NotFoundError, RequestError
import time


def determine_remark(percentage):
    if percentage >= 80:
        return "Ce CV correspond très bien à ce besoin"
    elif percentage >= 60:
        return "Ce CV correspond bien à ce besoin malgré quelques notions manquantes"
    elif percentage >= 40:
        return "Ce CV pourrait correspondre à un besoin similaire avec moins de contraintes"
    elif percentage >= 20:
        return "Ce CV correpond moins à ce besoin par rapport à d'autres"
    else:
        return "Ce CV ne correspond pas à ce besoin ."

@require_http_methods(["POST"])
def process_matching(request):
    try:
        mission_text = request.POST.get('mission_text')
        langue_text = request.POST.get('langue_text')
        entreprises_text = request.POST.get('entreprises_text')
        competences_text = request.POST.get('competences_text')
        poids_mission = int(request.POST.get('poids_mission'))
        poids_langue = int(request.POST.get('poids_langue'))
        poids_entreprises = int(request.POST.get('poids_entreprises'))
        poids_competences = int(request.POST.get('poids_competences'))
        cv_files = request.FILES.getlist('cv_files')

        if not any([mission_text, langue_text, entreprises_text, competences_text]):
            return JsonResponse({"error": "Veuillez remplir au moins un champ de recherche."}, status=400)

        if not cv_files:
            return JsonResponse({"error": "Veuillez uploader au moins un fichier de CV."}, status=400)

        try:
            es.delete_by_query(index='cvs', body={"query": {"match_all": {}}})
        except NotFoundError:
            pass

        try:
            es.indices.create(index='cvs')
        except RequestError as e:
            if e.error == 'resource_already_exists_exception':
                pass
            else:
                raise

        cv_texts = []
        for file in cv_files:
            cv_text = extract_text_from_pdf(file)
            preprocessed_cv_text = preprocess_text_mission(cv_text)
            cv_texts.append((file.name, preprocessed_cv_text))

        for cv_filename, cv_text in cv_texts:
            index_document("cvs", cv_filename, {"filename": cv_filename, "content": cv_text})

        max_attempts = 50
        attempt = 0
        results = []

        while attempt < max_attempts and not results:
            # Rechercher les correspondances
            matching_results = search_matching_cvs(
                mission_text, langue_text, entreprises_text, competences_text,
                poids_mission, poids_langue, poids_entreprises, poids_competences
            )
            results = [{"filename": result['_source']['filename'], "score": result['_score'], "content": result['_source']['content']} for result in matching_results]
            if not results:
                time.sleep(1)
                attempt += 1

        if not results:
            return JsonResponse({"error": "Aucune correspondance trouvée après plusieurs tentatives."}, status=404)

        score_max = max(result['score'] for result in results)
        for result in results:
            result['percentage'] = (result['score'] / score_max) * 100
            result['remark'] = determine_remark(result['percentage'])
            
            # Calculate keyword occurrences
            keyword_occurrences = calculate_keyword_occurrences(result['content'], mission_text, langue_text, entreprises_text, competences_text)
            result['keyword_occurrences'] = keyword_occurrences

        results = sorted(results, key=lambda x: x['score'], reverse=True)

        return JsonResponse({"results": results})
    
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def calculate_keyword_occurrences(cv_content, mission_text, langue_text, entreprises_text, competences_text):
    keywords = (mission_text + ' ' + langue_text + ' ' + entreprises_text + ' ' + competences_text).split()
    keyword_occurrences = {keyword: cv_content.lower().count(keyword.lower()) for keyword in keywords}
    return keyword_occurrences

def calculate_keyword_occurrences_v2(cv_content, mission_text, keywords_text):
    keywords = (' ' + keywords_text).split()
    keyword_occurrences = {keyword: cv_content.lower().count(keyword.lower()) for keyword in keywords}
    return keyword_occurrences
   
def upload_cv(request):
    if request.method == 'POST':
        try:
            file = request.FILES.get('cv_file')
            if not file:
                return JsonResponse({"error": "No file provided"}, status=400)

            # Extraire le texte du PDF et ajouter à l'index Elasticsearch
            cv_text = extract_text_from_pdf(file)
            preprocessed_cv_text = preprocess_text_cv(cv_text)

            es = Elasticsearch()
            doc = {
                'filename': file.name,
                'content': preprocessed_cv_text,
            }
            res = es.index(index='cvs', document=doc)
            
            return JsonResponse({"file_id": res['_id']})
        
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method."}, status=400)

def delete_cv(request, cv_id):
    if request.method == 'DELETE':
        try:
            # Vérifier si le document existe
            res = es.get(index='cvs', id=cv_id, ignore=[404])
            if not res['found']:
                return JsonResponse({"error": "Document not found"}, status=404)
            
            # Supprimer le document de l'index Elasticsearch
            es.delete(index='cvs', id=cv_id)
            
            return JsonResponse({"message": "Document deleted successfully"})
        
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({"error": str(e)}, status=500)
    
    return JsonResponse({"error": "Invalid request method."}, status=400)
    
from django.core.paginator import Paginator
from .models import Leads

def search_results(request):
    query = request.GET.get('query', '')
    search_type = request.GET.get('type', 'offre')
    
    if search_type == 'offre':
        leads = Leads.objects.filter(nom_offre__icontains=query)
    else:
        leads = Leads.objects.filter(nom__icontains=query)
    
    paginator = Paginator(leads, 20)  # 20 leads per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    leads_data = list(page_obj.object_list.values('id', 'nom_offre', 'nom', 'nombre_offres', 'localisation_du_lead'))
    return JsonResponse({
        'leads': leads_data,
        'num_pages': paginator.num_pages,
        'current_page': page_obj.number,
    })


#############################################################################"

def changer_mots_cle_lead(request, lead_id):
    lead = get_object_or_404(Leads, pk=lead_id)
    processed_description = preprocess_text_mission(lead.description_job)
    full_description = f"{lead.nom_offre} {processed_description}"
    keywords = extract_keywords(full_description)
    print('La description est :', full_description)
    print(f'Les mots clés retournés sont : {keywords}')
    return render(request, 'test/changer_mots_cle_lead.html', {'lead': lead, 'keywords': keywords})

from django.db.models import Q

def template_choix_leads(request):
    entreprises = Leads.objects.values_list('nom', flat=True).distinct()
    entreprise_selectionnee = request.GET.get('entreprise', '')
    search_query = request.GET.get('search', '')
    page = request.GET.get('page', 1)

    leads = Leads.objects.all()
    
    if entreprise_selectionnee:
        leads = leads.filter(nom=entreprise_selectionnee)
    
    if search_query:
        leads = leads.filter(
            Q(nom__icontains=search_query) |
            Q(nom_offre__icontains=search_query) |
            Q(localisation_du_lead__icontains=search_query)
        )

    paginator = Paginator(leads, 10)  # 10 leads per page
    leads_page = paginator.get_page(page)

    context = {
        'entreprises': entreprises,
        'entreprise_selectionnee': entreprise_selectionnee,
        'leads': leads_page,
        'search_query': search_query,
    }
    return render(request, 'test/choix_job_matching.html', context)
##################################################""
#matching process v2 

@require_http_methods(["POST"])
def process_matching_v2(request):
    try:
        mission_text = request.POST.get('mission_text')
        keywords_text = request.POST.get('keywords_text')
        poids_lead = int(request.POST.get('poids_lead'))
        poids_keywords = int(request.POST.get('poids_keywords'))
        cv_files = request.FILES.getlist('cv_files')

        if not mission_text and not keywords_text:
            return JsonResponse({"error": "Veuillez remplir au moins un champ de recherche."}, status=400)

        if not cv_files:
            return JsonResponse({"error": "Veuillez uploader au moins un fichier de CV."}, status=400)

        try:
            es.delete_by_query(index='cvs', body={"query": {"match_all": {}}})
        except NotFoundError:
            pass

        try:
            es.indices.create(index='cvs')
        except RequestError as e:
            if e.error == 'resource_already_exists_exception':
                pass
            else:
                raise

        cv_texts = []
        for file in cv_files:
            cv_text = extract_text_from_pdf(file)
            preprocessed_cv_text = preprocess_text_mission(cv_text)
            cv_texts.append((file.name, preprocessed_cv_text))

        for cv_filename, cv_text in cv_texts:
            index_document("cvs", cv_filename, {"filename": cv_filename, "content": cv_text})

        max_attempts = 50
        attempt = 0
        results = []

        while attempt < max_attempts and not results:
            matching_results = search_matching_cvs_v2(
                mission_text, keywords_text,
                poids_lead, poids_keywords
            )
            results = [{"filename": result['_source']['filename'], "score": result['_score'], "content": result['_source']['content']} for result in matching_results]
            if not results:
                time.sleep(1)
                attempt += 1

        if not results:
            return JsonResponse({"error": "Aucune correspondance trouvée après plusieurs tentatives."}, status=404)

        score_max = max(result['score'] for result in results)
        for result in results:
            result['percentage'] = (result['score'] / score_max) * 100
            result['remark'] = determine_remark(result['percentage'])
            keyword_occurrences = calculate_keyword_occurrences_v2(result['content'], mission_text, keywords_text)
            result['keyword_occurrences'] = keyword_occurrences

        results = sorted(results, key=lambda x: x['score'], reverse=True)

        return JsonResponse({"results": results})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
    ##########################################################################