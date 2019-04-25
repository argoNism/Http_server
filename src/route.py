from controller import NormalController
from controller import ArticleController
import os

def route(request):
    head, tail = os.path.split(request.target)
    
    if request.target.startswith("/blog/"):
        return ArticleController()
    else:
        print("give a NormalController")
        return NormalController()
