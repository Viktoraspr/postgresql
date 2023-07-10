from dataclasses import dataclass
from .logins import USER, HOST, DBNAME, PASSWORD, PORT


@dataclass
class User:
    """
    Creates User object for connection with DB.
    """
    host: str
    dbname: str
    user: str
    password: str
    port: int


USER = User(host=HOST, dbname=DBNAME, user=USER, password=PASSWORD, port=PORT)
