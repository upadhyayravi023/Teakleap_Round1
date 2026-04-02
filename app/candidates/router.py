from typing import List, Optional, Union
from fastapi import APIRouter, Depends, status
from .schemas import CandidateCreate, CandidateResponse, CandidateStatusUpdate, CandidateStatus
from .service import CandidateService, get_candidate_service

router = APIRouter(prefix="/candidates", tags=["Candidates"])

@router.post("", response_model=Union[CandidateResponse, List[CandidateResponse]], status_code=status.HTTP_201_CREATED)
async def create_candidate(
    candidate: Union[CandidateCreate, List[CandidateCreate]],
    service: CandidateService = Depends(get_candidate_service)
):
    return await service.create_candidates(candidate)

@router.get("", response_model=List[CandidateResponse], status_code=status.HTTP_200_OK)
async def get_candidates(
    status: Optional[CandidateStatus] = None,
    service: CandidateService = Depends(get_candidate_service)
):
    return await service.get_all_candidates(status=status)

@router.put("/{id}/status", response_model=CandidateResponse, status_code=status.HTTP_200_OK)
async def update_candidate_status(
    # Refactored for BSON ObjectId
    id: str,
    status_update: CandidateStatusUpdate,
    service: CandidateService = Depends(get_candidate_service)
):
    return await service.update_candidate_status(id, status_update)
