import copy
import logging
from typing import Any, cast

from ibm_watsonx_orchestrate.client.client_errors import NoCredentialsProvided, ClientError
from ibm_watsonx_orchestrate.client.credentials import Credentials
from ibm_watsonx_orchestrate.client.messaging.chat_messages import ChatMessages
from ibm_watsonx_orchestrate.client.messaging.messages import Messages
from ibm_watsonx_orchestrate.client.resources.threads import Threads
from ibm_watsonx_orchestrate.client.service_instance import ServiceInstance


class Client:
    """The main class of ibm_watsonx_orchestrate. The very heart of the module. Client contains objects that manage the service reasources.

    To explore how to use Client, refer to:
     - :ref:`Setup<setup>` - to check correct initialization of Client for a specific environment.
     - :ref:`Core<core>` - to explore core properties of an Client object.

    :param url: URL of the service
    :type url: str

    :param credentials: credentials used to connect with the service
    :type credentials: Credentials

    **Example**

    .. code-block:: python

        from ibm_watsonx_orchestrate import Client, Credentials

        credentials = Credentials(
            url = "<url>",
            api_key = "<api_key>"
        )

        client = Client(credentials, space_id="<space_id>")

        client.models.list()
        client.deployments.get_details()

        client.set.default_project("<project_id>")

        ...

    """
    version: str | None = None
    _internal: bool = False

    def __init__(
        self,
        credentials: Credentials | None = None,
        **kwargs: Any,
    ) -> None:
        if credentials is None:
            raise TypeError("Client() missing 1 required argument: 'credentials'")

        self._logger = logging.getLogger(__name__)

        credentials._set_env_vars_from_credentials()

        if isinstance(credentials.verify, str):
            credentials.verify = True

        # At this stage `credentials` has type Dict[str, str]
        credentials = cast(Credentials, credentials)
        self.credentials = copy.deepcopy(credentials)
        self.CLOUD_PLATFORM_SPACES = True
        self.ICP_PLATFORM_SPACES = False
        self.PLATFORM_URL = None
        self._iam_id = None
        self._spec_ids_per_state: dict = {}
        self._user_headers: dict | None = None  # Used in set_headers() method

        self.PLATFORM_URLS_MAP = {
            "https://dev-conn.watson-orchestrate.ibm.com": "https://api.dev-conn.watson-orchestrate.ibm.com",
        }

        import ibm_watsonx_orchestrate._wrappers.requests as requests

        requests.packages.urllib3.disable_warnings()  # type: ignore[attr-defined]

        if self.credentials.token is not None:
            if not self.credentials.api_key:
                self.proceed = True
            else:
                # _is_env_token is used for initialising client on cluster with USER_ACCESS_TOKEN environment variable.
                self.proceed = not self.credentials._is_env_token
        else:
            self.proceed = False

        self.token: str | None = None
        if credentials is None:
            raise NoCredentialsProvided()
        if self.credentials.url is None:
            raise ClientError(ChatMessages.get_message(message_id="url_not_provided"))
        if not self.credentials.url.startswith("https://"):
            raise ClientError(ChatMessages.get_message(message_id="invalid_url"))
        if self.credentials.url[-1] == "/":
            self.credentials.url = self.credentials.url.rstrip("/")

        self.PLATFORM_URL = self.PLATFORM_URLS_MAP[self.credentials.url]        

        # For cloud, service_instance.details will be set during space creation( if instance is associated ) or
        # while patching a space with an instance
        self.service_instance: ServiceInstance = ServiceInstance(self)
        self.chat_messages = ChatMessages(self)
        self.threads = Threads(self)
        self._logger.info(
            Messages.get_message(message_id="client_successfully_initialized")
        )

    def _check_if_either_is_set(self) -> None:
        if self.default_space_id is None and self.default_project_id is None:
            raise ClientError(
                ChatMessages.get_message(
                    message_id="it_is_mandatory_to_set_the_space_project_id"
                )
            )

    def _get_headers(
        self,
        content_type: str = "application/json",
        no_content_type: bool = False,
        zen: bool = False,
    ) -> dict:

        if zen:
            headers = {"Content-Type": content_type}
            token = self.service_instance._create_token()
            if len(token.split(".")) == 1:
                headers.update({"Authorization": "Basic " + token})

            else:
                headers.update({"Authorization": "Bearer " + token})
        else:
            if self.proceed is True:
                token_to_use = self.credentials.token
                if len(token_to_use.split(".")) == 1:
                    token = "Basic " + token_to_use

                else:
                    token = "Bearer " + token_to_use
            else:
                token = "Bearer " + self.service_instance._get_token()
            headers = {
                "Authorization": token,
                # "User-Agent": get_user_agent_header(),
            }

            if not no_content_type:
                headers.update({"Content-Type": content_type})

        if self._user_headers:
            headers = headers | self._user_headers

        return headers

    def set_token(self, token: str) -> None:
        """
        Method which allows refresh/set new User Authorization Token.

        :param token: User Authorization Token
        :type token: str

        **Examples**

        .. code-block:: python

            client.set_token("<USER AUTHORIZATION TOKEN>")

        """
        self.proceed = True
        self.token = token
        self.credentials.token = token

    def set_headers(self, headers: dict) -> None:
        """
        Method which allows refresh/set new User Request Headers.

        :param headers: User Request Headers
        :type headers: dict

        **Examples**

        .. code-block:: python

            headers = {
                'Authorization': 'Bearer <USER AUTHORIZATION TOKEN>',
                'User-Agent': 'ibm-watsonx-ai/1.0.1 (lang=python; arch=x86_64; os=darwin; python.version=3.10.13)',
                'X-Watson-Project-ID': '<PROJECT ID>',
                'Content-Type': 'application/json'
            }

            client.set_headers(headers)

        """
        self._user_headers = headers

    def _get_icptoken(self) -> str:
        return self.service_instance._create_token()

    def _is_default_space_set(self) -> bool:
        if self.default_space_id is not None:
            return True
        return False

    def _is_IAM(self) -> bool:
        if self.credentials.api_key is not None:
            if self.credentials.api_key != "":
                return True
            else:
                raise ClientError(
                    ChatMessages.get_message(message_id="apikey_value_cannot_be_empty")
                )
        elif self.credentials.token is not None:
            if self.credentials.token != "":
                return True
            else:
                raise ClientError(
                    ChatMessages.get_message(message_id="token_value_cannot_be_empty")
                )
        else:
            return False

    def _is_MCSP(self) -> bool:
        if self.credentials.api_key is not None:
            if self.credentials.api_key != "":
                return True
            else:
                raise ClientError(
                    ChatMessages.get_message(message_id="apikey_value_cannot_be_empty")
                )
        elif self.credentials.token is not None:
            if self.credentials.token != "":
                return True
            else:
                raise ClientError(
                    ChatMessages.get_message(message_id="token_value_cannot_be_empty")
                )
        else:
            return False

    def _check_if_fm_ga_api_available(self) -> bool:
        import ibm_watsonx_orchestrate._wrappers.requests as requests

        response_ga_api = requests.get(
            url="{}/ml/v1/foundation_model_specs?limit={}".format(
                self.credentials.url, "1"
            ),
            params={"version": self.version_param},
        )
        return response_ga_api.status_code == 200
