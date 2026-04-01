from enum import Enum
from pydantic import BaseModel, EmailStr

class CandidateStatus(str, Enum):
    applied = "applied"
    interview = "interview"
    selected = "selected"
    rejected = "rejected"

class CandidateBase(BaseModel):
    name: str
    email: EmailStr
    skill: str
    status: CandidateStatus

class CandidateCreate(CandidateBase):
    pass

class CandidateResponse(CandidateBase):
    id: str

class CandidateStatusUpdate(BaseModel):
    status: CandidateStatus
