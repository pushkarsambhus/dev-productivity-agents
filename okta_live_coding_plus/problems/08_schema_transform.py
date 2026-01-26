"""
08_schema_transform.py
----------------------
Goal: Normalize messy JSON records into a clean schema.

Why this matters:
- Real data rarely arrives clean. You must write robust transformations.

We define a simple normalized schema:
{
  "user_id": str,
  "email": str,
  "country": str,
  "age": int | None
}

Input records might have different keys or types; we coerce carefully.
"""

from typing import Any, Dict, Optional

def to_int_or_none(value: Any) -> Optional[int]:
    """Try to convert to int; return None if impossible."""
    try:
        return int(value)
    except Exception:
        return None

def normalize(record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Map varied keys to the canonical schema and coerce types.
    We handle common alternatives like 'id' vs 'userId', etc.
    Missing fields become None.
    """
    # Extract with fallbacks
    user_id = record.get("user_id") or record.get("id") or record.get("userId")
    email = record.get("email") or record.get("mail") or record.get("contact_email")
    country = record.get("country") or record.get("location") or record.get("nation")
    age = record.get("age") or record.get("yrs") or record.get("years_old")

    # Convert types
    user_id = str(user_id) if user_id is not None else None
    email = str(email) if email is not None else None
    country = str(country) if country is not None else None
    age = to_int_or_none(age)

    return {
        "user_id": user_id,
        "email": email,
        "country": country,
        "age": age,
    }


if __name__ == "__main__":
    messy = [
        {"id": 123, "mail": "a@x.com", "location": "US", "yrs": "29"},
        {"userId": "u-99", "email": "b@x.com", "country": "IN"},
        {"user_id": "42", "contact_email": "c@x.com", "nation": "DE", "years_old": "NaN"},
    ]
    for m in messy:
        print(normalize(m))
