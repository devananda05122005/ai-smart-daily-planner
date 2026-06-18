from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from models.request import PlannerRequest
from services.planner import optimize_schedule

app = FastAPI()

# Mount static folder
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def home():
    return FileResponse("static/index.html")

@app.post("/optimize")
def optimize(data: PlannerRequest):
    # .model_dump() replaces outdated .dict() in Pydantic v2
    request_data = data.model_dump()
    
    result = optimize_schedule(
        tasks=request_data["tasks"],
        free_time=request_data["free_time"],
        peak_hours=request_data["peak_hours"],
        fixed_tasks=request_data["fixed_tasks"]
    )
    
    # Catching background errors explicitly to alert UI engine cleanly
    if isinstance(result, dict) and "error" in result:
        return {
            "success": False,
            "error": result["error"]
        }
        
    return {
        "success": True,
        "data": result
    }