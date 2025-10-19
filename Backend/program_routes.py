# program_routes.py - Routes for program submissions
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List
from database import get_db, SessionLocal, User, Program404640723Data, Program404640758Data, Program403640724Data
from models import Program404640723Request, Program404640723Response, Program404640758Request, Program404640758Response, Program403640724Request, Program403640724Response
from auth import get_current_active_user

router = APIRouter()

# Program 404640723 routes
@router.get("/programs/404640723/{user_id}", response_model=Program404640723Response)
async def get_program_404640723_data(user_id: int, current_user: User = Depends(get_current_active_user)):
    """Get program 404640723 data for a specific user"""
    # Users can only access their own data, admins can access all
    if current_user.id != user_id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Access denied")
    
    db = SessionLocal()
    try:
        data = db.query(Program404640723Data).filter(Program404640723Data.user_id == user_id).first()
        if not data:
            raise HTTPException(status_code=404, detail="No data found for this user")
        return data
    finally:
        db.close()

@router.post("/programs/404640723", response_model=dict)
async def save_program_404640723_data(
    form_data: Program404640723Request, 
    current_user: User = Depends(get_current_active_user)
):
    """Save or update program 404640723 data"""
    db = SessionLocal()
    try:
        # Check if user already has data
        existing = db.query(Program404640723Data).filter(
            Program404640723Data.user_id == current_user.id
        ).first()
        
        if existing:
            # Update existing data
            for field, value in form_data.dict().items():
                if hasattr(existing, field):
                    setattr(existing, field, value)
            existing.updated_at = datetime.utcnow()
        else:
            # Create new data
            new_data = Program404640723Data(
                user_id=current_user.id,
                **form_data.dict()
            )
            db.add(new_data)
        
        db.commit()
        return {"message": "Program 404640723 data saved successfully", "success": True}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error saving data: {str(e)}")
    finally:
        db.close()

@router.get("/programs/404640723/all", response_model=List[Program404640723Response])
async def get_all_program_404640723_data(current_user: User = Depends(get_current_active_user)):
    """Get all program 404640723 data - Admin only"""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    db = SessionLocal()
    try:
        data = db.query(Program404640723Data).all()
        return data
    finally:
        db.close()

@router.delete("/programs/404640723/{user_id}")
async def delete_program_404640723_data(user_id: int, current_user: User = Depends(get_current_active_user)):
    """Delete program 404640723 data for a user - Admin only"""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    db = SessionLocal()
    try:
        data = db.query(Program404640723Data).filter(Program404640723Data.user_id == user_id).first()
        if not data:
            raise HTTPException(status_code=404, detail="No data found for this user")
        
        db.delete(data)
        db.commit()
        return {"message": "Program 404640723 data deleted successfully"}
    finally:
        db.close()

# Program 404640758 routes
@router.get("/programs/404640758/{user_id}", response_model=Program404640758Response)
async def get_program_404640758_data(user_id: int, current_user: User = Depends(get_current_active_user)):
    """Get program 404640758 data for a specific user"""
    # Users can only access their own data, admins can access all
    if current_user.id != user_id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Access denied")
    
    db = SessionLocal()
    try:
        data = db.query(Program404640758Data).filter(Program404640758Data.user_id == user_id).first()
        if not data:
            raise HTTPException(status_code=404, detail="No data found for this user")
        return data
    finally:
        db.close()

@router.post("/programs/404640758", response_model=dict)
async def save_program_404640758_data(
    form_data: Program404640758Request, 
    current_user: User = Depends(get_current_active_user)
):
    """Save or update program 404640758 data"""
    db = SessionLocal()
    try:
        # Check if user already has data
        existing = db.query(Program404640758Data).filter(
            Program404640758Data.user_id == current_user.id
        ).first()
        
        if existing:
            # Update existing data
            for field, value in form_data.dict().items():
                if hasattr(existing, field):
                    setattr(existing, field, value)
            existing.updated_at = datetime.utcnow()
        else:
            # Create new data
            new_data = Program404640758Data(
                user_id=current_user.id,
                **form_data.dict()
            )
            db.add(new_data)
        
        db.commit()
        return {"message": "Program 404640758 data saved successfully", "success": True}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error saving data: {str(e)}")
    finally:
        db.close()

@router.get("/programs/404640758/all", response_model=List[Program404640758Response])
async def get_all_program_404640758_data(current_user: User = Depends(get_current_active_user)):
    """Get all program 404640758 data - Admin only"""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    db = SessionLocal()
    try:
        data = db.query(Program404640758Data).all()
        return data
    finally:
        db.close()

@router.delete("/programs/404640758/{user_id}")
async def delete_program_404640758_data(user_id: int, current_user: User = Depends(get_current_active_user)):
    """Delete program 404640758 data for a user - Admin only"""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    db = SessionLocal()
    try:
        data = db.query(Program404640758Data).filter(Program404640758Data.user_id == user_id).first()
        if not data:
            raise HTTPException(status_code=404, detail="No data found for this user")
        
        db.delete(data)
        db.commit()
        return {"message": "Program 404640758 data deleted successfully"}
    finally:
        db.close()

# Program 403640724 routes
@router.get("/programs/403640724/{user_id}", response_model=Program403640724Response)
async def get_program_403640724_data(user_id: int, current_user: User = Depends(get_current_active_user)):
    """Get program 403640724 data for a specific user"""
    # Users can only access their own data, admins can access all
    if current_user.id != user_id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Access denied")
    
    db = SessionLocal()
    try:
        data = db.query(Program403640724Data).filter(Program403640724Data.user_id == user_id).first()
        if not data:
            raise HTTPException(status_code=404, detail="No data found for this user")
        return data
    finally:
        db.close()

@router.post("/programs/403640724", response_model=dict)
async def save_program_403640724_data(
    form_data: Program403640724Request, 
    current_user: User = Depends(get_current_active_user)
):
    """Save or update program 403640724 data"""
    db = SessionLocal()
    try:
        # Check if user already has data
        existing = db.query(Program403640724Data).filter(
            Program403640724Data.user_id == current_user.id
        ).first()
        
        if existing:
            # Update existing data
            for field, value in form_data.dict().items():
                if hasattr(existing, field):
                    setattr(existing, field, value)
            existing.updated_at = datetime.utcnow()
        else:
            # Create new data
            new_data = Program403640724Data(
                user_id=current_user.id,
                **form_data.dict()
            )
            db.add(new_data)
        
        db.commit()
        return {"message": "Program 403640724 data saved successfully", "success": True}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error saving data: {str(e)}")
    finally:
        db.close()

@router.get("/programs/403640724/all", response_model=List[Program403640724Response])
async def get_all_program_403640724_data(current_user: User = Depends(get_current_active_user)):
    """Get all program 403640724 data - Admin only"""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    db = SessionLocal()
    try:
        data = db.query(Program403640724Data).all()
        return data
    finally:
        db.close()

@router.delete("/programs/403640724/{user_id}")
async def delete_program_403640724_data(user_id: int, current_user: User = Depends(get_current_active_user)):
    """Delete program 403640724 data for a user - Admin only"""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    db = SessionLocal()
    try:
        data = db.query(Program403640724Data).filter(Program403640724Data.user_id == user_id).first()
        if not data:
            raise HTTPException(status_code=404, detail="No data found for this user")
        
        db.delete(data)
        db.commit()
        return {"message": "Program 403640724 data deleted successfully"}
    finally:
        db.close()
