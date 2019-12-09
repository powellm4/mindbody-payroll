import flask
from intuitlib.client import AuthClient
from intuitlib.enums import Scopes
import config



    # Instantiate client
auth_client = AuthClient(
    client_id=config.client_id,
    client_secret=config.client_secret,
    redirect_uri=config.quickbooks_redirect_uri,
    environment="sandbox",
)


def authorize_quickbooks():
    # Prepare scopes
    scopes = [
        Scopes.ACCOUNTING,
    ]

    # Get authorization URL
    auth_url = auth_client.get_authorization_url(scopes)
    return auth_url
