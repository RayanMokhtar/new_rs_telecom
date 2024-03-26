from django.conf import settings
from datetime import datetime
import uuid
from django.shortcuts import render
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
import xmlrpc.client as xmlrpclib
import os
from django.core.files.storage import FileSystemStorage
from .utils import validationMail
from .models import Postuler
from pulls.tasks import send_email_message

def home(request):
    return render(request, 'libs/home.html',{'head': True}) 

def about(request):
    return render(request, 'libs/about.html',{'active_page': 'about'})

def service(request):
    return render(request, 'libs/services.html',{'active_page': 'service'})

def expertise(request):
    return render(request, 'libs/experiences.html',{'active_page': 'expertise'})

def detailSecteur(request,detail):
    return render(request, 'libs/details_expertise.html',{'active_page': detail})

def carriere(request):
    common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(settings.URL_ODOO))
    uid = common.authenticate(settings.DB_ODOO, settings.EMAIL_ODOO_USER, settings.PASSWORD_ODOO, {})
    models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(settings.URL_ODOO))
    list_poste = models.execute_kw(settings.DB_ODOO, uid, settings.PASSWORD_ODOO,
    'hr.job', 'search_read',
    [[['is_published','=',True], ['website_published', '=', True]]],
    {'fields': ['display_name', 'create_uid','write_date','new_application_count','application_count', 'website_description','description'], 'limit': 10})
    
    poste_write_date = datetime.strptime(list_poste[0]['write_date'], '%Y-%m-%d %H:%M:%S')
    format_date = poste_write_date.strftime('%d:%m:%Y %H:%M')
    
    context={
        'postes':list_poste,
        'format_date':format_date,

        'active_page':'carriere'
    }
    return render(request, 'libs/carriere.html',context)

def getDetail(request,id_post):
    context={}
    common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(settings.URL_ODOO))
    print(common)
    uid = common.authenticate(settings.DB_ODOO, settings.EMAIL_ODOO_USER, settings.PASSWORD_ODOO, {})
    models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(settings.URL_ODOO))
    post_data = models.execute_kw(
        settings.DB_ODOO,
        uid,
        settings.PASSWORD_ODOO,
        'hr.job',
        'read',
        [[id_post]],
    )
    context={
        'active_page':'detail',
        'poste':post_data
    }
    return render(request,'libs/detail.html',context)

def postuler(request,id_post):
    context={}
    common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(settings.URL_ODOO))
    print(common)
    uid = common.authenticate(settings.DB_ODOO, settings.EMAIL_ODOO_USER, settings.PASSWORD_ODOO, {})
    models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(settings.URL_ODOO))
    post_data = models.execute_kw(
        settings.DB_ODOO,
        uid,
        settings.PASSWORD_ODOO,
        'hr.job',
        'read',
        [[id_post]],
    )
    context={
        'active_page':'postuler',
        'poste':post_data
    }
    
    return render(request,'libs/services.html',context)

def contact(request):
    if (request.headers.get('x-requested-with')=='XMLHttpRequest'):
        name=request.POST.get('name')
        compagny=request.POST.get('compagny')
        phone=request.POST.get('phone')
        subject=request.POST.get('subject')
        message=request.POST.get('message')
        email=request.POST.get('email')
        ctx={
            'status':True,
            'user': {
                'nom':name,
                'compagny':compagny,
                'phone':phone,
                'subject':subject,
                'message':message,
            }
        }

        if settings.DEBUG:
            send_email_message(
                subject=subject,
                header_from="",
                template_name="server/response.html",
                user_id=email,
                ctx=ctx,
                simple=False
            )
        else:
            send_email_message(
                subject=subject,
                template_name="portail_web/Templates/server/response.html",
                user_id=email,
                ctx=ctx,
                simple=False
            )
        
        return JsonResponse(ctx)
    else :
        return render(request, 'libs/contact.html',{'active_page': 'contact'})

def postulerSpontaner(request):
    context = {}
    if request.method == 'POST':
        isclient = request.POST.get('isClient')
        if(isclient=="true"):
            last_name = request.POST.get('lastName')
            first_name = request.POST.get('firstName')
            email = request.POST.get('email')
            company = request.POST.get('company')
            message = request.POST.get('message')
            
            if(validationMail(email)):
                try :
                    user=Postuler.objects.get(email=email)
                    context={
                        'statut': False,
                        'message': 'Nous avons deja les informations de client dans nos archives'
                    }
                    return JsonResponse(context)
                except ObjectDoesNotExist:
                    user=Postuler.objects.create(email=email)
                    user.nom=last_name
                    user.prenom=first_name
                    user.compagny=company
                    user.message=message
                    user.non_spontaner=False
                    user.type_candidat="client"
                    user.save()
                    context={
                        'statut': True,
                        'message': 'Félicitations, votre message a été transmis.'
                    }
                    return JsonResponse(context)
            else:
                context={
                        'statut': False,
                        'message': 'Une addresse professionnel est nessaire pour transmettre votre demande.'
                    }
                return JsonResponse(context)
        
        else :
            last_name = request.POST.get('lastName')
            first_name = request.POST.get('firstName')
            email = request.POST.get('email')
            cv_file = request.FILES.get('cv')
            message = request.POST.get('message')
            try :
                user=Postuler.objects.filter(email=email).count()
                if(user==2):
                    context={
                        'statut': False,
                        'message': 'Nous avons deja les informations de client dans nos archives'
                    }
                else :
                    new_filename = str(uuid.uuid4()) + '.' + cv_file.name.split('.')[-1]
                    fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'curriculum_vitae'))
                    filename = fs.save(new_filename, cv_file)
                    user=Postuler.objects.create(email=email)
                    user.nom=last_name
                    user.prenom=first_name
                    user.cv=filename
                    user.message=message
                    user.non_spontaner=False
                    user.type_candidat="candidat"
                    user.save()
                    context={
                            'statut': True,
                            'message': 'Félicitations, votre message a été transmis'
                        }  
                return JsonResponse(context)
            except :
                print("Erreur request")
                
    else:
        return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

def postulerOffres(request):
    if (request.headers.get('x-requested-with')=='XMLHttpRequest'):
        fullname = request.POST.get('name').strip()
        email = request.POST.get('email').strip()
        candit_for_post = request.POST.get('candit_for_post').strip()
        departure = request.POST.get('departure').strip()
        message = request.POST.get('message').strip()
        file_path = request.FILES.get('delivery')
        print(candit_for_post,fullname,departure,message,file_path)
        print(fullname.split(' '))
        try :
            #  user=Postuler.objects.create(email=email)
            pass
             
        except :
            print('erreur')
        return JsonResponse({'status': True})
    return JsonResponse({'status':False})