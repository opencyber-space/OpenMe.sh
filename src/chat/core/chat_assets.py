import boto3
import os
import uuid
import logging
from botocore.exceptions import BotoCoreError, ClientError
from typing import Tuple

logger = logging.getLogger(__name__)


class ChatAssetUploader:
    def __init__(self):
        try:
            self.endpoint_url = os.getenv("S3_URL")
            self.bucket_name = os.getenv("S3_BUCKET")
            self.access_key = os.getenv("S3_ACCESS_KEY")
            self.secret_key = os.getenv("S3_SECRET_KEY")
            self.region = os.getenv("S3_REGION", "us-east-1")

            self.client = boto3.client(
                "s3",
                endpoint_url=self.endpoint_url,
                aws_access_key_id=self.access_key,
                aws_secret_access_key=self.secret_key,
                region_name=self.region
            )

            logger.info("Initialized ChatAssetUploader with S3 endpoint")
        except Exception as e:
            logger.error(f"Failed to initialize S3 client: {e}")
            raise

    def upload_file(self, file_bytes: bytes, session_id: str, content_type: str = "application/octet-stream") -> Tuple[bool, str]:
        try:
            file_uuid = str(uuid.uuid4())
            key = f"{session_id}/{file_uuid}"

            self.client.put_object(
                Bucket=self.bucket_name,
                Key=key,
                Body=file_bytes,
                ContentType=content_type
            )

            logger.info(f"File uploaded to {key}")
            return True, key
        except (BotoCoreError, ClientError) as e:
            logger.error(f"Failed to upload file to S3: {e}")
            return False, str(e)
