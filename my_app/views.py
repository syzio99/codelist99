from django.shortcuts import render
from bs4 import BeautifulSoup

import requests
from requests.compat  import quote_plus
from . import models


BASE_URL = 'https://www.coursera.org/search?query={}'

# Create your views here.
def home(request):
    return render(request,'base.html')

def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    final_url = BASE_URL.format(quote_plus(search))
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')
    
    post_listings = soup.find_all('li', {'class' : 'ais-InfiniteHits-item'})
    final_posting = []
    for post in post_listings:
        try:
            post_title = post.find(class_='card-title').text
            post_spec = post.find(class_ = "_jen3vs").text
            post_upl = post.find(class_ = "partner-name").text
            post_img = post.find(class_ = "product-photo")['src']
            post_url = "https://www.coursera.org"+post.find('a').get('href')
            final_posting.append((post_title,post_spec,post_upl,post_img,post_url))
        except:
            pass

    send = {
        'search':search,
        'final_posting':final_posting,
    }
    
    return render(request,'my_app/new_search.html',send)