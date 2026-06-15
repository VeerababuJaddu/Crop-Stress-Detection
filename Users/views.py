from django.shortcuts import render

from Users.utility.classification_report import Classification_report
from .models import UserRegistrationModel
from django.contrib import messages

# Create your views here.
def userHome(request):
    return render(request,'users/userHome.html')
def register(request):
    if request.method=='POST':
        name=request.POST['name']
        email=request.POST['email']
        loginid=request.POST['loginid']
        password=request.POST['password']
        mobile=request.POST['mobile']
        locality=request.POST['locality']
        state=request.POST['state']

        try:

            userRegister=UserRegistrationModel(name=name,email=email,loginid=loginid,password=password,mobile=mobile,locality=locality,address=state)
            if userRegister:
                userRegister.save()
                messages.error(request,' Enter deatils saved  sucessfully')
                return render(request,'userRegister.html')
            else:
                messages.error(request,'Invalid Details , Enter deatils carefully')
                return render(request,'userRegister.html')
        except Exception as e:
            pass
            messages.error(request,e)
            return render(request,'userRegister.html')


def userLoginCheck(request):
    if request.method=="POST":
        loginid=request.POST['username']
        password=request.POST['password']

        try:
            user=UserRegistrationModel.objects.get(loginid=loginid,password=password)

            status=user.status
            print(status)
            if status=='activated':
               
                return render(request,'users/userHome.html')
            else:
                messages.error(request,'Status Not Actiavted')
                return render(request,'userLogin.html')
        except Exception as e:
            pass
            messages.error(request,'Invalid details')
            return render(request,'userLogin.html')

def Classification_result(request):
    accuracy=Classification_report()
    return render(request,'users/classification_view.html',{'accuracy':accuracy})


import os
from django.core.files.storage import default_storage
from django.conf import settings
from .utility.prediction import predict_image

def prediction(request):
    print("Prediction view called")  # Debugging: View entry point

    if request.method == 'POST' and 'image' in request.FILES:
        print("POST request received with image file")  # Debugging: POST request with image

        # Save uploaded image temporarily
        image_file = request.FILES['image']
        print(f"Uploaded file name: {image_file.name}")  # Debugging: File name

        # Ensure that the 'temp' directory exists
        temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp')
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
        try:
            file_path = default_storage.save('temp/' + image_file.name, image_file)
            print(f"File saved at: {file_path}")  # Debugging: Saved file path

            temp_image_path = default_storage.path(file_path)
            print(f"Full filesystem path: {temp_image_path}")  # Debugging: Full filesystem path

            # Predict the image
            predicted_label, confidence = predict_image(temp_image_path)
            print(f"Predicted label: {predicted_label}")  # Debugging: Predicted label
            if confidence < 0.5:
                return render(request, 'users/prediction.html', {'error_message': "Invalid image please Upload Valid Image"})

            # Generate the URL for the uploaded image
            image_url = settings.MEDIA_URL + file_path
            print(f"Image URL: {image_url}")  # Debugging: Image URL

            return render(request, 'users/prediction.html', {
                'predicted_label': predicted_label,
                'image_url': image_url,  # Pass the image URL to the template
            })
        except:
            return render(request, 'users/prediction.html', {'error_message': "Invalid image please Upload Valid Image"})



    print("Rendering empty prediction form")  # Debugging: GET request or no image
    return render(request, 'users/prediction.html')
