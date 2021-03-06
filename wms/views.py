from django.shortcuts import render,get_object_or_404
from .models import Plant,Tank
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login
from django.views.generic import View
from .forms import UserForm,LoginForm
from django.contrib.auth import logout
from django.contrib.auth.models import User
# from django.conf.urls.defaults import *
# import datetime

def index(request):
	all_plants=Plant.objects.all()
	all_tanks=Tank.objects.all()
	context={'all_tanks':all_tanks,
		'all_plants':all_plants,
	}
	return render(request,'wms/index.html',context)

def about(request):
	return render(request,'wms/about.html',{})

def get_data(request):
    tank_water_level=request.GET['twl']
    soil_moisture=request.GET['sm']
    plant_id=request.GET['pid']
    tank_id=request.GET['tid']
    is_raining=request.GET['rain']
    p=Plant.objects.get(id=plant_id)
    t=Tank.objects.get(id=tank_id)
    p.plant_data_set.create(soilMoisture=soil_moisture,pH=7,raining=is_raining)
    t.tank_data_set.create(tankWaterLevel=tank_water_level)
    return redirect('wms:plant_database',plant_id)

def calc_average(plant_data):
    spH=ssM=0
    for i in plant_data:  
        spH+=i.pH
        ssM+=i.soilMoisture
    averagepH=spH/len(plant_data)
    averageSoilMoisture=ssM/len(plant_data)
    return (averagepH,averageSoilMoisture)
def plant_details(request,plant_id):
    # getting plan object
    plant=get_object_or_404(Plant,id=plant_id)
    # getting the latest value of tank water level
    c=plant.tank.tank_data_set.count()
    tank_data=plant.tank.tank_data_set.all()
    tank_data10=tank_data.order_by('-id')[:12][::-1]

    plant_data=plant.plant_data_set.all()
    (plant.averagepH,plant.averageSoilMoisture)=calc_average(plant_data)
    plant.save()
    latest_plant=plant_data[len(plant_data)-1]

    latest_plant_pH=latest_plant.pH
    percent_plant_pH=latest_plant_pH/1.4
    latest_plant_soilMoisture=latest_plant.soilMoisture
    percent_plant_soilMoisture=latest_plant.soilMoisture/100
    latest_tank_water_level=plant.tank.tank_data_set.all()[c-1].tankWaterLevel
    percent_tank_water_level=latest_tank_water_level/10
    is_raining=latest_plant.raining
    plant_data10=plant_data.order_by('-id')[:12][::-1]

    context={
    'plant':plant,#plant
    'latest_tank_water_level':latest_tank_water_level,#last tank water level reported for the tank
    'percent_tank_water_level':percent_tank_water_level,
    'tank_data10':tank_data10,#list of all the database
    'plant_data10':plant_data,
    
    'latest_plant_soilMoisture':latest_plant_soilMoisture,
    'latest_plant_pH':latest_plant_pH,
    'percent_plant_soilMoisture':percent_plant_soilMoisture,
    'percent_plant_pH':percent_plant_pH,
    'is_raining':is_raining,
    }
    return render(request,'wms/plant_detail.html',context)

def plant_database(request,plant_id):
    plant=get_object_or_404(Plant,id=plant_id)
    plant_data=plant.plant_data_set.all().order_by('-id')
    tank_data=plant.tank.tank_data_set.all().order_by('-id')
    zipped=zip(plant_data,tank_data)
    context={ 
    'plant':plant,
    'zipped':zipped,
    }
    return render(request,'wms/plant_detail_database.html',context)

def tank_details(request,tank_id):
	tank=get_object_or_404(Tank,id=tank_id)
	return render(request,'wms/tank_detail.html',{'tank':tank}) 

def construction(request):
    return render(request,'wms/coming_soon.html')

def plants(request):
    #plants=User.plant_set.all()
    return render(request,'wms/plants.html')

# class UserFormView(View):
# 	form_class=UserForm(request.POST or None)
# 	template_name='wms/reg_form.html'
# 	#displaying a blank form
# 	def get(self,request):
# 		form=self.form_class(None)
# 		return render(request,self.template_name,{'form':form})
# 	#adding user to database
# 	def post(self,request):
# 		form=self.form_class(request.POST)
# 		if(form.is_valid()):
# 			user=form.save(commit=False)
# 			#cleaned data
# 			username=form.cleaned_data['username']
# 			password=form.cleaned_data['password']
# 			user.set_password(password)
# 			user.username=username
# 			user.save()

# 			# if credentials are correct
# 			user=authenticate(username=username,password=password)
# 			if user is not None:
# 				if user.is_active:
# 					login(request,user)
# 					return redirect('wms:index')
# 		return render(request,self.template_name,{'form':form})


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    # return render(request, 'wms/login.html', context)
    return redirect('wms:index')


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                # albums = Album.objects.filter(user=request.user)
                return render(request, 'wms/index.html')
            else:
                return render(request, 'wms/login_new.html', {'error_message': 'Your account has been disabled'})
        if user is None:
            return render(request, 'wms/login_new.html', {'error_message': 'Invalid login'})
    return render(request, 'wms/login_new.html')

# def login_prad(request):
#     if request.method == "POST":
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(username=username, password=password)
#         if user is not None:
#             if user.is_active:
#                 login(request, user)
#                 # albums = Album.objects.filter(user=request.user)
#                 return render(request, 'wms/index.html')
#             else:
#                 return render(request, 'wms/login_pradeep.html', {'error_message': 'Your account has been disabled'})
#         if user is None:
#             return render(request, 'wms/login_pradeep.html', {'error_message': 'Invalid login'})
#     return render(request,'wms/login_pradeep.html',{})

def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        email=form.cleaned_data['email']
        password = form.cleaned_data['password']
        # user=User.objects.create_user(username=username,password=password,email=email)
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if(user is None):
            print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            print(username)
            print(password)
            print(email)
        if user is not None:
            if user.is_active:
                login(request, user)
                # plants = Plant.objects.filter(user=request.user)
                # tanks  = Tank.objects.filter(user=request.user)
                return redirect('wms:index')
    context = {
        "form": form,
    }
    return render(request, 'wms/login_new.html', context)