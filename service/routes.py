"""
Account Service

This microservice handles the lifecycle of Accounts
"""
# pylint: disable=unused-import
from flask import jsonify, request, make_response, abort, url_for   # noqa; F401
from service.models import Account
from service.common import status  # HTTP Status Codes
from . import app  # Import Flask application


############################################################
# Health Endpoint
############################################################
@app.route("/health")
def health():
    """Health Status"""
    return jsonify(dict(status="OK")), status.HTTP_200_OK


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """Root URL response"""
    return (
        jsonify(
            name="Account REST API Service",
            version="1.0",
            # paths=url_for("list_accounts", _external=True),
        ),
        status.HTTP_200_OK,
    )


######################################################################
# CREATE A NEW ACCOUNT
######################################################################
@app.route("/accounts", methods=["POST"])
def create_accounts():
    """
    Creates an Account
    This endpoint will create an Account based the data in the body that is posted
    """
    app.logger.info("Request to create an Account")
    check_content_type("application/json")
    account = Account()
    account.deserialize(request.get_json())
    account.create()
    message = account.serialize()
    # Uncomment once get_accounts has been implemented
    # location_url = url_for("get_accounts", account_id=account.id, _external=True)
    location_url = "/"  # Remove once get_accounts has been implemented
    return make_response(
        jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}
    )

######################################################################
# LIST ALL ACCOUNTS
######################################################################

# ... place you code here to LIST accounts ...


@app.route("/accounts", methods=["GET"])
def list_accounts():
    """ List accounts """
    # use the Account.all() method to retrieve all accounts
    account_list = Account.all()

    # create a list of serialize() accounts
    accounts_list = [account.serialize() for account in account_list]

    # log the number of accounts being returned in the list
    num_accounts = len(accounts_list)
    app.logger.info(f"returning {num_accounts} accounts in list.")

    # return the list with a return code of status.HTTP_200_O
    return jsonify(accounts_list), status.HTTP_200_OK

######################################################################
# READ AN ACCOUNT
######################################################################

# ... place you code here to READ an account ...


@app.route("/accounts/<int:account_id>", methods=["GET"])
def get_accounts(account_id):
    """Reads one account"""

    # use the Account.find() method to find the account
    find_account = Account.find(account_id)

    # abort() with a status.HTTP_404_NOT_FOUND if it cannot be found
    if not find_account:
        abort(status.HTTP_404_NOT_FOUND, "Account was not found.")

    # return the serialize() version of the account with a return code of status.HTTP_200_OK
    return find_account.serialize(), status.HTTP_200_OK

######################################################################
# UPDATE AN EXISTING ACCOUNT
######################################################################

# ... place you code here to UPDATE an account ...


@app.route("/accounts/<int:account_id>", methods=["PUT"])
def update_accounts(account_id):
    """Update an account"""

    # use the Account.find() method to retrieve the account by the account_id
    find_account = Account.find(account_id)

    # abort() with a status.HTTP_404_NOT_FOUND if it cannot be found
    if not find_account:
        abort(status.HTTP_404_NOT_FOUND, "Account not found")

    # call the deserialize() method on the account passing in request.get_json()
    find_account.deserialize(request.get_json())

    # call account.update() to update the account with the new data
    find_account.update()

    # return the serialize() version of the account with a return code of status.HTTP_200_OK
    return find_account.serialize(), status.HTTP_200_OK

######################################################################
# DELETE AN ACCOUNT
######################################################################

# ... place you code here to DELETE an account ...


@app.route("/accounts/<int:account_id>", methods=["Delete"])
def delete_accounts(account_id):
    """ Delete Account """

    # use the Account.find() method to retrieve the account by the account_id
    find_account = Account.find(account_id)

    # if found, call the delete() method on the account
    if find_account:
        find_account.delete()

    # return and empty body ("") with a return code of status.HTTP_204_NO_CONTENT
    return "", status.HTTP_204_NO_CONTENT

######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


def check_content_type(media_type):
    """Checks that the media type is correct"""
    content_type = request.headers.get("Content-Type")
    if content_type and content_type == media_type:
        return
    app.logger.error("Invalid Content-Type: %s", content_type)
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        f"Content-Type must be {media_type}",
    )
