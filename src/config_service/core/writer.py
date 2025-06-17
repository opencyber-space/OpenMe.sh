from sqlalchemy.exc import SQLAlchemyError
from uuid import uuid4
from .db import db_session
# Assuming the models are in models.py
from .base import TopicsData, MessagingConfigParams, GlobalConfigParams
import logging

# Setup basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def write_topics_data(subject_id=None, topic_ids=None):

    try:
        if subject_id is None:
            subject_id = str(uuid4())

        new_topic_data = TopicsData(
            subject_id=subject_id, topic_ids=','.join(topic_ids))
        db_session.add(new_topic_data)
        db_session.commit()
        logger.info(f"Inserted topics data with subject_id {subject_id}")
    except SQLAlchemyError as e:
        db_session.rollback()
        logger.error(f"Error inserting topics_data: {str(e)}")
        raise


def update_topics_data(subject_id, topic_ids):

    try:
        topic_data = TopicsData.query.filter_by(subject_id=subject_id).first()
        if topic_data:
            topic_data.topic_ids = ','.join(topic_ids)
            db_session.commit()
            logger.info(f"Updated topics data for subject_id {subject_id}")
        else:
            logger.warning(f"No topics data found for subject_id {subject_id}")
    except SQLAlchemyError as e:
        db_session.rollback()
        logger.error(f"Error updating topics_data: {str(e)}")
        raise


def write_messaging_config_params(topic_id, config_name, config_value):

    try:
        new_config = MessagingConfigParams(
            topic_id=topic_id, config_name=config_name, config_value=config_value)
        db_session.add(new_config)
        db_session.commit()
        logger.info(
            f"Inserted messaging config for topic_id {topic_id}, config_name {config_name}")
    except SQLAlchemyError as e:
        db_session.rollback()
        logger.error(f"Error inserting messaging_config_params: {str(e)}")
        raise


def update_messaging_config_params(topic_id, config_name, config_value):

    try:
        config = MessagingConfigParams.query.filter_by(
            topic_id=topic_id, config_name=config_name).first()
        if config:
            config.config_value = config_value
            db_session.commit()
            logger.info(
                f"Updated messaging config for topic_id {topic_id}, config_name {config_name}")
        else:
            logger.warning(
                f"No config found for topic_id {topic_id}, config_name {config_name}")
    except SQLAlchemyError as e:
        db_session.rollback()
        logger.error(f"Error updating messaging_config_params: {str(e)}")
        raise


def write_global_config_params(config_name, config_value):

    try:
        new_config = GlobalConfigParams(
            config_name=config_name, config_value=config_value)
        db_session.add(new_config)
        db_session.commit()
        logger.info(f"Inserted global config {config_name}")
    except SQLAlchemyError as e:
        db_session.rollback()
        logger.error(f"Error inserting global_config_params: {str(e)}")
        raise


def update_global_config_params(config_name, config_value):

    try:
        config = GlobalConfigParams.query.filter_by(
            config_name=config_name).first()
        if config:
            config.config_value = config_value
            db_session.commit()
            logger.info(f"Updated global config {config_name}")
        else:
            logger.warning(
                f"No global config found for config_name {config_name}")
    except SQLAlchemyError as e:
        db_session.rollback()
        logger.error(f"Error updating global_config_params: {str(e)}")
        raise
