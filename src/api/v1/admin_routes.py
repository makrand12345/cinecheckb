from fastapi import APIRouter, HTTPException
from typing import List
from models.movie import Movie
from schemas.movie import MovieOut
from beanie import PydanticObjectId

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/")
async def admin_dashboard():
    return {"message": "Welcome Admin"}

# Admin movie management routes - REMOVE current_user=Depends(admin_required)
@router.get("/movies/pending", response_model=List[MovieOut])
async def get_pending_movies():
    """Get all pending movies for admin approval"""
    try:
        movies = await Movie.find(Movie.status == "pending").to_list()
        movie_list = []
        for m in movies:
            movie_list.append(
                MovieOut(
                    id=str(m.id),
                    title=m.title,
                    description=m.description,
                    genres=m.genres,
                    release_date=m.release_date,
                    duration=m.duration,
                    poster_url=m.poster_url,
                    trailer_url=m.trailer_url,
                    director=m.director,
                    cast=m.cast,
                    language=m.language,
                    country=m.country,
                    age_rating=m.age_rating,
                    rating=m.rating,
                    submitted_by=m.submitted_by,
                    status=m.status,
                    featured=m.featured,
                    created_at=m.created_at,
                    updated_at=m.updated_at
                )
            )
        return movie_list
    except Exception as e:
        print(f"💥 Pending movies error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch pending movies: {str(e)}")

@router.post("/movies/{movie_id}/approve")
async def approve_movie(movie_id: str):
    """Approve a pending movie"""
    try:
        movie = await Movie.get(PydanticObjectId(movie_id))
        if not movie:
            raise HTTPException(status_code=404, detail="Movie not found")
        
        movie.status = "approved"
        await movie.save()
        
        return {"message": "Movie approved successfully"}
    except Exception as e:
        print(f"💥 Approve movie error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to approve movie: {str(e)}")

@router.post("/movies/{movie_id}/reject")
async def reject_movie(movie_id: str):
    """Reject a pending movie"""
    try:
        movie = await Movie.get(PydanticObjectId(movie_id))
        if not movie:
            raise HTTPException(status_code=404, detail="Movie not found")
        
        movie.status = "rejected"
        await movie.save()
        
        return {"message": "Movie rejected successfully"}
    except Exception as e:
        print(f"💥 Reject movie error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to reject movie: {str(e)}")