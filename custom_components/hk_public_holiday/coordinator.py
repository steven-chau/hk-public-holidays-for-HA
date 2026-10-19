"""DataUpdateCoordinator for the Hong Kong public holiday integration."""

from __future__ import annotations

from datetime import datetime, timedelta
import json
import logging
from typing import Any

from aiohttp import ClientError, ClientTimeout

from homeassistant.core import CALLBACK_TYPE, HomeAssistant, callback
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.event import async_call_later
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.util import dt as dt_util

from .const import DATA_URL, DOMAIN, TZ_HK
from .parser import parse_holidays

_LOGGER = logging.getLogger(__name__)

_TIMEOUT = ClientTimeout(total=30)


def _next_midnight(now: datetime) -> datetime:
    """Return the next midnight after *now* (Hong Kong time)."""
    return (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)


def _next_dec_30(now: datetime) -> datetime:
    """Return the next 30 December at 00:05 (Hong Kong time)."""
    target = now.replace(month=12, day=30, hour=0, minute=5, second=0, microsecond=0)
    if target <= now:
        target = target.replace(year=now.year + 1)
    return target


class HkHolidayCoordinator(DataUpdateCoordinator[dict[str, str]]):
    """Fetches the list of Hong Kong public holidays.

    Data is downloaded when the integration is set up and refreshed yearly
    on 30 December, when the government publishes next year's holidays.
    """

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize the coordinator."""
        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=None)
        self._unsub_day: CALLBACK_TYPE | None = None
        self._unsub_year: CALLBACK_TYPE | None = None

    @callback
    def _schedule_year(self) -> None:
        """Schedule the yearly data download on 30 December."""
        now = dt_util.now(TZ_HK)
        self._unsub_year = async_call_later(
            self.hass,
            (_next_dec_30(now) - now).total_seconds(),
            self._on_yearly_refresh,
        )

    @callback
    def _schedule_day(self) -> None:
        """Schedule the next sensor update at midnight."""
        now = dt_util.now(TZ_HK)
        self._unsub_day = async_call_later(
            self.hass,
            (_next_midnight(now) - now).total_seconds(),
            self._on_day_change,
        )

    def schedule(self) -> None:
        """Schedule the yearly data refresh and the day-change updates."""
        self._schedule_year()
        self._schedule_day()

    def unschedule(self) -> None:
        """Cancel the scheduled updates."""
        for unsub in (self._unsub_day, self._unsub_year):
            if unsub is not None:
                unsub()

    async def _on_yearly_refresh(self, _now: datetime) -> None:
        """Download the new holiday data and schedule next year's refresh."""
        self._schedule_year()
        await self.async_refresh()

    async def _on_day_change(self, _now: datetime) -> None:
        """Re-render the sensor at midnight without re-downloading data."""
        self._schedule_day()
        self.async_set_updated_data(self.data)

    async def _async_update_data(self) -> dict[str, str]:
        """Download and parse the holiday data."""
        websession = async_get_clientsession(self.hass)
        try:
            async with websession.get(DATA_URL, timeout=_TIMEOUT) as response:
                response.raise_for_status()
                raw = await response.read()
            payload: Any = json.loads(raw.decode("utf-8-sig"))
            return parse_holidays(payload)
        except (ClientError, ValueError, TimeoutError) as err:
            raise UpdateFailed(f"Could not load Hong Kong holiday data: {err}") from err
