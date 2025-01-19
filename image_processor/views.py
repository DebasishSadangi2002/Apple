from django.shortcuts import render
from .forms import UploadImageForm
from .models import UploadedImage
from .ml_model import process_image
from PIL import Image


def process_image_view(request):
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = form.save(commit=False)
            crop_type = request.POST.get('crop_type')  # Get crop type from the form
            
            uploaded_image.save()

            image_path = uploaded_image.image.path
            result, confidence = process_image(image_path)  # Process the image with selected crop type

            # Display the uploaded image using Django's ImageField
            image = uploaded_image.image

            return render(request, 'image_processor/result.html', {'result': result, 'image': image, 'confidence': confidence})
    else:
        form = UploadImageForm()
    return render(request, 'image_processor/upload.html', {'form': form})

def home(request):
    return render(request, 'image_processor/index.html')

def image_list(request):
    images = UploadedImage.objects.all()
    return render(request, 'image_processor/image_list.html', {'images': images})

