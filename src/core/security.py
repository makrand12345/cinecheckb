from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer
from src.models.user import User

security = HTTPBearer()

async def admin_required(token: str = Depends(security)):
    # TEMPORARY: Allow all access for testing
    # In production, you'll need proper JWT validation
    user = await User.find_one({"role": "admin"})
    if not user:
        # For now, just get any user to test the functionality
        user = await User.find_one()
        if not user:
            raise HTTPException(status_code=403, detail="No users found")
    return user

# OR even simpler - remove auth temporarily:
async def admin_required():
    # Bypass authentication for testing
    user = await User.find_one()
    if not user:
        raise HTTPException(status_code=403, detail="No users found")
    return user