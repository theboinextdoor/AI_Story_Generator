from sqlalchemy.orm import Session
from core.config import settings

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

from core.prompts import STORY_PROMPT
from models.story import Story, StoryNode
from core.models import StoryLLMResponse, StoryNodeLLM


class StoryGenerator:

    @classmethod
    def get_llm(cls):
        return ChatOpenAI(model="gpt-4-turbo")

    @classmethod
    def generate_story(
        cls, db: Session, session_id: str, theme: str = "fantasy"
    ) -> Story:
        llm = cls.get_llm()
        story_parser = PydanticOutputParser(pydantic_object=StoryLLMResponse)

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", STORY_PROMPT),
                ("human", f"Create the story with this theme : {theme}"),
            ]
        ).partial(format_instruction=story_parser.get_format_instructions())

        raw_response = llm.invoke(prompt.invoke({}))

        response_text = raw_response
        if hasattr(raw_response, "content"):
            response_text = raw_response.content

        story_structure = story_parser.parse(response_text)

        story_db = Story(title=story_structure.title, session_id=session_id)
        db.add(story_db)
        db.flush()

        root_node_data = story_structure.rootNode

        if isinstance(root_node_data, dict):
            root_node_data = StoryNodeLLM.model_validate(root_node_data)

        # TODO : process data
        cls._process_story_node(db, story_db.id, root_node_data, is_root=True)

        db.commit()
        return story_db

    @classmethod
    def _process_story_node(
        cls, db: Session, story_id: int, node_data: StoryNodeLLM, is_root: bool = False
    ) -> StoryNode | None:

        node = StoryNode(
            story_id=story_id,
            content=(
                node_data.content
                if hasattr(node_data, "content")
                else node_data["content"]
            ),
            is_root=is_root,
            is_ending=(
                node_data.isEnding
                if hasattr(node_data, "isEnding")
                else node_data["isEnding"]
            ),
            is_winning_ending=(
                node_data.isWinnigEnding
                if hasattr(node_data, "isWinningEnding")
                else node_data["isWinningEnding"]
            ),
            options=[],
        )

        db.add(node)
        db.flush()

        if not node.is_ending and (hasattr(node_data, "options") and node_data.options):
            options_list = []

            for option_data in node_data.options:
                next_node = option_data.nextNode

                if isinstance(next_node, dict):
                    next_node = StoryNodeLLM.model_validate(next_node)

                child_node = cls._process_story_node(db, story_id, next_node, False)

                options_list.append(
                    {"text": option_data.text, "node_id": child_node.id}
                )

            node.options = options_list

        db.flush()
        return node
