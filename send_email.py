import requests

MAILGUN_API_KEY = "ac3d5f74-58d132c2"
MAILGUN_DOMAIN = "sandbox9937da24f1034c798682e7b28e55b209.mailgun.org"

def send_otp_email(email: str, otp: str):
    """
    Sends an OTP email using Mailgun's API.
    """
    url = f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages"
    auth = ("api", MAILGUN_API_KEY)
    data = {
        "from": f"YourApp <no-reply@{MAILGUN_DOMAIN}>",
        "to": [email],
        "subject": "Your OTP Code",
        "text": f"Your OTP code is: {otp}",
    }

    response = requests.post(url, auth=auth, data=data)

    if response.status_code == 200:
        print(f"OTP sent to {email}")
        return True
    else:
        print("Failed to send OTP:", response.text)
        return False
