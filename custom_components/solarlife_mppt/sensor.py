"""Sensor platform for SolarLife MPPT."""

from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfElectricCurrent, UnitOfElectricPotential, UnitOfPower
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import SolarLifeMpptCoordinator


@dataclass
class SolarLifeSensorDescription:
    """Describe a SolarLife sensor."""

    key: str
    name: str
    unit: str | None = None


SENSORS: tuple[SolarLifeSensorDescription, ...] = (
    SolarLifeSensorDescription("battery_voltage", "Battery Voltage", UnitOfElectricPotential.VOLT),
    SolarLifeSensorDescription("solar_voltage", "Solar Voltage", UnitOfElectricPotential.VOLT),
    SolarLifeSensorDescription("solar_current", "Solar Current", UnitOfElectricCurrent.AMPERE),
    SolarLifeSensorDescription("solar_power", "Solar Power", UnitOfPower.WATT),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up SolarLife MPPT sensors from a config entry."""
    coordinator: SolarLifeMpptCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        SolarLifeMpptSensor(coordinator, entry, description)
        for description in SENSORS
    )


class SolarLifeMpptSensor(CoordinatorEntity, SensorEntity):
    """Representation of a SolarLife MPPT sensor."""

    def __init__(
        self,
        coordinator: SolarLifeMpptCoordinator,
        entry: ConfigEntry,
        description: SolarLifeSensorDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._entry = entry

        self._attr_name = f"{entry.title} {description.name}"
        self._attr_unique_id = f"{entry.entry_id}_{description.key}"
        self._attr_native_unit_of_measurement = description.unit

    @property
    def device_info(self) -> DeviceInfo:
        """Return device info."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._entry.entry_id)},
            name=self._entry.title,
            manufacturer="SolarLife",
            model="MPPT",
        )

    @property
    def native_value(self):
        """Return the sensor value."""
        return self.coordinator.data.get(self.entity_description.key)
