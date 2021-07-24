def get_limit(request):
    try:
        limit = int(request.query_params['recipes_limit'])
        if limit <= 0:
            raise ValueError()
        return limit
    except (KeyError, ValueError):
        pass
    return None
