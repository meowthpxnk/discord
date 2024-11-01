from fastapi.responses import HTMLResponse

from app import api
from app.constants import DOCS_HTML_PATH
from app.utils.path import read_file


@api.get("/docs", include_in_schema=False)
def documentation() -> HTMLResponse:
    return HTMLResponse(read_file(DOCS_HTML_PATH))
