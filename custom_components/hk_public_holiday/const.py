"""Constants for the Hong Kong public holiday integration."""

from zoneinfo import ZoneInfo

DOMAIN = "hk_public_holiday"

DATA_URL = (
    "https://res.data.gov.hk/api/get-download-file?"
    "name=https%3A%2F%2Fwww.1823.gov.hk%2Fcommon%2Fical%2Fen.json"
)

TZ_HK = ZoneInfo("Asia/Hong_Kong")
