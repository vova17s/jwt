from dataclasses import dataclass
from typing import Any


@dataclass
class ResultDataClass:
    data: Any | None
    detail: str | None
    status: int

    def __init__(self,
        data: Any | None = None,
        detail: str | None = None,
        status: int = None
    ) -> None:
        self.data = data
        self.detail = detail 
        self.status = status 

    def get_result(self):
        if self.data:
            return {
                "data": self.data,
                "status": self.status
            }

        return None

    def get_error(self):
        if self.detail:
            return {
                "data": self.detail,
                "status": self.status
            }

        return None
    
    def __iter__(self):
        if self.data:
            return iter((self.data, True))
        
        return iter((None, False))