from dataclasses import dataclass, field
from google.cloud.storage import Client
from google.oauth2.service_account import Credentials


@dataclass(init=True, repr=True)
class Config:
    """ 세팅 정보 공유
    """
    # GCP 설정
    CREDENTIAL_PATH: str = field(default="./credentials/gcp_develop_credential.json")
    BUCKET_NAME: str = field(default="vlcc-storage")

    # 캐시 설정
    CACHE_TYPE: str = field(default="SimpleCache")
    CACHE_DEFAULT_TIMEOUT: int = field(default=3600)

    # Kalman filter optimizer 설정
    SYSTEM_NOISE: int = field(default=10)
    SENSOR_NOISE: int = field(default=1000)
    INIT_NOISE: int = field(default=10)

    @property
    def storage_bucket(self):
        credential = Credentials.from_service_account_file(self.CREDENTIAL_PATH)
        client = Client(credentials=credential)
        return client.get_bucket(self.BUCKET_NAME)


@dataclass(init=True, repr=True)
class DevConfig(Config):
    """ 개발환경 서버 세팅
    python appserver/app.py
    """
    HOST: str = field(default="0.0.0.0")
    PORT: int = field(default=8890)
    DEBUG: bool = field(default=True)


@dataclass(init=True, repr=True)
class LiveConfig(Config):
    """ Live 환경 서버 세팅
    gunicorn --bind {{HOST}}:{{PORT}} appserver.run:app
    """
    pass
