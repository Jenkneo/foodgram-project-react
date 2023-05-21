def is_base_func(request, obj, model=None):
    user = request.user
    if user.is_anonymous:
        return False
    elif model:
        return model.objects.filter(user=user, recipe=obj).exists()
    elif request:
        return user.subscriptions.filter(author=obj).exists()
