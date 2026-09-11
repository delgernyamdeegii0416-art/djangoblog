from django.shortcuts import render


def home(request):
    return render(request, 'blog/home.html', {'title': 'This is the Djangblog Homepage.'})

def about(request):
    return render(request,'blog/about.html', {'team': 'This is the Djangoblog team.'})   

def contact(request):
    return render(request,'blog/contact.html',{'content': 'i`m Deegii.'})     

    