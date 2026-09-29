import json
from urllib import error as urllib_error
from urllib import request as urllib_request
import logging
from fastapi import HTTPException
from ..config import get_required_setting
from ..schemas import ContactRequest
logger = logging.getLogger("uvicorn.error")

def send_contact_email(contact: ContactRequest) -> None:
    api_key = get_required_setting("RESEND_API_KEY")
    from_email = get_required_setting("RESEND_FROM_EMAIL")
    to_email = get_required_setting("CONTACT_TO_EMAIL")
    payload = json.dumps({
        "from": from_email,
        "to": [to_email],
        "reply_to": contact.email,
        "subject": contact.subject,
        "text": f"Name: {contact.name}\nEmail: {contact.email}\n\n{contact.message}",
    }).encode("utf-8")
    request = urllib_request.Request(
        "https://api.resend.com/emails",
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib_request.urlopen(request, timeout=10) as response:
            if response.status >= 300:
                raise HTTPException(status_code=502, detail="Email provider rejected the message")
    except urllib_error.HTTPError as exc:
        response_body = exc.read().decode("utf-8", errors="replace")
        logger.error(
            "Resend rejected email with status %s: %s",
            exc.code,
            response_body,
        )
        raise HTTPException(
            status_code=502,
            detail="Email provider rejected the message",
        ) from exc
    except urllib_error.URLError as exc:
        raise HTTPException(status_code=502, detail="Unable to reach email provider") from exc
