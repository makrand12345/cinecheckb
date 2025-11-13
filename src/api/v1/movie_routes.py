from fastapi import APIRouter, HTTPException, Depends
from typing import List
from models.movie import Movie
from schemas.movie import MovieOut
from pydantic import BaseModel
from typing import List, Optional
from beanie import PydanticObjectId
from core.security import admin_required


router = APIRouter(prefix="/movies", tags=["Movies"])

class CreateMovieRequest(BaseModel):
    title: str
    description: str
    genres: List[str]
    release_date: Optional[str] = None
    duration: Optional[int] = None
    poster_url: Optional[str] = None
    trailer_url: Optional[str] = None
    director: Optional[str] = None
    cast: List[dict] = []
    language: Optional[str] = None
    country: Optional[str] = None
    age_rating: Optional[str] = None
    submitted_by: Optional[str] = None

@router.post("/test-movie")
async def create_test_movie():
    """Create a test movie to verify the database connection"""
    try:
        test_movie = Movie(
            title="The Shawshank Redemption",
            description="Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.",
            genres=["Drama"],
            release_date="1994-09-23",
            duration=142,
            director="Frank Darabont",
            cast=[{"name": "Tim Robbins", "role": "Andy Dufresne"}, {"name": "Morgan Freeman", "role": "Ellis Redding"}],
            status="approved"
        )
        await test_movie.insert()
        return {"message": "Test movie created successfully", "movie_id": str(test_movie.id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create test movie: {str(e)}")

@router.post("/", response_model=MovieOut)
async def create_movie(movie_data: CreateMovieRequest):
    """
    Create a new movie submission
    """
    try:
        # Create new movie
        movie = Movie(
            **movie_data.dict(),
            status="pending"  # New movies start as pending
        )
        
        await movie.insert()
        
        # Return the created movie
        return MovieOut(
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
        )
        
    except Exception as e:
        print(f"💥 Create movie error: {e}")
        raise HTTPException(status_code=400, detail=f"Failed to create movie: {str(e)}")

@router.get("/", response_model=List[MovieOut])
async def get_all_movies():
    """
    Fetch all approved movies from MongoDB.
    """
    try:
        print("DEBUG: Starting database query")
        movies = await Movie.find(Movie.status == "approved").to_list()
        print(f"DEBUG: Found {len(movies)} movies")
        # ... rest of function
    except Exception as e:
        print(f"💥 REAL Movies DB error: {e}")
        import traceback
        print(f"💥 FULL TRACEBACK: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Movies DB error: {str(e)}")

@router.post("/test-movie")
async def create_test_movie():
    """Create a test movie to verify the database connection"""
    try:
        test_movie = Movie(
            title="The Shawshank Redemption",
            description="Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.",
            genres=["Drama"],
            release_date="1994-09-23",
            duration=142,
            director="Frank Darabont",
            cast=[{"name": "Tim Robbins", "role": "Andy Dufresne"}, {"name": "Morgan Freeman", "role": "Ellis Redding"}],
            status="approved"
        )
        await test_movie.insert()
        return {"message": "Test movie created successfully", "movie_id": str(test_movie.id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create test movie: {str(e)}")

@router.get("/{movie_id}", response_model=MovieOut)
async def get_movie_details(movie_id: str):
    """
    Fetch a single movie by ID
    """
    try:
        movie = await Movie.get(PydanticObjectId(movie_id))
        if not movie:
            raise HTTPException(status_code=404, detail="Movie not found")
        return MovieOut(
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
        )
    except Exception as e:
        print(f"💥 Movie detail error: {e}")
        raise HTTPException(status_code=500, detail=f"Movie detail error: {str(e)}")

@router.get("/debug/all")
async def debug_all_movies():
    """Get ALL movies regardless of status"""
    try:
        movies = await Movie.find_all().to_list()
        return {
            "total_movies": len(movies),
            "movies": [
                {
                    "id": str(m.id),
                    "title": m.title,
                    "status": m.status
                } for m in movies
            ]
        }
    except Exception as e:
        return {"error": str(e)}
    
    # Admin routes for movie management
@router.get("/admin/pending", response_model=List[MovieOut])
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

@router.post("/admin/{movie_id}/approve")
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

@router.post("/admin/{movie_id}/reject")
async def reject_movie(movie_id: str):
    """Reject a pending movie"""
    try:
        movie = await Movie.get(PydanticObjectId(movie_id))
        if not movie:
            raise HTTPException(status_code=404, detail="Movie not found")
        
        # You can either delete the movie or mark it as rejected
        movie.status = "rejected"
        await movie.save()
        
        return {"message": "Movie rejected successfully"}
    except Exception as e:
        print(f"💥 Reject movie error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to reject movie: {str(e)}")
    
    