from fastapi import APIRouter, HTTPException
from typing import List
from models.review import Review
from schemas.review import ReviewCreate, ReviewOut
from models.movie import Movie
from beanie import PydanticObjectId
from datetime import datetime

router = APIRouter(prefix="/reviews", tags=["Reviews"])

@router.post("/", response_model=ReviewOut)
async def create_review(review_data: ReviewCreate, user_id: str = "anonymous", username: str = "Anonymous"):
    """
    Create a new review for a movie
    """
    try:
        # Validate movie exists
        movie = await Movie.get(PydanticObjectId(review_data.movie_id))
        if not movie:
            raise HTTPException(status_code=404, detail="Movie not found")
        
        # Validate rating
        if review_data.rating < 1 or review_data.rating > 5:
            raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")
        
        # Check if user already reviewed this movie
        existing_review = await Review.find_one(
            Review.movie_id == PydanticObjectId(review_data.movie_id),
            Review.user_id == user_id
        )
        
        if existing_review:
            # Update existing review
            existing_review.rating = review_data.rating
            existing_review.review_text = review_data.review_text
            existing_review.updated_at = datetime.utcnow()
            await existing_review.save()
            
            # Recalculate movie rating
            await update_movie_rating(review_data.movie_id)
            
            return ReviewOut(
                id=str(existing_review.id),
                movie_id=str(existing_review.movie_id),
                user_id=existing_review.user_id,
                username=existing_review.username,
                rating=existing_review.rating,
                review_text=existing_review.review_text,
                created_at=existing_review.created_at,
                updated_at=existing_review.updated_at
            )
        
        # Create new review
        review = Review(
            movie_id=PydanticObjectId(review_data.movie_id),
            user_id=user_id,
            username=username,
            rating=review_data.rating,
            review_text=review_data.review_text
        )
        await review.insert()
        
        # Update movie average rating
        await update_movie_rating(review_data.movie_id)
        
        return ReviewOut(
            id=str(review.id),
            movie_id=str(review.movie_id),
            user_id=review.user_id,
            username=review.username,
            rating=review.rating,
            review_text=review.review_text,
            created_at=review.created_at,
            updated_at=review.updated_at
        )
        
    except Exception as e:
        print(f"💥 Create review error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create review: {str(e)}")

@router.get("/movie/{movie_id}", response_model=List[ReviewOut])
async def get_movie_reviews(movie_id: str):
    """
    Get all reviews for a specific movie
    """
    try:
        reviews = await Review.find(Review.movie_id == PydanticObjectId(movie_id)).sort(-Review.created_at).to_list()
        
        return [
            ReviewOut(
                id=str(r.id),
                movie_id=str(r.movie_id),
                user_id=r.user_id,
                username=r.username,
                rating=r.rating,
                review_text=r.review_text,
                created_at=r.created_at,
                updated_at=r.updated_at
            ) for r in reviews
        ]
    except Exception as e:
        print(f"💥 Get reviews error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch reviews: {str(e)}")

@router.get("/user/{user_id}", response_model=List[ReviewOut])
async def get_user_reviews(user_id: str):
    """
    Get all reviews by a specific user
    """
    try:
        reviews = await Review.find(Review.user_id == user_id).sort(-Review.created_at).to_list()
        
        return [
            ReviewOut(
                id=str(r.id),
                movie_id=str(r.movie_id),
                user_id=r.user_id,
                username=r.username,
                rating=r.rating,
                review_text=r.review_text,
                created_at=r.created_at,
                updated_at=r.updated_at
            ) for r in reviews
        ]
    except Exception as e:
        print(f"💥 Get user reviews error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch user reviews: {str(e)}")

@router.delete("/{review_id}")
async def delete_review(review_id: str, user_id: str = "anonymous"):
    """
    Delete a review (only by the user who created it)
    """
    try:
        review = await Review.get(PydanticObjectId(review_id))
        if not review:
            raise HTTPException(status_code=404, detail="Review not found")
        
        if review.user_id != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to delete this review")
        
        movie_id = str(review.movie_id)
        await review.delete()
        
        # Recalculate movie rating
        await update_movie_rating(movie_id)
        
        return {"message": "Review deleted successfully"}
    except Exception as e:
        print(f"💥 Delete review error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to delete review: {str(e)}")

async def update_movie_rating(movie_id: str):
    """
    Recalculate and update the average rating for a movie
    """
    try:
        reviews = await Review.find(Review.movie_id == PydanticObjectId(movie_id)).to_list()
        
        if reviews:
            avg_rating = sum(r.rating for r in reviews) / len(reviews)
            movie = await Movie.get(PydanticObjectId(movie_id))
            if movie:
                movie.rating = round(avg_rating, 1)
                await movie.save()
        else:
            # No reviews, set rating to None
            movie = await Movie.get(PydanticObjectId(movie_id))
            if movie:
                movie.rating = None
                await movie.save()
    except Exception as e:
        print(f"💥 Update movie rating error: {e}")

