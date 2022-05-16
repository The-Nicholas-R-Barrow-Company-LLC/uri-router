import functools
from router import URIRouter


handler = URIRouter(__name__)


@handler.route("flagship:/this/long/url", "Nick", sirname="HRM")
def home(name, sirname = "Mr.", *args, **kwargs):
    print(f"Hello, {sirname} {name}")
    print(kwargs)


def main():
    simulated_received_uri = "flagship:/this/long/url?param1=foo&param2=2"
    handler.handle(simulated_received_uri)


if __name__ == "__main__":
    main()

