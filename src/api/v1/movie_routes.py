from fastapi import APIRouter, HTTPException, Depends
from typing import List
from models.movie import Movie
from schemas.movie import MovieOut
from pydantic import BaseModel
from typing import List, Optional
from beanie import PydanticObjectId
from core.security import admin_required
from datetime import datetime, timezone


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

def _to_epoch(dt: datetime) -> float:
    """
    Convert datetime to a UTC epoch float. Handles both naive and tz-aware datetimes.
    """
    if dt is None:
        return 0.0
    if dt.tzinfo is None:
        # assume naive datetimes are UTC (adjust if your app uses local time)
        dt = dt.replace(tzinfo=timezone.utc)
    else:
        dt = dt.astimezone(timezone.utc)
    return dt.timestamp()

def _parse_datetime(val):
    """
    Return a timezone-aware datetime (UTC) from datetime or ISO string.
    Returns None if it cannot be parsed.
    """
    if val is None:
        return None
    if isinstance(val, datetime):
        dt = val
    elif isinstance(val, str):
        try:
            # try ISO format first
            dt = datetime.fromisoformat(val)
        except Exception:
            # fallback: attempt basic YYYY-MM-DD parse
            try:
                dt = datetime.strptime(val.split("T")[0], "%Y-%m-%d")
            except Exception:
                return None
    else:
        return None

    # make timezone-aware in UTC
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    else:
        dt = dt.astimezone(timezone.utc)
    return dt

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
async def get_all_movies(
    search: Optional[str] = None,
    genre: Optional[str] = None,
    year: Optional[int] = None,
    min_rating: Optional[float] = None,
    sort_by: Optional[str] = "created_at",  # created_at, rating, title
    featured: Optional[bool] = None
):
    """
    Fetch all approved movies with optional filtering and sorting
    """
    try:
        # Build query
        query = {"status": "approved"}
        if featured is not None:
            query["featured"] = featured
        
        movies_query = Movie.find(query)
        
        # Apply filters
        movies = await movies_query.to_list()
        
        # Filter in memory (can be optimized with MongoDB aggregation)
        filtered_movies = []
        for m in movies:
            # Search filter
            if search:
                search_lower = search.lower()
                if (search_lower not in m.title.lower() and 
                    search_lower not in m.description.lower() and
                    search_lower not in (m.director or "").lower()):
                    continue
            
            # Genre filter
            if genre and genre not in m.genres:
                continue
            
            # Year filter
            if year and m.release_date:
                try:
                    movie_year = int(m.release_date.split("-")[0])
                    if movie_year != year:
                        continue
                except:
                    pass
            
            # Rating filter
            if min_rating is not None:
                if m.rating is None or m.rating < min_rating:
                    continue
            
            filtered_movies.append(m)
        
        # Normalize datetimes to avoid naive/aware comparison errors
        for m in filtered_movies:
            try:
                m.created_at = _parse_datetime(getattr(m, "created_at", None))
                m.updated_at = _parse_datetime(getattr(m, "updated_at", None))
            except Exception:
                # keep original if normalization fails
                pass
        
        # Sort
        if sort_by == "rating":
            filtered_movies.sort(key=lambda x: x.rating if x.rating else 0, reverse=True)
        elif sort_by == "title":
            filtered_movies.sort(key=lambda x: x.title.lower())
        else:  # created_at (default)
            filtered_movies.sort(key=lambda x: _to_epoch(getattr(x, "created_at", None)), reverse=True)
        
        # Convert to MovieOut
        movie_list = []
        for m in filtered_movies:
            movie_list.append(MovieOut(
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
            ))
        return movie_list
        
    except Exception as e:
        print(f"💥 Get movies error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch movies: {str(e)}")

@router.get("/featured", response_model=List[MovieOut])
async def get_featured_movies():
    """
    Get all featured movies
    """
    try:
        movies = await Movie.find(Movie.status == "approved", Movie.featured == True).sort(-Movie.rating).to_list()
        
        movie_list = []
        for m in movies:
            movie_list.append(MovieOut(
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
            ))
        return movie_list
    except Exception as e:
        print(f"💥 Get featured movies error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch featured movies: {str(e)}")
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

@router.post("/admin/{movie_id}/feature")
async def toggle_featured(movie_id: str):
    """Toggle featured status of a movie"""
    try:
        movie = await Movie.get(PydanticObjectId(movie_id))
        if not movie:
            raise HTTPException(status_code=404, detail="Movie not found")
        
        movie.featured = not movie.featured
        await movie.save()
        
        return {"message": f"Movie {'featured' if movie.featured else 'unfeatured'} successfully", "featured": movie.featured}
    except Exception as e:
        print(f"💥 Toggle featured error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to toggle featured: {str(e)}")

