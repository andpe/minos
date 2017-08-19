# Minos
A vote-based queue management system for Sonos speakers

## Setup
Install the requirements using ```pip install --user -r requirements.txt``` (preferably in a virtualenv to not litter).

To start the application you also need the consumer token and consumer secret for twitter authentication, which can be found/created at https://apps.twitter.com/

These two tokens need to be inserted into the database manually (for now):
```sql
INSERT INTO oauth_settings (provider_name, "key", value) VALUES('twitter', 'consumer_key', 'KEY_GOES_HERE')
INSERT INTO oauth_settings (provider_name, "key", value) VALUES('twitter', 'consumer_secret', 'SECRET_GOES_HERE')
```
