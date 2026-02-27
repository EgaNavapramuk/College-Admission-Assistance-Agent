from __future__ import annotations

import json
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import Dict

USERS_PATH = Path("users.json")


@dataclass
class User:
    username: str


def _hash_password(password: str) -> str:
    return sha256(password.encode("utf-8")).hexdigest()


def load_users() -> Dict[str, str]:
    if not USERS_PATH.exists():
        return {}
    try:
        data = json.loads(USERS_PATH.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            return {str(k): str(v) for k, v in data.items()}
    except Exception:
        return {}
    return {}


def save_users(users: Dict[str, str]) -> None:
    USERS_PATH.write_text(json.dumps(users, indent=2), encoding="utf-8")


def create_user(username: str, password: str) -> tuple[bool, str]:
    username = username.strip()
    if not username or not password:
        return False, "Username and password are required."
    users = load_users()
    if username in users:
        return False, "User already exists. Please log in instead."
    users[username] = _hash_password(password)
    save_users(users)
    return True, "Account created successfully. You can log in now."


def authenticate(username: str, password: str) -> tuple[bool, str]:
    username = username.strip()
    users = load_users()
    if username not in users:
        return False, "User not found."
    if users[username] != _hash_password(password):
        return False, "Incorrect password."
    return True, "Login successful."