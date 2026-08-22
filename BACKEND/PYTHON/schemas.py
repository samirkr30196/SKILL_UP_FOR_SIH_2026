from pydantic import BaseModel

class CitizenRegister(BaseModel):
    name: str
    email: str
    mobile: str
    password: str

class LoginData(BaseModel):
    email: str
    password: str

class OfficerLogin(BaseModel):
    officer_id: str
    password: str

class AdminLogin(BaseModel):
    admin_id: str
    password: str

class ComplaintCreate(BaseModel):
    user_id: int
    description: str
    location: str
    category: str

class ComplaintUpdate(BaseModel):
    officer_id: str
    status: str
    remark: str = ""