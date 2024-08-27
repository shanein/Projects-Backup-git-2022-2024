from fastapi import FastAPI
from routes import auth, CampaignRoute, terminalRoute, videoRoute, clientRoute
from controllers import *
from fastapi.middleware.cors import CORSMiddleware
from core.adminView import *


# app.mount("/static", StaticFiles(directory="static"), name="static")

origins = [
    "http://localhost",
    "45.147.96.95",
    "https://dev.smartdisplay.tech",
    "https://smartdisplay.tech",
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:3001",
    "http://localhost:5173",
]


app.include_router(auth.router)
app.include_router(videoRoute.router)
app.include_router(CampaignRoute.router)
app.include_router(terminalRoute.router)
app.include_router(clientRoute.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def main():
    print("Starting API on port 8080", flush=True)
    # models.database.Base.metadata.create_all(bind=database.engine)
    print("Database created", flush=True)


if __name__ == "__main__":
    main()
