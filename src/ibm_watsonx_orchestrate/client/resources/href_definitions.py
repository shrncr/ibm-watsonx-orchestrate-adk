#  -----------------------------------------------------------------------------------------
#  (C) Copyright IBM Corp. 2023-2024.
#  https://opensource.org/licenses/BSD-3-Clause
#  -----------------------------------------------------------------------------------------
from __future__ import annotations
from typing import TYPE_CHECKING

import re

if TYPE_CHECKING:
    from ibm_watsonx_orchestrate.client.client import Client

DEPLOYMENTS_HREF_PATTERN = "{}/v4/deployments"
DEPLOYMENT_HREF_PATTERN = "{}/v4/deployments/{}"

IAM_TOKEN_API = "{}&grant_type=urn%3Aibm%3Aparams%3Aoauth%3Agrant-type%3Aapikey"
IAM_TOKEN_URL = "{}/oidc/token"
PROD_URL = [
    "https://dl.watson-orchestrate.ibm.com",
]

DEV_URL = ["https://dev-conn.watson-orchestrate.ibm.com"]

MCSP_TOKEN_URL = "{}/siusermgr/api/1.0/apikeys/token"

GET_MESSAGES_IN_THREAD_HREF_PATTERN = "{}/v1/orchestrate/threads/{}/messages"
LIST_THREADS_HREF_PATTERN = "{}/v1/orchestrate/threads"

def is_url(s: str) -> bool:
    res = re.match("https?:\/\/.+", s)
    return res is not None


def is_id(s: str) -> bool:
    res = re.match("[a-z0-9\-]{36}", s)
    return res is not None


class HrefDefinitions:
    def __init__(
        self,
        client: Client,
        cloud_platform_spaces: bool = False,
        platform_url: str | None = None,
        cp4d_platform_spaces: bool = False,
    ):
        self._credentials = client.credentials
        self._client = client
        self.cloud_platform_spaces = cloud_platform_spaces
        self.cp4d_platform_spaces = cp4d_platform_spaces
        self.platform_url = platform_url

    def _get_platform_url_if_exists(self) -> str:
        return self.platform_url if self.platform_url else self._credentials.url

    def get_token_endpoint_href(self) -> str:
        return TOKEN_ENDPOINT_HREF_PATTERN.format(self._credentials.url)

    def get_cpd_token_endpoint_href(self) -> str:
        return CPD_TOKEN_ENDPOINT_HREF_PATTERN.format(
            self._credentials.url.replace(":31002", ":31843")
        )

    def get_cpd_bedrock_token_endpoint_href(self) -> str:
        return CPD_BEDROCK_TOKEN_ENDPOINT_HREF_PATTERN.format(
            self._credentials.bedrock_url
        )

    def get_cpd_validation_token_endpoint_href(self) -> str:
        return CPD_VALIDATION_TOKEN_ENDPOINT_HREF_PATTERN.format(self._credentials.url)

    def get_iam_token_api(self) -> str:
        return IAM_TOKEN_API.format(self._credentials.api_key)

    def get_iam_token_url(self) -> str:
        if self._credentials.url in PROD_URL:
            return IAM_TOKEN_URL.format("https://iam.cloud.ibm.com")
        else:
            return IAM_TOKEN_URL.format("https://iam.test.cloud.ibm.com")

    def get_mcsp_token_url(self) -> str:
        if self._credentials.url in PROD_URL:
            return MCSP_TOKEN_URL.format("https://iam.platform.saas.ibm.com")
        elif self._credentials.url in DEV_URL:
            return MCSP_TOKEN_URL.format("https://iam.platform.dev.saas.ibm.com")

        else:
            return MCSP_TOKEN_URL.format("https://iam.platform.test.saas.ibm.com")

    def get_url_prefix(self) -> str:
        return f'{self._client.PLATFORM_URL}/instances/{self._credentials.instance_id}'

    def get_messages_in_thread_href(self, thread_id: str) -> str:
        return GET_MESSAGES_IN_THREAD_HREF_PATTERN.format(self.get_url_prefix(), thread_id)

    def get_list_threads_href(self) -> str:
        return LIST_THREADS_HREF_PATTERN.format(self.get_url_prefix())
