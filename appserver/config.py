from dataclasses import dataclass, field
from google.cloud.storage import Client
from google.oauth2.service_account import Credentials


@dataclass(init=True, repr=True)
class Config:
    HOST: str = field(default="0.0.0.0")
    PORT: int = field(default=8890)

    DEBUG: bool = field(default=False)
    CREDENTIAL_PATH: str = field(default="./credentials/gcp_develop_credential.json")
    BUCKET_NAME: str = field(default="vlcc-storage")

    CACHE_TYPE: str = field(default="SimpleCache")
    CACHE_DEFAULT_TIMEOUT: int = field(default=3600)

    @property
    def storage_bucket(self):
        credential = Credentials.from_service_account_file(self.CREDENTIAL_PATH)
        client = Client(credentials=credential)
        return client.get_bucket(self.BUCKET_NAME)


@dataclass(init=True, repr=True)
class DevConfig(Config):
    DEBUG: bool = field(default=True)
