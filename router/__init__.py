import functools
from urllib.parse import urlparse


class _Route:

    """
    {{scheme}}:/{{path/more-path}}?{{param1=something}}&{{param2=somethingelse}}
    """

    # TODO: implement singleton protocol that works with *args and **kwargs

    def __init__(self, route, func, *args, **kwargs):
        self.parsed = urlparse(route)
        self.route = self.parsed.path
        self.scheme = self.parsed.scheme
        self.func = func
        self.args = args
        self.kwargs = kwargs
        # TODO: remove print statement w/ better logging
        print(f"new route created! {route=}, {func=}, {args=}, {kwargs=}")


class URIRouter:

    __instances__: list = []

    def __new__(cls, name, *args, **kwargs):
        for instance in cls.__instances__:
            if instance.name == name:
                # print("returning existing instance")
                return instance
        # print("creating new instance")
        instance = super(URIRouter, cls).__new__(cls, *args, **kwargs)
        URIRouter.__instances__.append(instance)
        return instance

    def __init__(self, name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.__routes__: "list[_Route]" = []

    @classmethod
    def get(cls, name):
        for instance in cls.__instances__:
            if instance.name == name:
                return instance
        return RuntimeError(f"URIRouter({name}) does not exist at runtime")

    def route(self, uri, *args, **kwargs):
        print("handling route")
        def decorator(func):
            print("in func")
            self.__routes__.append(_Route(uri, func, *args, **kwargs))
            @functools.wraps(func)
            def inner_function_handling_gateway(*args, **kwargs):
                self.__routes__.append(_Route(uri, func))
            return inner_function_handling_gateway
        return decorator

    def handle(self, uri):
        print("attempting to handle")
        parsed = urlparse(uri)
        for route in self.__routes__:
            print(parsed.path, route.route)
            # TODO: need to check the scheme as well
            if parsed.path == route.route:
                print("found!")
                for item in parsed.query.split("&"):
                    print(item)
                    key, value = item.split("=")
                    if key in route.kwargs.keys():
                        # TODO: better logging and handling
                        print("Key Exists! Overriding")
                    route.kwargs[key] = value
                route.func(*route.args, **route.kwargs)
                return True
        return False
