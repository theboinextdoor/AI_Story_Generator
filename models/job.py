from sqlalchemy import Integer, String, DateTime
from sqlalchemy.sql import func
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from db.database import Base


class StoryJob(Base):
    __tablename__ = "story_jobs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    job_id: Mapped[int] = mapped_column(Integer, index=True, unique=True)
    session_id: Mapped[str] = mapped_column(String, index=True)
    theme: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(String)
    story_id: Mapped[int] = mapped_column(Integer, nullable=True)
    error: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    completed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    #! Old way to do that:
    # id = Column(Integer, primary_key=True, index=True)
    # job_id = Column(Integer, index=True, unique=True)
    # session_id = Column(String, index=True)
    # theme = Column(String)
    # status = Column(String)
    # story_id = Column(Integer, nullable=True)
    # error = Column(String, nullable=True)
    # created_at = Column(DateTime(timezone=True), server_default=func.now())
    # completed_at = Column(DateTime(timezone=True), nullable=True)
