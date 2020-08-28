# lambda-messaging

Lambda that sends sms or email to user. It receives an array of dictionaries containing
phone_number or email and message contents.
Input:

```
{
    "data": {
        [
            {
                'phone_number': '+552199999999',
                'message': 'Bom dia!'
            },
            {
                'email': '+5521991299889',
                'message': 'Bom tarde!'
            }
        ]
    }
}
```

# Usage

Example of usage.

Lambda *asynchronous invocation* is preferable

```
import json
import boto3
from config import MS_MESSAGING

# MS_MESSAGING = "risk-mg-platform-dev-sms"


def send_sms(messages_array):
    """Send sms
    Args:
        phone_number (string): the phone number that will receive the sms
        body_message (string): the message
    """
    client = boto3.client('lambda')
    payload = {
        "data": messages_array
    }
    client.invoke(
        FunctionName=MS_MESSAGING,
        InvocationType='Event',
        Payload=json.dumps(payload),
        LogType='None'
    )

```