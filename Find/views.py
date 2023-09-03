from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SearchForm , PathForm
import os

import chromadb
import os

# Explorer function
final = []
metadatas = []
chroma_client = chromadb.Client()

collection = chroma_client.create_collection(name="System-db")

def listdirs(rootdir):
    for it in os.scandir(rootdir):
        if it.is_dir():
            if not os.listdir(it):
                # Empty
                if '/' in it.path:
                    final.append('folder ' + it.path.replace('/', ' '))
                else:
                    final.append('folder ' + it.path.replace("\\", ' '))
                    
                metadatas.append({"source": 'folder - ' + it.path})
                continue

            # Non empty dir
            listdirs(it)
        else:
            # Is a file
            final.append('file ' + it.path.replace("\\", ' '))
            metadatas.append({"source": '--file - ' + it.path})


def init(path):
    global final, metadatas

    # Adding all file paths to list
    final = []
    metadatas = []
    listdirs(path)

    # Adding all to the database
    ids = []
    for i in range(len(final)):
        ids.append("id" + str(i+1))
        
    collection.add(
        documents=final,
            metadatas=metadatas,
            ids=ids
        )

def search(query):
    results = collection.query(
        query_texts=[query],
        n_results=3
    )

    ans = []
    print(results)

    for item in results['metadatas'][0]:
        
        # if item['source'][0] == '-':
        ans.append(item['source'][9:])
    
    return ans

def base(request):

    result = []

    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            # Process the form data (e.g., save to the database)
            query = form.cleaned_data['query']
            # Add your processing logic here
            print('ans - ',query)

            result = search(query)
            print(result)

    else:
        form = SearchForm()
    return render(request,'base.html', {'form': form, 'searchResults': result})

def path(request):

    if request.method == 'POST':
        form = PathForm(request.POST)
        if form.is_valid():
            # Process the form data (e.g., save to the database)
            dir = form.cleaned_data['path']
            print('ans - ',dir)

            if os.path.exists(dir):

                if os.path.isdir(dir):

                    # messages.success(request, 'Please wait while the databse is created') 
                    init(dir)

                    return redirect('base/')
                else:
                    messages.error(request, 'Path not a directory that exists.')                
            else:
                messages.error(request, 'Path not a directory that exists.')
                return render(request,'home.html', {'form': form})
            
    else:
        print("hi")
        form = PathForm()
    return render(request,'home.html', {'form': form})