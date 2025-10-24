from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class StoryOptionLLM(BaseModel):
    text: str = Field(description="the text of the option shown to the user")
    nextNode: Dict[str, Any] = Field(description="next node content and its options")


class StoryNodeLLM(BaseModel):
    content: str = Field(description="main cintent of the sotry node")
    isEnding: bool = Field(description="Weather this node is an ending node")
    isWinnigEnding: bool = Field(
        description="Wheather this node is a winning ending node"
    )
    options: Optional[List[StoryOptionLLM]] = Field(
        default=None, description="The option for this nodes"
    )


class StoryLLMResponse(BaseModel):
    title: str = Field(description="Title of the story")
    rootNode: StoryNodeLLM = Field(description="The root node of th story")
