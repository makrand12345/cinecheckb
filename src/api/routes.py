from fastapi import APIRouter
from api.v1 import movie_routes, auth_routes, user_routes, admin_routes, review_routes, watchlist_routes

router = APIRouter()

# Mount all routes WITHOUT additional prefix
router.include_router(auth_routes.router)
router.include_router(movie_routes.router) 
router.include_router(user_routes.router)
router.include_router(admin_routes.router)
router.include_router(review_routes.router)
router.include_router(watchlist_routes.router)