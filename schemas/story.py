from typing import List, Dict, Optional
from datetime import datetime
from pydantic import BaseModel


class StoryOptionsSchema(BaseModel):
    title: str
    node_id: Optional[int] = None


class StoryNodeBase(BaseModel):
    content: str
    is_ending: bool = False
    is_winnig_ending: bool = False


class CompleteStoryNodeResponse(StoryNodeBase):
    id: int
    options: List[StoryOptionsSchema] = []

    class Config:
        from_attribute = True


class StoryBase(BaseModel):
    title: str
    session_id: Optional[str] = None

    class Config:
        from_attribute = True


class CreateStoryRequest(BaseModel):
    theme: str


class CompleteStoryResponse(StoryNodeBase):
    id: int
    created_at: datetime
    root_node: CompleteStoryNodeResponse
    all_nodes: Dict[int, CompleteStoryNodeResponse]

    class Config:
        from_attributes = True
