from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError

from sqlalchemy import inspect

from app.database.database import Base, engine

# MODELS (ensure all imports are correct)
from app.models.user import User
from app.models.favorite import Favorite
from app.models.review import Review
from app.models.search_history import SearchHistory
from app.models.view_history import ViewHistory
from app.models.user_preference import UserPreference

# ROUTES
from app.routes.auth import router as auth_router
from app.routes.movies import router as movies_router
from app.routes.favorites import router as favorites_router
from app.routes.reviews import router as reviews_router
from app.routes.view_history import router as view_history_router
from app.routes.dashboard import router as dashboard_router
from app.routes.recommendations import router as recommendation_router

from app.routes import history
from app.routes import preferences   # ✅ FIXED (correct import)

from app.utils.exceptions import validation_exception_handler

from fastapi.middleware.cors import CORSMiddleware


# =========================
# CREATE TABLES (DEBUG)
# =========================
print("TABLES BEFORE:")
print(inspect(engine).get_table_names())

Base.metadata.create_all(bind=engine)

print("TABLES AFTER:")
print(inspect(engine).get_table_names())


# =========================
# FASTAPI APP (ONLY ONCE)
# =========================
app = FastAPI(
    title="Movie Recommendation API",
    version="1.0.0"
)

# =========================
# CORS
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# EXCEPTION HANDLER
# =========================
app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler
)

# =========================
# ROUTES
# =========================
app.include_router(auth_router)
app.include_router(movies_router)
app.include_router(favorites_router)
app.include_router(reviews_router)
app.include_router(history.router)
app.include_router(view_history_router)
app.include_router(dashboard_router)
app.include_router(recommendation_router)
app.include_router(preferences.router)

# =========================
# ROOT ENDPOINT
# =========================
@app.get("/")
def home():
    return {
        "message": "Movie API Running"
    }