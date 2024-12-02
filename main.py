from dotenv import load_dotenv

from middlewares.authMiddlewares import protected_route

load_dotenv()

from fastapi.security import OAuth2PasswordBearer
from fastapi.openapi.utils import get_openapi

from Database.services.userServices import UserServiceDep
from core.jwtHelper import JwtHelper, JwtHelperDep


from fastapi import FastAPI

from routers.client.userAuthRouter import router as userAuthRouter
from routers.client.postRouter import router as postRouter
from routers.admin.adminAuthRouter import router as adminAuthRouter
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Custom OpenAPI schema function
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Your API",
        version="1.0.0",
        description="This is a custom OpenAPI schema with Bearer token authentication",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    openapi_schema["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


# Set the custom OpenAPI schema
app.openapi = custom_openapi


app.include_router(userAuthRouter, prefix="/auth", tags=["User Authentication"])
app.include_router(postRouter, prefix="/post", tags=["Posts"])

app.include_router(adminAuthRouter, prefix="/admin/auth", tags=["Admin Authentication"])


@app.get("/")
async def root(authUser: dict = protected_route()):
    return {"message": "Hello World", "user": authUser}
