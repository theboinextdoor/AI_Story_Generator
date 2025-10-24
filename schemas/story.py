from typing import List, Dict, Optional
from datetime import datetime
from pydantic import BaseModel


class StoryOptionsSchema(BaseModel):
    title: str
    node_id: Optional[int] = None


class StoryNodeBase(BaseModel):
    content: str
    is_ending: bool = False
    is_winning_ending: bool = False


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


class CompleteStoryResponse(StoryBase):
    id: int
    created_at: datetime
    root_node: CompleteStoryNodeResponse
    all_nodes: Dict[int, CompleteStoryNodeResponse]

    class Config:  # type: ignore[override]
        from_attribute = True


# CompleteStoryResponse
# │
# ├── id (int)
# ├── created_at (datetime)
# ├── content (str)
# ├── is_ending (bool)
# ├── is_winnig_ending (bool)
# ├── root_node → CompleteStoryNodeResponse
# │       ├── id
# │       ├── content
# │       ├── is_ending
# │       ├── is_winnig_ending
# │       └── options → [StoryOptionsSchema]
# │                 ├── title
# │                 └── node_id
# │
# └── all_nodes → Dict[int, CompleteStoryNodeResponse]
#         ├── node_id_1 → { ... same structure ... }
#         ├── node_id_2 → { ... same structure ... }
#         └── node_id_3 → { ... same structure ... }
