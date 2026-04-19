"""Coordinator for SolarLife MPPT."""

from __future__ import annotations

from datetime import timedelta
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class SolarLifeMpptCoordinator(DataUpdateCoordinator):
    """Coordinator to manage SolarLife MPPT data."""

    def __init__(self, hass: HomeAssistant, address: str) -> None:
        """Initialize the coordinator."""
        self.address = address
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=30),
        )

    async def _async_update_data(self):
        """Fetch data from the device."""
        return {
            "address": self.address,
            "connected": False,
            "battery_voltage": None,
            "solar_voltage": None,
            "solar_current": None,
            "solar_power": None,
        }
