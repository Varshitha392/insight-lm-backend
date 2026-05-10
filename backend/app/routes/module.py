from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.module import Module
from app.models.user import User
from app.schemas.module_schema import ModuleCreate
from app.utils.auth import get_current_user

router = APIRouter()

@router.post("/modules")
def create_module(
    module: ModuleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    new_module = Module(
        title=module.title,
        user_id=current_user.id
    )

    db.add(new_module)
    db.commit()
    db.refresh(new_module)

    return {
        "message": "Module created successfully",
        "module_id": new_module.id
    }

@router.get("/modules")
def get_modules(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    modules = db.query(Module).filter(
        Module.user_id == current_user.id
    ).all()

    return modules

@router.put("/modules/{module_id}")
def update_module(
    module_id: int,
    module: ModuleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    existing_module = db.query(Module).filter(
        Module.id == module_id,
        Module.user_id == current_user.id
    ).first()

    if not existing_module:
        return {"message": "Module not found"}

    existing_module.title = module.title

    db.commit()

    return {
        "message": "Module updated successfully"
    }

@router.delete("/modules/{module_id}")
def delete_module(
    module_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    existing_module = db.query(Module).filter(
        Module.id == module_id,
        Module.user_id == current_user.id
    ).first()

    if not existing_module:
        return {"message": "Module not found"}

    db.delete(existing_module)

    db.commit()

    return {
        "message": "Module deleted successfully"
    }