import flask
from intuitlib.client import AuthClient
from intuitlib.enums import Scopes
import config


def authorize_quickbooks():
    # Instantiate client
    auth_client = AuthClient(
        client_id=config.client_id,
        client_secret=config.client_secret,
        redirect_uri=config.quickbooks_redirect_uri,
        environment="sandbox",
    )

    # Prepare scopes
    scopes = [
        Scopes.ACCOUNTING,
        Scopes.PAYMENT,
    ]

    # Get authorization URL
    auth_url = auth_client.get_authorization_url(scopes)
    return auth_url
    # Using standard redirect
    # return redirect(auth_url)