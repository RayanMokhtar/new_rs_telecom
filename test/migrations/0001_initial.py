# Generated by Django 5.0.1 on 2024-06-04 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Leads',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=255)),
                ('nom_offre', models.CharField(max_length=255)),
                ('nombre_offres', models.IntegerField()),
                ('localisation_du_lead', models.CharField(max_length=255)),
                ('porteur_lead', models.CharField(max_length=255, null=True)),
                ('url_profil_porteur_lead', models.URLField(null=True)),
                ('adresse_mail_de_contact', models.EmailField(max_length=254, null=True)),
                ('telephone', models.CharField(max_length=20, null=True)),
                ('secteur_activite', models.CharField(max_length=255, null=True)),
                ('taille_entreprise', models.CharField(max_length=255, null=True)),
                ('chiffre_d_affaires', models.CharField(max_length=255, null=True)),
                ('source_lead', models.CharField(max_length=255, null=True)),
                ('statut_du_lead', models.CharField(choices=[('nouveau', 'Nouveau'), ('en_cours', 'En cours'), ('converti', 'Converti')], max_length=50, null=True)),
                ('date_publication_offre', models.DateField(null=True)),
                ('date_maj_lead', models.DateField(null=True)),
                ('remarques', models.TextField(blank=True, null=True)),
                ('priorite', models.CharField(choices=[('haute', 'Haute'), ('moyenne', 'Moyenne'), ('basse', 'Basse')], max_length=50, null=True)),
                ('description_job', models.TextField(null=True)),
                ('lien_vers_lead', models.URLField(null=True)),
            ],
            options={
                'db_table': 'leads',
            },
        ),
    ]
