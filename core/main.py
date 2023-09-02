from typing import Any

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from config import config
from routers import data, cv
from util.log import setup_logging

app = FastAPI(
    title = config.PROJECT_NAME + " API",
)

logger = setup_logging("core")

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(cv.cv_router)
app.include_router(data.data_router)


@app.get("/", response_class=HTMLResponse)
def index(request: Request) -> Any:
    """Renders the index page for the API.

    Args:
        request: The HTTP request object.

    Returns:
        An HTMLResponse object containing the index page.
    """
    body = (
        "<html>"
        "<body style='padding: 10px;'>"
        "<h1>CV API</h1>"
        "<div>"
        "<a href='/docs'>Interactive API docs</a><br>"
        "<a href='/redoc'>Alternative API docs</a>"
        "</div>"
        "</body>"
        "</html>"
    )
    logger.info(f"Index page requested by {request.client.host}")
    return HTMLResponse(content=body)


if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting API server on {config.API_HOST}:{config.API_PORT}")
    uvicorn.run(app, host=config.API_HOST, port=config.API_PORT)
