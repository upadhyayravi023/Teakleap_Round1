from typing import List, Optional
from fastapi import Depends
from .schemas import CandidateCreate, CandidateResponse, CandidateStatusUpdate, CandidateStatus
from .repository import CandidateRepository, get_candidate_repository
from app.core.exceptions import CandidateNotFoundError

class CandidateService:
    def __init__(self, repository: CandidateRepository = Depends(get_candidate_repository)):
        self.repository = repository

    async def create_candidate(self, candidate_in: CandidateCreate) -> CandidateResponse:
        return await self.repository.create(candidate_in)

    async def get_all_candidates(self, status: Optional[CandidateStatus] = None) -> List[CandidateResponse]:
        return await self.repository.get_all(status)

    async def update_candidate_status(self, candidate_id: str, status_update: CandidateStatusUpdate) -> CandidateResponse:
        updated_candidate = await self.repository.update_status(candidate_id, status_update.status)
        if not updated_candidate:
            raise CandidateNotFoundError(candidate_id=candidate_id)
        return updated_candidate

def get_candidate_service(service: CandidateService = Depends(CandidateService)) -> CandidateService:
    return service
