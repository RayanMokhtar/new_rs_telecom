from django.urls import path
from . import views


urlpatterns = [
    #path pour ajout de leads 
    path('add_company/', views.add_company, name='add_company'),
    path('check-name/', views.check_name, name='check_name'), # ajax
    path('check-offre/',views.check_offer_name,name='check_offer'),
    path('check-date',views.check_offer_date,name='check_date_publication'),
    path('submit-form/', views.submit_form, name='submit-form'), # soumission du formulaire avec futures vérifs coté serveur 

    #path pour le choix des leads 
    path('choix_leads/',views.choix_leads,name='choix_leads'),
    # visualisation des leads présents dans le fichier csv ou dans la base de données 
    path('visualisationLeads/', views.visualisation_leads, name='visualisation_leads'),
    #interface pour la maj des leads 
    path('update/',views.view_leads,name='view_leads'),
    path('test-base/', views.test_base_template, name='test_base'),
    #barre de recherche
    path('search-results/', views.search_results, name='search_results'),
    #pour le formulaire maj des laeds 
    path('update-lead/',views.update_lead_view,name='update_lead'),
    path('submit-form-update/',views.update_lead,name='submit_form_update'),

    #pour la suppression des leads ( affichage du tableau des leads + logique de suppression du lead )
    path('display-leads/', views.display_leads, name='display_leads'),
   path('delete-lead/', views.delete_lead, name='delete_lead'),
    #path pour la génération des leads 
    path('GenerateLead/', views.scrapingPage, name='scraping_lead'),
    path('start-scraping/' , views.start_scraping , name='start_scraping'),
    #récupération des données du fichier csv pour le nom des villes 
    path('update-lead/<int:id>/', views.update_lead_view, name='update_lead'),
    path('search-city/', views.search_city, name='search_city'),
    #détails de l'entreprise 
    path('company/<str:company_name>/', views.company_detail, name='company_detail'),
    # AJOUT MANUEL du descriptif de mission ainsi que d'autres détails selon la pondération de l'importance du critére de besoin
    path('search_results/', views.search_results, name='search_results'),
    path('matching-cv/', views.matching_cv_view, name='matching_cv'),
    path('process_matching/', views.process_matching, name='process_matching'),
    path('upload_cv/', views.upload_cv, name='upload_cv'),
    path('delete_cv/<str:cv_id>/', views.delete_cv, name='delete_cv'),
    path('statsleads/',views.statistiques_leads,name='statistiques_leads'),
    path('choix-du-lead/',views.template_choix_leads , name = 'choix_lead_job_matching'),
    #path à la vue qui se charge de renvoyer les mots clés changés du lead et proposition de vouloir les changer ou pas , puis procéder au processus du matching lead-CV 
    path('matching-lead-cv/<int:lead_id>/',views.changer_mots_cle_lead, name='lead_details'),
    path('process_matching_v2/', views.process_matching_v2, name='process_matching_v2'),
    
]