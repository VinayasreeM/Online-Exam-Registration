from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.database import engine, Base
from .api import auth, exams, registrations, payments, admin
from .api.admit_card import router as admit_card_router

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Online Exam Registration System",
    description="A complete exam registration system with student and admin features",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(exams.router)
app.include_router(registrations.router)
app.include_router(payments.router)
app.include_router(admin.router)
app.include_router(admit_card_router)

@app.get("/")
def root():
    return {
        "message": "Online Exam Registration System API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}
