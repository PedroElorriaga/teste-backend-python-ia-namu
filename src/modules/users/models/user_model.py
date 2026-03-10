from sqlalchemy import Column, DateTime, Enum, Integer, String, func
from sqlalchemy.dialects.postgresql import ARRAY
from src.database.postgres_setting import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    age = Column(Integer, nullable=False)
    goals = Column(ARRAY(String), nullable=False)
    restrictions = Column(String(255), default="Nenhuma")
    experience_level = Column(Enum(
        'iniciante', 'intermediário', 'avançado', name='experience_levels'), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
