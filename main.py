from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI


from routers.client.userAuthRouter import router as userAuthRouter

app = FastAPI()

app.include_router(userAuthRouter, prefix="/user", tags=["User Authentication"])

@app.get("/")
async def root():
    return {"message": "Hello World"}
