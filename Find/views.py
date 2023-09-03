from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SearchForm , PathForm
import os

def base(request):

    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            # Process the form data (e.g., save to the database)
            query = form.cleaned_data['query']
            # Add your processing logic here
            print('ans - ',query)
    else:
        print("hi")   
        form = SearchForm()
    return render(request,'base.html', {'form': form})

def path(request):

    if request.method == 'POST':
        form = PathForm(request.POST)
        if form.is_valid():
            # Process the form data (e.g., save to the database)
            dir = form.cleaned_data['path']
            print('ans - ',dir)

            if os.path.exists(dir):

                if os.path.isdir(dir):

                    return redirect('base/')
                else:
                    messages.error(request, 'Path not a directory.')                
            else:
                messages.error(request, 'Path does not exist.')
                return render(request,'home.html', {'form': form})
            
    else:
        print("hi")
        form = PathForm()
    return render(request,'home.html', {'form': form})