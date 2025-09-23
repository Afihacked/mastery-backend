from fastapi import FastAPI
from app.routers import extract, convert

app = FastAPI(
    title="MasterY Backend",
    description="Backend untuk aplikasi YouTube downloader",
    version="1.0.0"
)

# Include routers
app.include_router(extract.router, prefix="/api", tags=["Extract"])
app.include_router(convert.router, prefix="/api", tags=["Convert"])

@app.get("/")
def root():
    return {"message": "MasterY Backend is running 🚀"}
