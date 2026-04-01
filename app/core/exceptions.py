class CandidateNotFoundError(Exception):
    def __init__(self, candidate_id: str):
        self.candidate_id = candidate_id
        super().__init__(f"Candidate with ID {candidate_id} not found.")

class InvalidCandidateDataError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
