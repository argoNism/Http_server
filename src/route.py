from controller import NormalController
from controller import ArticleController
import os

def route(request):
    head, tail = os.path.split(request.target)

    print("request.type",request.type)

    if request.target.startswith("/blog"):
        controller = ArticleController()

        if request.type == "GET":
            return controller.do_get(request)
        elif request.type == "POST":
            print("do_post\n")
            return controller.do_post(request)


    else:
        controller = NormalController()
        return controller.do_get(request)
