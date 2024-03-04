def isRequestPost(request):
    #Query by POST methode, Query = dt. Abfrage
    return request.method == 'POST'