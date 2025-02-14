from contextlib import asynccontextmanager
import os
from fcntl import FASYNC

import redis
from aiobotocore.session import get_session
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

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
                 host: str = os.getenv("redis_host"),
                 port: str = os.getenv("redis_port"),
                 decode: bool = True):
        self.client = redis.Redis(host=host, port=port, decode_responses=decode)

    def get_client(self):
        return self.client


class PGClient:
    def __init__(self,
                 url: str = f"postgresql+asyncpg://{os.getenv("DB_LOGIN")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}:5432/{os.getenv('DB_NAME')}",
                 echo: bool = False
                 ):
        self.engine = create_async_engine(url=url, echo=echo)
        self.session_factory = async_sessionmaker(bind=self.engine, autocommit=False)

    async def get_session(self) -> AsyncSession:
        async with self.session_factory() as session:
            yield session
