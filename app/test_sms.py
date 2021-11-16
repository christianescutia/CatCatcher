from twilio.rest import Client


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = 'ACebaf22614c3bf1885d8bb9acf1638ab7'
auth_token = 'f54342d07240369873eddb11dfab5f25'
client = Client(account_sid, auth_token)

message = client.messages.create(
                              body='Cat Catcher App Test',
                              from_='+18646600650',
                              to='+15129634836'
                          )

print(message.sid)