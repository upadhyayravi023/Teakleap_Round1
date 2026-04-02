from typing import List, Optional, Union
from fastapi import Depends
from .schemas import CandidateCreate, CandidateResponse, CandidateStatusUpdate, CandidateStatus
from .repository import CandidateRepository, get_candidate_repository
from app.core.exceptions import CandidateNotFoundError, DuplicateEmailError, InvalidCandidateDataError

class CandidateService:
    def __init__(self, repository: CandidateRepository = Depends(get_candidate_repository)):
        self.repository = repository

    async def create_candidates(self, candidates_in: Union[CandidateCreate, List[CandidateCreate]]) -> Union[CandidateResponse, List[CandidateResponse]]:
        is_list = isinstance(candidates_in, list)
        candidates_list = candidates_in if is_list else [candidates_in]

        # Check internally for duplicates WITHIN the bulk payload payload 
        emails = [c.email for c in candidates_list]
        if len(emails) != len(set(emails)):
            raise InvalidCandidateDataError("Duplicate emails found inside the bulk payload array.")

        # Check externally against the Database to strictly avoid duplicates
        for cand in candidates_list:
            existing_candidate = await self.repository.get_by_email(cand.email)
            if existing_candidate:
                raise DuplicateEmailError(email=cand.email)
                
        if len(candidates_list) == 1:
            result = await self.repository.create(candidates_list[0])
            return [result] if is_list else result
            
        results = await self.repository.create_many(candidates_list)
        return results

    async def get_all_candidates(self, status: Optional[CandidateStatus] = None) -> List[CandidateResponse]:
        return await self.repository.get_all(status)

    async def update_candidate_status(self, candidate_id: str, status_update: CandidateStatusUpdate) -> CandidateResponse:
        updated_candidate = await self.repository.update_status(candidate_id, status_update.status)
        if not updated_candidate:
            raise CandidateNotFoundError(candidate_id=candidate_id)
        return updated_candidate

def get_candidate_service(service: CandidateService = Depends(CandidateService)) -> CandidateService:
    return service
