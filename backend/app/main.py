from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.database import connect_to_mongo, close_mongo_connection
from app.routes import users, credit


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events"""
    # Startup
    await connect_to_mongo()
    yield
    # Shutdown
    await close_mongo_connection()


# Create FastAPI app
app = FastAPI(
    title="Credit Risk Assessment API",
    description="Ethical & Explainable Credit Risk Assessment System for Informal and Gig Workers",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """API root endpoint"""
    return {
        "message": "Credit Risk Assessment API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "register": "POST /register",
            "calculate_score": "POST /calculate-score",
            "get_users": "GET /users",
            "get_user_detail": "GET /user/{id}"
        }
    }


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "database": "connected"
    }


# Register route: POST /register
@app.post("/register", tags=["Registration"])
async def register(user_data: users.UserRegisterRequest):
    """Register a new user - delegates to users router"""
    return await users.register_user(user_data)


# Calculate score route: POST /calculate-score
@app.post("/calculate-score", tags=["Credit Score"])
async def calculate_score(score_data: credit.CalculateScoreRequest):
    """Calculate credit score - delegates to credit router"""
    return await credit.calculate_score(score_data)


# Get all users route: GET /users
@app.get("/users", tags=["Users"])
async def get_users():
    """Get all users - delegates to users router"""
    return await users.get_all_users()


# Get user detail route: GET /user/{id}
@app.get("/user/{user_id}", tags=["Users"])
async def get_user(user_id: str):
    """Get user details - delegates to users router"""
    return await users.get_user_details(user_id)


# Include additional routers (for extensibility)
app.include_router(users.router)
app.include_router(credit.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
