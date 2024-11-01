from fastapi.responses import FileResponse

from app import api
from app.constants import FAVICON_PATH


@api.get("/favicon.ico", include_in_schema=False)
def favicon() -> FileResponse:
    return FileResponse(FAVICON_PATH)
