from fastapi.responses import HTMLResponse

from app import api, base_config
from app.constants import PUBLIC_HTML_PATH
from app.utils.path import read_file


@api.get("/", include_in_schema=False)
def home():
    data = read_file(PUBLIC_HTML_PATH)
    data = data.replace("{{TITLE}}", base_config.config.title)
    data = data.replace("{{DESCRIPTION}}", base_config.config.description)
    return HTMLResponse(data)
