from pathlib import Path
import shutil

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware

from database import create_tables
from schemas import (
    CitizenRegister,
    LoginData,
    OfficerLogin,
    AdminLogin,
    ComplaintUpdate,
)
from auth import (
    register_citizen,
    login_citizen,
    login_officer,
    login_admin,
)
from complaint import (
    create_complaint,
    get_user_complaints,
    get_complaint,
)
from officer import get_officer_complaints, update_complaint
from admin import get_all_complaints, get_city_statistics


app = FastAPI(title="CivicPulse AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


UPLOAD_DIR = Path(__file__).resolve().parent / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@app.on_event("startup")
def startup():
    create_tables()


@app.get("/")
def home():
    return {"message": "CivicPulse AI API is running"}


@app.post("/auth/register")
def register(data: CitizenRegister):
    try:
        return register_citizen(
            data.name,
            data.email,
            data.mobile,
            data.password,
        )
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Email already registered",
        )


@app.post("/auth/citizen-login")
def citizen_login(data: LoginData):
    result = login_citizen(data.email, data.password)

    if not result:
        raise HTTPException(
            status_code=401,
            detail="Invalid citizen credentials",
        )

    return result


@app.post("/auth/officer-login")
def officer_login(data: OfficerLogin):
    result = login_officer(data.officer_id, data.password)

    if not result:
        raise HTTPException(
            status_code=401,
            detail="Invalid officer credentials",
        )

    return result


@app.post("/auth/admin-login")
def admin_login(data: AdminLogin):
    result = login_admin(data.admin_id, data.password)

    if not result:
        raise HTTPException(
            status_code=401,
            detail="Invalid admin credentials",
        )

    return result


@app.post("/complaints")
async def create_complaint_api(
    user_id: int = Form(...),
    description: str = Form(...),
    location: str = Form(...),
    category: str = Form(...),
    image: UploadFile | None = File(default=None),
):
    image_path = ""

    if image and image.filename:
        safe_filename = Path(image.filename).name
        file_path = UPLOAD_DIR / safe_filename

        with file_path.open("wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

        image_path = str(file_path)

    return create_complaint(
        user_id=user_id,
        description=description,
        location=location,
        category=category,
        image_path=image_path,
    )


@app.get("/complaints/user/{user_id}")
def user_complaints(user_id: int):
    return get_user_complaints(user_id)


@app.get("/complaints/{complaint_id}")
def complaint_detail(complaint_id: int):
    result = get_complaint(complaint_id)

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Complaint not found",
        )

    return result


@app.get("/officer/complaints/{department}")
def officer_complaints(department: str):
    return get_officer_complaints(department)


@app.put("/complaints/{complaint_id}")
def update(complaint_id: int, data: ComplaintUpdate):
    updated = update_complaint(
        complaint_id,
        data.officer_id,
        data.status,
        data.remark,
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Complaint not found",
        )

    return {"success": True}


@app.get("/admin/complaints")
def admin_complaints():
    return get_all_complaints()


@app.get("/admin/statistics")
def statistics():
    return get_city_statistics()