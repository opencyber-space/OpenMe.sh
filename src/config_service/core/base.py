import uuid
from sqlalchemy import Column, String, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID  # Use this for PostgreSQL
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import CHAR
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

Base = declarative_base()

# Function to generate UUIDs


def generate_uuid():
    return str(uuid.uuid4())

# topics_data table


class TopicsData(Base):
    __tablename__ = 'topics_data'

    subject_id = Column(UUID(as_uuid=True), primary_key=True,
                        default=generate_uuid)  # UUID primary key
    # Can store a comma-separated list or JSON string for topic IDs
    topic_ids = Column(String, nullable=False)

# messaging_config_params table


class MessagingConfigParams(Base):
    __tablename__ = 'messaging_config_params'

    id = Column(UUID(as_uuid=True), primary_key=True,
                default=generate_uuid)  # UUID primary key
    topic_id = Column(UUID(as_uuid=True), ForeignKey(
        'topics_data.subject_id'), nullable=False)  # Foreign key to TopicsData
    config_name = Column(String, nullable=False)
    config_value = Column(String, nullable=False)

    topic = relationship("TopicsData", back_populates="configs")


TopicsData.configs = relationship(
    "MessagingConfigParams", back_populates="topic")


class GlobalConfigParams(Base):
    __tablename__ = 'global_config_params'

    config_name = Column(String, primary_key=True)
    config_value = Column(String, nullable=False)
