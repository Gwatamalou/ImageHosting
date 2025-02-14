from contextlib import asynccontextmanager
import os
import redis
from aiobotocore.session import get_session
from dotenv import load_dotenv

load_dotenv()


class S3Client:
    def __init__(self,
                 access_key: str = os.getenv("s3_access_key"),
                 secret_key: str = os.getenv("s3_secret_key"),
                 endpoint_url: str = os.getenv("s3_endpoint_url"),
                 bucket_name: str = os.getenv("s3_bucket_name")
                 ):
        self.config = {
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "endpoint_url": endpoint_url,
        }
        self.bucket_name = bucket_name
        self.session = get_session()

    @asynccontextmanager
    async def get_client(self):
        async with self.session.create_client("s3", **self.config) as client:
            yield client




class RedisClient:
    def __init__(self,
                 host: str = "redis",
                 port: str = "6379",
                 decode: bool = True):
        self.client = redis.Redis(host=host, port=port, decode_responses=decode)


    def get_client(self):
        return self.client
