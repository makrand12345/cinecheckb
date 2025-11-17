from fastapi import APIRouter, HTTPException
from typing import List
from models.user import User
from models.movie import Movie
from schemas.movie import MovieOut
from beanie import PydanticObjectId

router = APIRouter(prefix="/watchlist", tags=["Watchlist"])

@router.post("/{user_id}/add/{movie_id}")
async def add_to_watchlist(user_id: str, movie_id: str):
    """
    Add a movie to user's watchlist
    """
    try:
        # Find user by email (user_id is email)
        user = await User.find_one(User.email == user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Validate movie exists
        movie = await Movie.get(PydanticObjectId(movie_id))
        if not movie:
            raise HTTPException(status_code=404, detail="Movie not found")
        
        # Check if already in watchlist
        if PydanticObjectId(movie_id) in user.watchlist:
            return {"message": "Movie already in watchlist", "watchlist": [str(mid) for mid in user.watchlist]}
        
        # Add to watchlist
        user.watchlist.append(PydanticObjectId(movie_id))
        await user.save()
        
        return {"message": "Movie added to watchlist", "watchlist": [str(mid) for mid in user.watchlist]}
        
    except Exception as e:
        print(f"💥 Add to watchlist error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to add to watchlist: {str(e)}")

@router.delete("/{user_id}/remove/{movie_id}")
async def remove_from_watchlist(user_id: str, movie_id: str):
    """
    Remove a movie from user's watchlist
    """
    try:
        user = await User.find_one(User.email == user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        movie_obj_id = PydanticObjectId(movie_id)
        if movie_obj_id not in user.watchlist:
            raise HTTPException(status_code=400, detail="Movie not in watchlist")
        
        user.watchlist.remove(movie_obj_id)
        await user.save()
        
        return {"message": "Movie removed from watchlist", "watchlist": [str(mid) for mid in user.watchlist]}
        
    except Exception as e:
        print(f"💥 Remove from watchlist error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to remove from watchlist: {str(e)}")

@router.get("/{user_id}", response_model=List[MovieOut])
async def get_watchlist(user_id: str):
    """
    Get user's watchlist movies
    """
    try:
        user = await User.find_one(User.email == user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        if not user.watchlist:
            return []
        
        # Fetch all movies in watchlist
        movies = []
        for movie_id in user.watchlist:
            movie = await Movie.get(movie_id)
            if movie and movie.status == "approved":
                movies.append(MovieOut(
                    id=str(movie.id),
                    title=movie.title,
                    description=movie.description,
                    genres=movie.genres,
                    release_date=movie.release_date,
                    duration=movie.duration,
                    poster_url=movie.poster_url,
                    trailer_url=movie.trailer_url,
                    director=movie.director,
                    cast=movie.cast,
                    language=movie.language,
                    country=movie.country,
                    age_rating=movie.age_rating,
                    rating=movie.rating,
                    submitted_by=movie.submitted_by,
                    status=movie.status,
                    featured=movie.featured,
                    created_at=movie.created_at,
                    updated_at=movie.updated_at
                ))
        
        return movies
        
    except Exception as e:
        print(f"💥 Get watchlist error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch watchlist: {str(e)}")

@router.get("/{user_id}/check/{movie_id}")
async def check_watchlist(user_id: str, movie_id: str):
    """
    Check if a movie is in user's watchlist
    """
    try:
        user = await User.find_one(User.email == user_id)
        if not user:
            return {"in_watchlist": False}
        
        movie_obj_id = PydanticObjectId(movie_id)
        return {"in_watchlist": movie_obj_id in user.watchlist}
        
    except Exception as e:
        return {"in_watchlist": False}

