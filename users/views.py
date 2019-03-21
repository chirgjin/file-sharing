from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.conf import settings
from django.views.generic import CreateView
from .models import Document, Profile
from django.core.files.storage import FileSystemStorage
from .forms import DocumentForm

def home(request):
	return render(request, 'users/home.html')

def register(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f'Account for {username} has been successfully created!')
			return redirect('login')
	else:
		form = UserCreationForm()
	return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
	profile = Profile.objects.get(user=request.user)
	docs = Document.objects.filter(user=request.user)
	return render(request, 'users/profile.html', {'profile': profile, 'docs': docs, 'media': settings.MEDIA_URL})

# class DocumentCreateView(CreateView):
# 	model = Document

# 	success_url = '/accounts/profile'
# 	fields = ['file', 'name']

# 	def form_valid(self, form):		
# 		form.instance.user = self.request.user
# 		file = self.request.FILES['file']
# 		fs = FileSystemStorage()
# 		filename = fs.save(file.name, file)
# 		self.object = form.save()
# 		print("uuuuuuuuuu")
# 		print(self.object.id)
# 		profile = Profile.objects.get(user=self.request.user)
# 		print(profile)
# 		file = Document.objects.get(id=self.object.id)
# 		print(file)
# 		profile.docs.add(file)
# 		return super().form_valid(form)

def file_upload(request):
	if request.method == 'POST':
		form = DocumentForm(request.POST, request.FILES)
		if form.is_valid():
			form.instance.user = request.user
			object = form.save()
			profile = Profile.objects.get(user=request.user)
			print(profile)
			print(object)
			file = Document.objects.get(id=object.id)
			print(file)
			profile.docs.add(file)
			return redirect('profile')
	else:
		form = DocumentForm()
	return render(request, 'users/document_form.html', {
		'form': form
	})