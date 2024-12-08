from fastapi import FastAPI
from app.controller.user_controller import user_router


def create_public_app() -> FastAPI:
    pub_app = FastAPI()
    return pub_app


routes = [
    {
        "prefix": "",
        "router": user_router,
    }
]

public_app = create_public_app()
for route in routes:
    if route.get("prefix", "") != "":
        public_app.include_router(route.get("router"), prefix=route.get("prefix"))
    public_app.include_router(route.get("router"))


