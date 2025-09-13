from api.routers    import users, games, auctions
from fastapi        import FastAPI

app=FastAPI()

app.include_router(games.router)
app.include_router(auctions.router)
app.include_router(users.router)
