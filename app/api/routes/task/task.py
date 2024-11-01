from app.api.routes._base_router import APIRouter


tasks_router = APIRouter(tags=["task"], prefix="/task")


@tasks_router.get("")
def get_task():
    return {"ok": True}
