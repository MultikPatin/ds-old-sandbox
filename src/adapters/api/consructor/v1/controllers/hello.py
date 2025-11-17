from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

router = APIRouter(route_class=DishkaRoute)


@router.get("/items")
async def get_items() -> dict[str, str]:
    return {"message": "from mounted app constructor v1"}
