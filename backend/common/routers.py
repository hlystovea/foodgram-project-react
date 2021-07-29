from rest_framework.routers import Route, SimpleRouter


class CustomRouter(SimpleRouter):
    routes = [
        Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={
                'get': 'create',
                'delete': 'destroy',
            },
            name='{basename}-write',
            detail=False,
            initkwargs={'suffix': 'Write'}
        ),
    ]
