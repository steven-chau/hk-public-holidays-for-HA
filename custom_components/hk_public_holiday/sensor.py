"""Binary sensor indicating whether today is a Hong Kong public holiday."""

from __future__ import annotations

from typing import Any

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import dt as dt_util

from .const import DOMAIN, TZ_HK
from .coordinator import HkHolidayCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the binary sensor from a config entry."""
    coordinator: HkHolidayCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([HkPublicHolidaySensor(coordinator)])


class HkPublicHolidaySensor(CoordinatorEntity[HkHolidayCoordinator], BinarySensorEntity):
    """Binary sensor that is on during Hong Kong public holidays."""

    _attr_icon = "mdi:beach"
    _attr_name = "Hong Kong public holiday"
    _attr_unique_id = "today"

    def __init__(self, coordinator: HkHolidayCoordinator) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_attribution = "Hong Kong Government (1823)"

    def _today(self) -> str:
        """Return today's date in Hong Kong as "YYYYMMDD"."""
        return dt_util.now(TZ_HK).strftime("%Y%m%d")

    @property
    def is_on(self) -> bool:
        """Return True if today is a public holiday in Hong Kong."""
        return self._today() in (self.coordinator.data or {})

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Expose the name of today's holiday."""
        if self.is_on:
            return {"holiday_name": (self.coordinator.data or {})[self._today()]}
        return {}
