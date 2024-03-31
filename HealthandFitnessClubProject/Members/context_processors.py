def get_current_user(request):
    return {'user': request.user}
