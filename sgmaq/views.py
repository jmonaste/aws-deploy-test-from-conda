from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib.auth.decorators import login_required
from PIL import Image
import piexif
from django.http import JsonResponse
import json
import os
from datetime import datetime, date
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from .models import Task
from django.db.models import Count


def index(request):
    return render(request, 'global/index.html')

def about(request):
    return render(request, 'global/about.html')

@csrf_protect
def signup(request):
    if request.method == 'GET':
        return render(request, 'global/signup.html', {"form": UserCreationForm})
    else:

        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    request.POST["username"], password=request.POST["password1"])
                user.save()
                login(request, user)
                return redirect('index')
            except IntegrityError:
                return render(request, 'global/signup.html', {"form": UserCreationForm, "error": "Username already exists."})

        return render(request, 'global/signup.html', {"form": UserCreationForm, "error": "Passwords did not match."})

@csrf_protect
def signin(request):
    if request.method == 'GET':
        return render(request, 'global/signin.html', {"form": AuthenticationForm})
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'global/signin.html', {"form": AuthenticationForm, "error": "Username or password is incorrect."})

        login(request, user)
        return redirect('index')

@csrf_protect    
def signout(request):
    logout(request)
    return redirect('index')



def tasks(request):
    return render(request, 'tasks/tasks.html')





def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def parse_gps_coordinate(coord):
    # Convierte una cadena del tipo '[40, 25, 3347/100]' en una lista de números
    coord = coord.strip('[]')
    parts = coord.split(', ')
    return [int(parts[0]), int(parts[1]), float(parts[2].split('/')[0]) / float(parts[2].split('/')[1])]

def convert_to_degress(value):
    d = value[0][0] / value[0][1]
    m = value[1][0] / value[1][1]
    s = value[2][0] / value[2][1]

    return d + (m / 60.0) + (s / 3600.0)

def get_exif_data(image_path):
    exif_data = {
        "datetime": None,
        "latitude": None,
        "longitude": None,
    }
    try:
        img = Image.open(image_path)
        exif_dict = piexif.load(img.info['exif'])
        
        # Fecha y hora
        if piexif.ExifIFD.DateTimeOriginal in exif_dict['Exif']:
            exif_data["datetime"] = exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal].decode('utf-8')
        
        # Geolocalización
        gps_info = exif_dict.get('GPS', {})
        if gps_info:
            lat = gps_info.get(piexif.GPSIFD.GPSLatitude)
            lat_ref = gps_info.get(piexif.GPSIFD.GPSLatitudeRef)
            lon = gps_info.get(piexif.GPSIFD.GPSLongitude)
            lon_ref = gps_info.get(piexif.GPSIFD.GPSLongitudeRef)

            if lat and lat_ref and lon and lon_ref:
                exif_data["latitude"] = convert_to_degress(lat) * (1 if lat_ref == b'N' else -1)
                exif_data["longitude"] = convert_to_degress(lon) * (1 if lon_ref == b'E' else -1)
    except Exception as e:
        print(f"Error extracting EXIF data: {e}")

    return exif_data

def get_exif_data_from_file(f):
    exif_data = {
        "datetime": None,
        "latitude": None,
        "longitude": None,
    }
    try:
        img = Image.open(f)
        exif_dict = piexif.load(img.info['exif'])

        # Fecha y hora
        if piexif.ExifIFD.DateTimeOriginal in exif_dict['Exif']:
            exif_data["datetime"] = exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal].decode('utf-8')
        
        # Geolocalización
        gps_info = exif_dict.get('GPS', {})
        if gps_info:
            lat = gps_info.get(piexif.GPSIFD.GPSLatitude)
            lat_ref = gps_info.get(piexif.GPSIFD.GPSLatitudeRef)
            lon = gps_info.get(piexif.GPSIFD.GPSLongitude)
            lon_ref = gps_info.get(piexif.GPSIFD.GPSLongitudeRef)

            if lat and lat_ref and lon and lon_ref:
                exif_data["latitude"] = convert_to_degress(lat) * (1 if lat_ref == b'N' else -1)
                exif_data["longitude"] = convert_to_degress(lon) * (1 if lon_ref == b'E' else -1)
    except Exception as e:
        print(f"Error extracting EXIF data: {e}")

    return exif_data

def process_image(image_path):
    return "HVD1234", "100"

def handle_uploaded_file(f):
    # Define the upload directory using default_storage
    upload_dir = settings.MEDIA_ROOT
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    
    # Generate the file path
    file_path = os.path.join(upload_dir, f.name)
    
    try:
        # Save the file using default_storage
        file_name = default_storage.save(file_path, ContentFile(f.read()))
        return file_name
    except Exception as e:
        # Handle exceptions, log error or raise it
        print(f"Error uploading file: {e}")
        raise

def convert_datetime_format(exif_datetime):
    """
    Convierte una fecha y hora en formato EXIF (YYYY:MM:DD HH:MM:SS)
    a un formato aceptado por Django (YYYY-MM-DD HH:MM:SS).
    """
    try:
        # Convertir la cadena de fecha y hora de EXIF a un objeto datetime
        dt = datetime.strptime(exif_datetime, "%Y:%m:%d %H:%M:%S")
        # Convertir el objeto datetime a una cadena en el formato aceptado por Django
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except ValueError as e:
        print(f"Error al convertir el formato de fecha y hora: {e}")
        return None




@login_required
@csrf_exempt
def register_wash(request):
    if request.method == 'POST' and is_ajax(request):
        image_file = request.FILES['license_plate_photo']
        
        # Leer los metadatos EXIF directamente del archivo recibido
        exif_data = get_exif_data_from_file(image_file)
        print(exif_data)

        # Guardar la imagen en el servidor
        image_path = handle_uploaded_file(image_file)
        
        # Procesar la imagen
        license_plate_text, license_plate_text_score = process_image(image_path)

        if license_plate_text:
            # Guardar la ruta de la imagen en la sesión
            request.session['uploaded_image_path'] = image_path

            return JsonResponse({
                'success': True, 
                'license_plate_text': license_plate_text, 
                'image_url': request.build_absolute_uri(settings.MEDIA_URL + os.path.basename(image_path)),
                'exif_data': exif_data
            })
        else:
            return JsonResponse({'success': False, 'error': 'No se pudo detectar la matrícula.'})

    return JsonResponse({'success': False, 'error': 'Solicitud inválida.'})




@csrf_exempt
@login_required
def create_task(request):
    if request.method == 'POST' and is_ajax(request):
        data = json.loads(request.body)
        license_plate = data.get('license_plate')

        # Retrieve uploaded image path from session
        uploaded_image = request.session.get('uploaded_image_path')

        # Obtén los metadatos EXIF
        license_plate_img_datetime = data.get('imgDatetime')
        license_plate_img_lat = data.get('imgLat')
        license_plate_img_long = data.get('imgLong')

        if license_plate and uploaded_image and request.user.is_authenticated:
            task = Task.objects.create(
                license_plate=license_plate,
                comment="generado automáticamente",
                license_plate_image=uploaded_image,
                created=datetime.now(),
                datecompleted=datetime.now(),
                employee_user=request.user,
                img_datetime=convert_datetime_format(license_plate_img_datetime),
                img_lat=license_plate_img_lat,
                img_long=license_plate_img_long,

            )
            return JsonResponse({'success': True, 'task_id': task.id})
        else:
            return JsonResponse({'success': False, 'error': 'Datos inválidos o usuario no autenticado.'})

    return JsonResponse({'success': False, 'error': 'Solicitud inválida.'})




@login_required
def task_overview(request):
    tasks = Task.objects.all()
    # Recuento por días
    task_counts = tasks.extra({'datecreated': "date(created)"}).values('datecreated').annotate(count=Count('id')).order_by('datecreated')

    task_data = []
    for task in tasks:
        task_data.append({
            'id': task.id,
            'license_plate': task.license_plate,
            'comment': task.comment,
            'license_plate_image': str(task.license_plate_image.url),
            'created': str(task.created),
            'datecompleted': str(task.datecompleted),
            'employee_user_id': task.employee_user_id,
            'img_datetime': str(task.img_datetime),
            'img_lat': task.img_lat,
            'img_long': task.img_long
        })

    task_counts_list = [
        {'datecreated': item['datecreated'].isoformat() if isinstance(item['datecreated'], (datetime, date)) else item['datecreated'], 'count': item['count']}
        for item in task_counts
    ]

    return render(request, 'tasks/task_overview.html', {
        'tasks': tasks,
        'task_data_json': json.dumps(task_data),
        'task_counts': json.dumps(task_counts_list),  # Pass as JSON string
    })