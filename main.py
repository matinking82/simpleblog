from dotenv import load_dotenv

from core.jwtHelper import JwtHelper, JwtHelperDep

load_dotenv()

from fastapi import FastAPI

from middlewares.authMiddlewares import AuthMiddleware
from routers.client.userAuthRouter import router as userAuthRouter
from routers.admin.adminAuthRouter import router as adminAuthRouter
from core.jwtHelper import JwtHelperDep
from fastapi import Request

app = FastAPI()

app.add_middleware(AuthMiddleware, jwtHelper=JwtHelper())


app.include_router(userAuthRouter, prefix="/auth", tags=["User Authentication"])
app.include_router(adminAuthRouter, prefix="/admin/auth", tags=["Admin Authentication"])


@app.get("/")
async def root(request: Request):
    return {"message": "Hello World", "user": request.state}
