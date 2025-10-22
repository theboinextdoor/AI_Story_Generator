from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from typing import Any, Dict

#! Initializing the FastAPI instance
app = FastAPI(
    title="AI Generative Story Telling Application",
    description="API to generate cool stories",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)


#! Initializing the cors middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],  # ? [GET, POST, DELETE, PUT, UPDATE etc.]
    allow_headers=["*"],  # ? Additional informations
)


@app.get("/name")
async def greetings(name: str) -> Dict[str, Any]:
    return {"message": f"Hellow {name}", "status": 200}


# ! NOTE : Run code only when the file is executed directly
# ! i.e ->  python main.py
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
