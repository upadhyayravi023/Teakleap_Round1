from typing import List, Optional
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId

from .schemas import CandidateCreate, CandidateResponse, CandidateStatus
from app.core.database import get_db

class CandidateRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db.get_collection("candidates")

    async def get_by_email(self, email: str) -> Optional[CandidateResponse]:
        doc = await self.collection.find_one({"email": email})
        if doc:
            doc["id"] = str(doc.pop("_id"))
            return CandidateResponse(**doc)
        return None

    async def create(self, candidate_in: CandidateCreate) -> CandidateResponse:
        candidate_data = candidate_in.model_dump()
        result = await self.collection.insert_one(candidate_data)
        
        # cleanly enforce ID format for DTO creation mapped from NoSQL
        candidate_data["id"] = str(result.inserted_id)
        if "_id" in candidate_data:
            del candidate_data["_id"]
        return CandidateResponse(**candidate_data)

    async def create_many(self, candidates_in: List[CandidateCreate]) -> List[CandidateResponse]:
        if not candidates_in:
            return []
            
        docs = [cand.model_dump() for cand in candidates_in]
        result = await self.collection.insert_many(docs)
        
        responses = []
        for doc, inserted_id in zip(docs, result.inserted_ids):
            doc["id"] = str(inserted_id)
            if "_id" in doc:
                del doc["_id"]
            responses.append(CandidateResponse(**doc))
        return responses

    async def get_all(self, status: Optional[CandidateStatus] = None) -> List[CandidateResponse]:
        query = {}
        if status:
            query["status"] = status.value
            
        cursor = self.collection.find(query)
        candidates = []
        for doc in await cursor.to_list(length=1000):
            doc["id"] = str(doc.pop("_id"))
            candidates.append(CandidateResponse(**doc))
        return candidates

    async def get_by_id(self, candidate_id: str) -> Optional[CandidateResponse]:
        if not ObjectId.is_valid(candidate_id):
            return None
        doc = await self.collection.find_one({"_id": ObjectId(candidate_id)})
        if doc:
            doc["id"] = str(doc.pop("_id"))
            return CandidateResponse(**doc)
        return None

    async def update_status(self, candidate_id: str, new_status: CandidateStatus) -> Optional[CandidateResponse]:
        if not ObjectId.is_valid(candidate_id):
            return None
        
        result = await self.collection.update_one(
            {"_id": ObjectId(candidate_id)},
            {"$set": {"status": new_status.value}}
        )
        if result.modified_count == 1 or result.matched_count == 1:
            return await self.get_by_id(candidate_id)
        return None

def get_candidate_repository(db: AsyncIOMotorDatabase = Depends(get_db)) -> CandidateRepository:
    return CandidateRepository(db)
