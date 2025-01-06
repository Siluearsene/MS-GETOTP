from sqlmodel import Field, SQLModel
import uuid
from datetime import datetime

class Otp(SQLModel, table=True):
    __tablename__ = "otp"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    username: str = Field(nullable=False)
    otp_code: int = Field(nullable=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
