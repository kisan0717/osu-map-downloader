import keyring
import osu
from modules.constants import SERVICE
from modules.gui import editCredentials

def getCredentials():
	clientID = keyring.get_password(
		SERVICE,
		'client_id'
	)

	clientSecret = keyring.get_password(
		SERVICE,
		'client_secret'
	)

	if not clientID or not clientSecret:
		editCredentials()

		clientID = keyring.get_password(
			SERVICE,
			'client_id'
		)

		clientSecret = keyring.get_password(
			SERVICE,
			'client_secret'
		)

	return clientID, clientSecret

# get osu client from credentials
def getClient():
	clientID, clientSecret = getCredentials()

	client = osu.Client.from_credentials(
		clientID,
		clientSecret,
		None
	)

	return client
