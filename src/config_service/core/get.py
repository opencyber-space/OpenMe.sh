from sqlalchemy.exc import SQLAlchemyError
from .db import db_session
# Assuming models are in models.py
from .base import TopicsData, MessagingConfigParams, GlobalConfigParams
import logging

# Setup basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_topics_data_by_subject_id(subject_id):

    try:
        topic_data = TopicsData.query.filter_by(subject_id=subject_id).first()
        if topic_data:
            logger.info(f"Fetched topics data for subject_id {subject_id}")
            return topic_data
        else:
            logger.warning(f"No topics data found for subject_id {subject_id}")
            return None
    except SQLAlchemyError as e:
        logger.error(
            f"Error fetching topics_data for subject_id {subject_id}: {str(e)}")
        raise


def get_all_topics_data():

    try:
        topics_data_list = TopicsData.query.all()
        logger.info(f"Fetched {len(topics_data_list)} topics_data records")
        return topics_data_list
    except SQLAlchemyError as e:
        logger.error(f"Error fetching all topics_data: {str(e)}")
        raise


def get_messaging_config_by_topic_id(topic_id):

    try:
        configs = MessagingConfigParams.query.filter_by(
            topic_id=topic_id).all()
        if configs:
            logger.info(
                f"Fetched {len(configs)} configs for topic_id {topic_id}")
            return configs
        else:
            logger.warning(f"No configs found for topic_id {topic_id}")
            return None
    except SQLAlchemyError as e:
        logger.error(
            f"Error fetching configs for topic_id {topic_id}: {str(e)}")
        raise


def get_messaging_config_by_config_name(topic_id, config_name):

    try:
        config = MessagingConfigParams.query.filter_by(
            topic_id=topic_id, config_name=config_name).first()
        if config:
            logger.info(
                f"Fetched config for topic_id {topic_id} and config_name {config_name}")
            return config
        else:
            logger.warning(
                f"No config found for topic_id {topic_id} and config_name {config_name}")
            return None
    except SQLAlchemyError as e:
        logger.error(
            f"Error fetching config for topic_id {topic_id} and config_name {config_name}: {str(e)}")
        raise


def get_global_config_by_name(config_name):

    try:
        config = GlobalConfigParams.query.filter_by(
            config_name=config_name).first()
        if config:
            logger.info(f"Fetched global config for config_name {config_name}")
            return config
        else:
            logger.warning(
                f"No global config found for config_name {config_name}")
            return None
    except SQLAlchemyError as e:
        logger.error(
            f"Error fetching global config for config_name {config_name}: {str(e)}")
        raise


def get_all_global_configs():

    try:
        configs = GlobalConfigParams.query.all()
        logger.info(f"Fetched {len(configs)} global configs")
        return configs
    except SQLAlchemyError as e:
        logger.error(f"Error fetching all global configs: {str(e)}")
        raise
