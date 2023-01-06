from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import json
import requests
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.decorators import api_view
# Create your views here.
@api_view(['GET','POST'])
def login(request):
    return render(request,'login.html')

@api_view(['GET'])
@login_required
def home(request):
    user=request.user
    #token='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'
   
    #headers = {'Authorization': 'token ' + token}
    user_details= requests.get('https://api.github.com/users/' + f"{user.username}", headers="")
    data=user_details.json()
    
    repo_details = requests.get('https://api.github.com/users/' +f"{user.username}"+'/repos',headers="")
    data["total_repos"]=len(repo_details.json())
    return render(request,'home.html',{"data":data})
#https://api.github.com/repos/archana-1209/animal-tracking
@api_view(['POST'])
@login_required
def create_repo(request):
    name=request.data.get('repo_name',None)
    description=request.data.get('repo_description',None)
    if not name:
        message="Repo Name required"
    elif not description:
        message="Description Required"
    elif not name and not description:
        message="Repo Name and Description Required"
    else:
        user=request.user
        token='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'
        # #url='https://api.github.com/' + f"{request.user.username}"+'/repos'
        # #print(url)
        # login = requests.post('https://api.github.com/user/' + f"{request.user.username}"+'/repos',data=json.dumps(payload))
        # print(login)
        # repo = 'some_repo'
        # description = 'Created with api'
        payload = {'name': name, 'description': description, 'auto_init': 'true'}

        repo= requests.post('https://api.github.com/' + 'user/repos', auth=(user,token), data=json.dumps(payload))
        if repo.status_code==422:
            json_data=repo.json()
            message=json_data["errors"][0]["message"]
        elif repo.status_code==201:
            message='created successfully'
    
    return render(request,'create_repo.html',{"data":message})
    #return JsonResponse({'msg':repo.json(),"status":repo.status_code})

@api_view(['GET','DELETE'])
@login_required   
def delete_repo(request,repo_name):

    user = request.user.username
    token='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'

    headers = {'Authorization': 'token ' + token}

    repo = requests.delete('https://api.github.com/' + 'repos/' + f"{user}" + '/' + f"{repo_name}", headers=headers)
    
    msg='deleted successfully '+f"{repo_name}"+" repo "
    return JsonResponse({'msg':msg,"status":repo.status_code})


@api_view(['GET'])
@login_required
def repos_list(request):
    token='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'

    headers = {'Authorization': 'token ' + token}
    params={
       
        "sort":"updated"
    }
    details = requests.get('https://api.github.com/user/' + 'repos', headers=headers,params=params)
    p = Paginator(details.json(), 10) 
    page_number = request.GET.get('page')
    try:
        repos_list = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        repos_list = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        repos_list= p.page(p.num_pages)

    return render(request,'profile.html',{"repos_list":repos_list})
    

@api_view(['GET'])
@login_required
def get_repo(request):
    return render(request,'create_repo.html')
    