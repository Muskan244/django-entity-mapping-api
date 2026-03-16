def get_object_or_none(model, pk):
    try:
        return model.objects.get(pk=pk)
    except model.DoesNotExist:
        return None
