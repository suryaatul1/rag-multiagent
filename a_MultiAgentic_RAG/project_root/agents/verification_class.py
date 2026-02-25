from typing import List

from pydantic import Field, BaseModel


class VerificationClass(BaseModel):
    Supported : str
    Unsupported_Claims : List[str] = Field(default_factory=list)
    Contradictions : List[str] = Field(default_factory=list)
    Relevant : str
    Additional_Details : List[str] = Field(default_factory=list)
