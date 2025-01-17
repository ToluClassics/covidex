import pkg_resources
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

from app.routers import related, search
from app.services.highlighter import Highlighter
from app.services.ranker import Ranker
# from app.services.related_searcher import RelatedSearcher
from app.services.searcher import Searcher
from app.settings import settings

app = FastAPI()

# Set global state for reusable services
if not settings.testing:
    if settings.highlight:
        app.state.highlighter = Highlighter()

    if settings.neural_ranking:
        app.state.ranker = Ranker()

    # if settings.related_search:
    #     app.state.related_searcher = RelatedSearcher()

    app.state.searcher = Searcher()

# Disable CORS in development mode to interact with frontend locally
if settings.development:
    origins = ["http://localhost:3000", "http://localhost"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# API endpoints
app.include_router(search.router, tags=["search"], prefix="/api")
app.include_router(related.router, tags=["related"], prefix="/api")


@app.get("/api/status", status_code=200)
def status():
    return


@app.get("/api/.*", status_code=404, include_in_schema=False)
def invalid_api():
    return None


# Serve static files and client build if not running in development mode
if not settings.development:
    app.mount(
        "/static",
        StaticFiles(directory=pkg_resources.resource_filename(__name__, "static")),
        name="static",
    )

    @app.get("/manifest.json", include_in_schema=False)
    def manifest():
        return FileResponse(
            pkg_resources.resource_filename(__name__, "static/manifest.json")
        )

    @app.get("/favicon.ico", include_in_schema=False)
    def favicon():
        return FileResponse(
            pkg_resources.resource_filename(__name__, "static/favicon.ico")
        )

    @app.get("/logo192.png", include_in_schema=False)
    def favicon():
        return FileResponse(
            pkg_resources.resource_filename(__name__, "static/logo192.png")
        )

    @app.get("/logo512.png", include_in_schema=False)
    def favicon():
        return FileResponse(
            pkg_resources.resource_filename(__name__, "static/logo512.png")
        )

    @app.get("/.*", include_in_schema=False)
    def root():
        return HTMLResponse(
            pkg_resources.resource_string(__name__, "static/index.html")
        )
