import base64
import email as email_lib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
from googleapiclient.discovery import build
from auth import get_credentials


def _build_service():
    return build("gmail", "v1", credentials=get_credentials())


def _decode_body(payload) -> str:
    """Recursively extract plain text from a message payload."""
    mime_type = payload.get("mimeType", "")
    if mime_type == "text/plain":
        data = payload.get("body", {}).get("data", "")
        return base64.urlsafe_b64decode(data + "==").decode("utf-8", errors="replace")
    if mime_type.startswith("multipart/"):
        for part in payload.get("parts", []):
            text = _decode_body(part)
            if text:
                return text
    return ""


def _parse_headers(headers: list) -> dict:
    return {h["name"].lower(): h["value"] for h in headers}


def list_messages(query: str = "in:inbox", max_results: int = 20) -> list[dict]:
    service = _build_service()
    result = service.users().messages().list(
        userId="me", q=query, maxResults=max_results
    ).execute()
    messages = result.get("messages", [])

    summaries = []
    for msg in messages:
        full = service.users().messages().get(
            userId="me", id=msg["id"], format="metadata",
            metadataHeaders=["Subject", "From", "Date"]
        ).execute()
        headers = _parse_headers(full.get("payload", {}).get("headers", []))
        snippet = full.get("snippet", "")
        labels = full.get("labelIds", [])
        summaries.append({
            "id": msg["id"],
            "subject": headers.get("subject", "(no subject)"),
            "from": headers.get("from", "unknown"),
            "date": headers.get("date", ""),
            "snippet": snippet,
            "unread": "UNREAD" in labels,
        })
    return summaries


def get_message(msg_id: str) -> dict:
    service = _build_service()
    full = service.users().messages().get(
        userId="me", id=msg_id, format="full"
    ).execute()
    headers = _parse_headers(full.get("payload", {}).get("headers", []))
    body = _decode_body(full.get("payload", {}))
    return {
        "id": msg_id,
        "subject": headers.get("subject", "(no subject)"),
        "from": headers.get("from", "unknown"),
        "to": headers.get("to", ""),
        "date": headers.get("date", ""),
        "body": body,
        "thread_id": full.get("threadId"),
        "label_ids": full.get("labelIds", []),
        "message_id_header": headers.get("message-id", ""),
        "references": headers.get("references", ""),
    }


def get_thread(thread_id: str) -> list[dict]:
    service = _build_service()
    result = service.users().threads().get(userId="me", id=thread_id, format="full").execute()
    messages = []
    for msg in result.get("messages", []):
        headers = _parse_headers(msg.get("payload", {}).get("headers", []))
        body = _decode_body(msg.get("payload", {}))
        messages.append({
            "id": msg["id"],
            "from": headers.get("from", "unknown"),
            "to": headers.get("to", ""),
            "date": headers.get("date", ""),
            "body": body,
        })
    return messages


def send_message(to: str, subject: str, body: str, reply_to: Optional[dict] = None) -> dict:
    service = _build_service()
    msg = MIMEMultipart()
    msg["To"] = to
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    thread_id = None
    if reply_to:
        msg["In-Reply-To"] = reply_to.get("message_id_header", "")
        refs = reply_to.get("references", "")
        if refs:
            msg["References"] = refs + " " + reply_to.get("message_id_header", "")
        else:
            msg["References"] = reply_to.get("message_id_header", "")
        thread_id = reply_to.get("thread_id")

    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    body_payload = {"raw": raw}
    if thread_id:
        body_payload["threadId"] = thread_id

    return service.users().messages().send(userId="me", body=body_payload).execute()


def archive_message(msg_id: str) -> dict:
    service = _build_service()
    return service.users().messages().modify(
        userId="me", id=msg_id, body={"removeLabelIds": ["INBOX"]}
    ).execute()


def trash_message(msg_id: str) -> dict:
    service = _build_service()
    return service.users().messages().trash(userId="me", id=msg_id).execute()


def mark_read(msg_id: str) -> dict:
    service = _build_service()
    return service.users().messages().modify(
        userId="me", id=msg_id, body={"removeLabelIds": ["UNREAD"]}
    ).execute()


def mark_unread(msg_id: str) -> dict:
    service = _build_service()
    return service.users().messages().modify(
        userId="me", id=msg_id, body={"addLabelIds": ["UNREAD"]}
    ).execute()


def list_labels() -> list[dict]:
    service = _build_service()
    result = service.users().labels().list(userId="me").execute()
    return result.get("labels", [])


def apply_label(msg_id: str, label_name: str) -> Optional[dict]:
    service = _build_service()
    labels = list_labels()
    label = next((l for l in labels if l["name"].lower() == label_name.lower()), None)
    if not label:
        return None
    return service.users().messages().modify(
        userId="me", id=msg_id, body={"addLabelIds": [label["id"]]}
    ).execute()


def get_profile() -> dict:
    service = _build_service()
    return service.users().getProfile(userId="me").execute()
