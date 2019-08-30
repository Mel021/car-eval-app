from django.views import View
from django.shortcuts import render
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score,confusion_matrix
from sklearn import tree
from sklearn.metrics import r2_score, explained_variance_score, mean_absolute_error
import pickle 
from sklearn import *
from django.http import HttpResponse
from django.conf import settings
import os
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from eval.models import CarEval as carmodel

# Create your views here. 

def home (request):
	return render (request,'welcome.html',context={})

def index (request):
	return render (request,'index.html',context={})

@csrf_exempt
def get_class (request):
	print ("REquest")
	if request.POST.get ('bttn'):
		print ("Class predicted")
		ans = Car_Predict.get (request.POST.get('buying'),request.POST.get('maint'),request.POST.get('doors'),request.POST.get('persons'),request.POST.get('leg_boot'),request.POST.get('safety'))
		html = "".format(ans)
		print (carmodel.objects.all())
		return render (request,'class.html',{'original_input':{'buying':request.POST.get('buying'),'maintenance':request.POST.get('maint'),'doors':request.POST.get('doors'),'persons':request.POST.get('persons'),'leg_boot':request.POST.get('leg_boot'),'safety':request.POST.get('safety')},'result':ans})

class Car_Train (View):
	def get (self,request):
		path_d = os.path.join(settings.MODEL_DATA,'car.data')
		data = pd.read_csv(path_d,sep=',')
		data.columns = ['buying','maint','doors','persons','leg_boot','safety','class']
		new_col={"buying":{"vhigh":4,"high":3,"med":2,"low":1},"maint":{"vhigh":4,"high":3,"med":2,"low":1},"leg_boot":{"small":0,"med":1,"big":2},"safety":{"low":0,"med":1,"high":2},"doors":{"2":2,"3":3,"4":4,"5more":5},"persons":{"2":2,"4":4,"more":5},"class":{"unacc":0,"acc":1,"good":2,"vgood":3}}
		data.replace(new_col,inplace=True)
		model_name = 'model'
		x = data[['buying','maint','doors','persons','leg_boot','safety']]
		y = data['class']

		xt, xte, yt, yte = train_test_split (x,y,random_state=0)
		cl = ensemble.RandomForestClassifier(n_estimators=500)
		cl = cl.fit(xt,yt)

		path_m = os.path.join (settings.MODEL_ROOT,model_name+".pkl")
		with open (path_m,'wb') as f:
			pickle.dump(cl,f)
		return render (request,'class.html',{'model_result':'model created and saved'})

class Car_Predict (View):
	def get (a,b,c,d,e,f):
		#if request.method == 'POST':
		path = os.path.join(settings.MODEL_ROOT,'model.pkl')
		with open (path,'rb') as model:
			mod = pickle.load(model)
		ans = mod.predict (pd.DataFrame([[int(a),int(b),int(c),int(d),int(e),int(f)]]))
		if ans == 0:
			ans = "unacceptable"
		elif ans == 1:
			ans = "acceptable"
		elif ans == 2:
			ans = "good"
		else:
			ans = "v-good"
		careval_instance = carmodel(buying_price = a,maintenance = b,doors = c,persons = d,boot_space = e,safety = f,label=ans)
		careval_instance.save()
		
		return ans
