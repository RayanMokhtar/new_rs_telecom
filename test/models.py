from django.db import models

class Leads(models.Model):
    nom = models.CharField(max_length=255, null=False)
    nom_offre = models.CharField(max_length=255, null=False)
    nombre_offres = models.IntegerField(null=False)
    localisation_du_lead = models.CharField(max_length=255, null=False)
    porteur_lead = models.CharField(max_length=255, null=True)
    url_profil_porteur_lead = models.URLField(null=True)
    adresse_mail_de_contact = models.EmailField(null=True)
    telephone = models.CharField(max_length=20, null=True)
    secteur_activite = models.CharField(max_length=255, null=True)
    taille_entreprise = models.CharField(max_length=255, null=True)
    chiffre_d_affaires = models.CharField(max_length=255, null=True)
    source_lead = models.CharField(max_length=255, null=True)
    statut_du_lead = models.CharField(max_length=50, choices=[('nouveau', 'Nouveau'), ('en_cours', 'En cours'), ('converti', 'Converti')], null=True)
    date_publication_offre = models.DateField(null=True)
    date_maj_lead = models.DateField(null=True)
    remarques = models.TextField(null=True, blank=True)
    priorite = models.CharField(max_length=50, choices=[('haute', 'Haute'), ('moyenne', 'Moyenne'), ('basse', 'Basse')], null=True)
    description_job = models.TextField(null=True)
    lien_vers_lead = models.URLField(null=True)

    class Meta:
        db_table = 'leads'  # Définir explicitement le nom de la table

    def __str__(self):
        return self.nom