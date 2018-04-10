from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import Urls
from django.views.decorators.csrf import csrf_exempt
import sys


FORMULARIO = """
    <form action="" method="POST">
    INTRODUCE UNA URL:<br>
    <input type="text" name="url" value=""><br>
    <input type="submit" value="Listo">
    </form>
            """


NO_URL_MESSAGE = """
    <html><body><h1>404 NOT FOUND</h1>
    <p>Error: Introduce una URL, por favor.</p></body></html>
    """


def completar(url):
    if url.find("http://") != 0 and url.find("https://") != 0:
        # la url NO empieza por http:// o https://
        url = ("http://" + url)  # añadimos http:// al inicio
    return url


def acortar_url(num):
    url_acort = "http://localhost:8000/" + str(num)
    return url_acort


def mostrar_url(url_orig, url_acort):
    titulo = "<h1>PRACTICA 2 - SARO - Web Acortadora de Urls</h1>\
               <title>P2-SARO</title>"
    enlace = ("Url real --> <a href='" + url_orig + "'>" + url_orig + "\
                </a><br>Url acortada --> <a href='" + url_acort + "'>\
                " + url_acort + "</a>")
    htmlAnswer = "<html><body>" + titulo + "<p>URLS AÑADIDAS:\
                    </p>" + enlace + "</body></html>"

    return htmlAnswer


def mostrar_principal(urls):
    salida = "<html><h1>PRACTICA 2 - SARO - Web Acortadora de Urls</h1>\
              <title>P2-SARO</title>" + FORMULARIO + "\
              <p>URLs REALES hasta el momento:</p>"

    for my_url in urls:
        salida += '<li><a href="' + my_url.orig + '">' + my_url.orig + '</a>'
    salida += "<p>URLs ACORTADAS hasta el momento:</p>"

    for my_url in urls:
        salida += '<li><a href="' + my_url.acort + '">' + my_url.acort + '</a>'
    salida += "</html>"

    return salida


@csrf_exempt
def root_page(request):
    if request.method == "GET":
        my_urls = Urls.objects.all()
        htmlAnswer = mostrar_principal(my_urls)
        return HttpResponse(htmlAnswer)
    elif request.method == "POST":  # POST
        try:
            #urls = Urls.objects.all() #Para BORRAR urls guardadas
            #urls.delete()
            url = request.POST['url']
            if(url == '' or url.isspace()):  # si la url es blanca o nula
                return HttpResponse(NO_URL_MESSAGE)
            url = completar(url)

            try:
                url_db = Urls.objects.get(orig=url)
                htmlAnswer = mostrar_url(url_db.orig, url_db.acort)
                return HttpResponse(htmlAnswer)

            except Urls.DoesNotExist:  # add a la DB
                num = len(Urls.objects.all())
                url_acort = acortar_url(num)
                try:
                    new_url = Urls(orig=url, acort=url_acort)
                    new_url.save(force_insert=True)  # add url
                except IntegrityError:
                    htmlAnswer = "<html><body><h1>ERROR 404 NOT FOUND</h1>\
                            <p>Error al guardar la URL</p></body></html>"
                url_add = Urls.objects.all().last()  # ultima url agregada
                htmlAnswer = mostrar_url(url_add.orig, url_add.acort)
                return HttpResponse(htmlAnswer)

        except:
            print("Unexpected error:", sys.exc_info()[0])
            return HttpResponse(NO_URL_MESSAGE)
    else:
            htmlAnswer = "<html><body><h1>ERROR 404 NOT FOUND</h1>\
                           <p>Metodos unicos: GET o POST</p></body></html>"
            return HttpResponse(htmlAnswer)


@csrf_exempt
def redirect_page(request, recurso):
    if request.method == "GET":
        try:
            url = acortar_url(recurso)
            url = Urls.objects.get(acort=url)
            http_redirect = ("<meta http-equiv='" + "refresh'\
                             " + 'content="' + '0;URL=' + url.orig + '">')
            htmlAnswer = ("<html><body>REDIRIGIENDO...\
                             " + http_redirect + "</body></html>")
            return HttpResponse(htmlAnswer)

        except Urls.DoesNotExist:
            htmlAnswer = "<html><body><h1>404 NOT FOUND</h1>\
            <p>Error: RECURSO NO DISPONIBLE.</p></body></html>"
            return HttpResponse(htmlAnswer)
    else:
        htmlAnswer = "<html><body><h1>404 NOT FOUND</h1>\
        <p>Error: Para esta URL, solo es valido un GET.</p></body></html>"
        return HttpResponse(htmlAnswer)
