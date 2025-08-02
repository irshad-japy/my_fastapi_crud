from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.db import Base, engine, get_db
from app.models import product
from app.routers import product as product_router
from strawberry.fastapi import GraphQLRouter
from app.graphql.schema import schema

app = FastAPI()

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",   # if using Create React App
        "http://localhost:5173"    # if using Vite
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include REST API
app.include_router(product_router.router)

# Create tables
Base.metadata.create_all(bind=engine)

# ✅ Fix context_getter to use async generator
async def get_context(request: Request):
    db = next(get_db())
    return {"db": db}

# ✅ GraphQL router
graphql_app = GraphQLRouter(
    schema,
    graphiql=True,
    context_getter=get_context
)
app.include_router(graphql_app, prefix="/graphql")
