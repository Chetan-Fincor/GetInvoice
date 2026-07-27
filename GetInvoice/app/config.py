import os
from pathlib import Path

# Override via environment variable: GETINVOICE_NETWORK_PATH
NETWORK_SHARE_PATH: Path = Path(
    os.getenv("GETINVOICE_NETWORK_PATH", r"C:\Users\c.bhoumik\Desktop\GetInvoice\data")
)

APP_TITLE = "Get Invoice"
APP_DESCRIPTION = "Enter a client code to find and open the matching folder."
