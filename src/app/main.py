# %%
from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
from pathlib import Path
import sys
CODE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(CODE_DIR))

from app.cron.job import main
from app.routers import endpoints
import uvicorn

# %%
app = FastAPI()
app.include_router(endpoints.router)

scheduler = BackgroundScheduler()
scheduler.add_job(main, "interval", minutes=60)
scheduler.start()

@app.on_event("shutdown")
def shutdown_event():
    scheduler.shutdown()

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="localhost", port=8000, reload=True)