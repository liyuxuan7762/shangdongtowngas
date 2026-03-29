"""Sensor platform for TownGas Meter — exposes currReading as m³."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfVolume
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)
from homeassistant.util import dt as dt_util

from .const import CONF_SUBS_CODE, CONF_SUBS_ID, CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL, DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up sensor from a config entry."""
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator: DataUpdateCoordinator = data["coordinator"]
    schedule_info: dict = data["schedule_info"]
    subs_id = entry.data[CONF_SUBS_ID]
    subs_code = entry.data.get(CONF_SUBS_CODE, subs_id[:8])

    async_add_entities(
        [TownGasMeterSensor(coordinator, entry, subs_id, subs_code, schedule_info)],
        True,
    )


class TownGasMeterSensor(CoordinatorEntity, SensorEntity):
    """Gas meter total reading in m³."""

    _attr_has_entity_name = True
    _attr_device_class = SensorDeviceClass.GAS
    _attr_state_class = SensorStateClass.TOTAL_INCREASING
    _attr_native_unit_of_measurement = UnitOfVolume.CUBIC_METERS
    _attr_icon = "mdi:meter-gas"
    _attr_suggested_display_precision = 0

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        entry: ConfigEntry,
        subs_id: str,
        subs_code: str,
        schedule_info: dict,
    ) -> None:
        super().__init__(coordinator)
        self._subs_id = subs_id
        self._subs_code = subs_code
        self._schedule_info = schedule_info
        self._attr_unique_id = f"towngas_{subs_id}_reading"
        self._attr_translation_key = "gas_meter_reading"

    @property
    def device_info(self) -> dict[str, Any]:
        return {
            "identifiers": {(DOMAIN, self._subs_id)},
            "name": f"港华燃气表 {self._subs_code}",
            "manufacturer": "港华燃气",
            "model": "NB-IoT 燃气表",
        }

    def _get_curr_reading(self) -> str | None:
        """从 datas.readingRptList[0].currReading 读取."""
        datas = (self.coordinator.data or {}).get("datas")
        if not isinstance(datas, dict):
            return None
        lst = datas.get("readingRptList")
        if not lst or not isinstance(lst, list):
            return None
        first = lst[0] if lst else None
        if not isinstance(first, dict):
            return None
        return first.get("currReading")

    @property
    def native_value(self) -> float | None:
        raw = self._get_curr_reading()
        if raw is None:
            return None
        try:
            return float(raw)
        except (ValueError, TypeError):
            return None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        datas = (self.coordinator.data or {}).get("datas", {})
        if not isinstance(datas, dict):
            return {}
        attrs: dict[str, Any] = {}
        for key in (
            "subsCode", "subsName", "subsAddr", "chargeType",
            "totalFee", "errorCode", "errorMsg", "savingSum",
        ):
            val = datas.get(key)
            if val is not None:
                attrs[key] = val
        lst = datas.get("readingRptList")
        if lst and isinstance(lst, list) and lst:
            rpt = lst[0]
            if isinstance(rpt, dict):
                for k in ("recordDate", "resId", "amount"):
                    if rpt.get(k) is not None:
                        attrs[k] = rpt[k]

        now = dt_util.utcnow()
        for key in ("next_data_refresh", "next_token_refresh"):
            ts = self._schedule_info.get(key)
            if ts is not None:
                delta = int((ts - now).total_seconds())
                attrs[key] = ts.isoformat()
                attrs[f"{key}_in"] = f"{max(delta, 0)}s"

        return attrs
