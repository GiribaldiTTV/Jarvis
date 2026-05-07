"""Local Monitoring/HUD telemetry boundary helpers for FAM-006.

This module defines the SLC-025 adapter shape. It reports local runtime
readiness facts and the smallest safe native telemetry proof currently
available to the desktop renderer. It does not read vendor APIs, invent
hardware values, model voice/audio behavior, or implement broad provider
platform work. The HUD can show setup/unavailable states and a native CPU load
proof without pretending GPU or thermal values exist before a validated
provider route is admitted.
"""

from __future__ import annotations

import os
import ctypes
from dataclasses import dataclass


PACKAGE_ID = "PKG-006"
SLICE_ID = "SLC-025"
ADAPTER_ID = "desktop-runtime-boundary"
DEFAULT_POLLING_RATE_MS = 1000
MINIMUM_SAFE_POLLING_RATE_MS = 1000


class _FileTime(ctypes.Structure):
    _fields_ = [
        ("dwLowDateTime", ctypes.c_uint32),
        ("dwHighDateTime", ctypes.c_uint32),
    ]


def _filetime_to_int(value: _FileTime) -> int:
    return (int(value.dwHighDateTime) << 32) + int(value.dwLowDateTime)


class NativeCpuLoadProbe:
    """Tiny Windows-native CPU-load proof using kernel/user/idle deltas."""

    def __init__(self) -> None:
        self._last_idle: int | None = None
        self._last_kernel: int | None = None
        self._last_user: int | None = None

    def sample(self) -> tuple[float | None, str]:
        if not hasattr(ctypes, "windll"):
            return None, "Native CPU load unavailable on this platform"

        idle = _FileTime()
        kernel = _FileTime()
        user = _FileTime()
        try:
            ok = ctypes.windll.kernel32.GetSystemTimes(
                ctypes.byref(idle),
                ctypes.byref(kernel),
                ctypes.byref(user),
            )
        except Exception:
            return None, "Native CPU load provider unavailable"

        if not ok:
            return None, "Native CPU load provider unavailable"

        idle_value = _filetime_to_int(idle)
        kernel_value = _filetime_to_int(kernel)
        user_value = _filetime_to_int(user)

        if self._last_idle is None or self._last_kernel is None or self._last_user is None:
            self._last_idle = idle_value
            self._last_kernel = kernel_value
            self._last_user = user_value
            return None, "Native CPU load provider warming"

        idle_delta = idle_value - self._last_idle
        kernel_delta = kernel_value - self._last_kernel
        user_delta = user_value - self._last_user
        self._last_idle = idle_value
        self._last_kernel = kernel_value
        self._last_user = user_value

        total = kernel_delta + user_delta
        if total <= 0:
            return None, "Native CPU load sample unavailable"

        busy = max(0, total - idle_delta)
        return max(0.0, min(100.0, busy * 100.0 / total)), "Native Windows CPU load"


_CPU_LOAD_PROBE = NativeCpuLoadProbe()


@dataclass(frozen=True)
class MonitoringHudSource:
    label: str
    value: str
    source: str

    def as_dict(self) -> dict[str, str]:
        return {
            "label": self.label,
            "value": self.value,
            "source": self.source,
        }


@dataclass(frozen=True)
class MonitoringHudSensor:
    sensor_id: str
    label: str
    value: str
    source: str
    state: str

    def as_dict(self) -> dict[str, str]:
        return {
            "id": self.sensor_id,
            "label": self.label,
            "value": self.value,
            "source": self.source,
            "state": self.state,
        }


@dataclass(frozen=True)
class MonitoringHudCard:
    card_id: str
    label: str
    summary: str
    badge: str
    meta: str
    state: str
    sensors: tuple[MonitoringHudSensor, ...]

    def as_dict(self) -> dict[str, object]:
        return {
            "id": self.card_id,
            "label": self.label,
            "summary": self.summary,
            "badge": self.badge,
            "meta": self.meta,
            "state": self.state,
            "sensors": [sensor.as_dict() for sensor in self.sensors],
        }


@dataclass(frozen=True)
class MonitoringHudTelemetrySnapshot:
    package_id: str
    slice_id: str
    adapter_id: str
    adapter_status: str
    source_scope: str
    hardware_polling: str
    provider_state: str
    provider_label: str
    live_values: str
    polling_rate_ms: int
    sources: tuple[MonitoringHudSource, ...]
    sensor_cards: tuple[MonitoringHudCard, ...]

    def as_dict(self) -> dict[str, object]:
        return {
            "packageId": self.package_id,
            "sliceId": self.slice_id,
            "adapterId": self.adapter_id,
            "adapterStatus": self.adapter_status,
            "sourceScope": self.source_scope,
            "hardwarePolling": self.hardware_polling,
            "providerState": self.provider_state,
            "providerLabel": self.provider_label,
            "liveValues": self.live_values,
            "pollingRateMs": self.polling_rate_ms,
            "sources": [source.as_dict() for source in self.sources],
            "sensorCards": [card.as_dict() for card in self.sensor_cards],
        }


def _yes_no(value: bool) -> str:
    return "yes" if value else "no"


def build_monitoring_hud_telemetry_snapshot(
    *,
    page_ready: bool,
    desktop_mode: bool,
    runtime_log_path: str = "",
    event_route_present: bool = False,
    polling_rate_ms: int = DEFAULT_POLLING_RATE_MS,
) -> MonitoringHudTelemetrySnapshot:
    """Build a HUD-ready runtime snapshot without fake hardware values."""

    runtime_log = os.path.abspath(runtime_log_path) if runtime_log_path else ""
    runtime_log_label = "runtime log route present" if runtime_log else "runtime log route not supplied"
    event_route_label = "event route present" if event_route_present else "event route not supplied"
    safe_polling_rate = max(MINIMUM_SAFE_POLLING_RATE_MS, int(polling_rate_ms or DEFAULT_POLLING_RATE_MS))
    cpu_load, cpu_source = _CPU_LOAD_PROBE.sample()
    cpu_load_ready = cpu_load is not None
    cpu_load_value = f"{cpu_load:.0f}%" if cpu_load_ready else "Warming up"
    cpu_state = "ready" if cpu_load_ready else "setup"
    provider_state = "native-partial" if cpu_load_ready else "setup-required"
    provider_label = "Native CPU load active; thermal/GPU provider pending" if cpu_load_ready else "Provider setup required"
    hardware_polling = (
        f"Native CPU load sampled at {safe_polling_rate // 1000}s; thermal/GPU provider unavailable"
        if cpu_load_ready
        else f"Native CPU load warming at {safe_polling_rate // 1000}s; thermal/GPU provider unavailable"
    )
    live_values = "native-cpu-load-only" if cpu_load_ready else "provider-required"

    return MonitoringHudTelemetrySnapshot(
        package_id=PACKAGE_ID,
        slice_id=SLICE_ID,
        adapter_id=ADAPTER_ID,
        adapter_status="Provider contract boundary ready; native CPU load proof bounded",
        source_scope="Provider-contract-first local runtime readiness plus native CPU load",
        hardware_polling=hardware_polling,
        provider_state=provider_state,
        provider_label=provider_label,
        live_values=live_values,
        polling_rate_ms=safe_polling_rate,
        sources=(
            MonitoringHudSource("Visual page", "ready" if page_ready else "loading", "renderer page state"),
            MonitoringHudSource("Desktop surface", "enabled" if desktop_mode else "pending", "desktop mode flag"),
            MonitoringHudSource("Runtime log", runtime_log_label, "runtime log path"),
            MonitoringHudSource("Event route", event_route_label, "renderer event logger"),
            MonitoringHudSource("CPU load", "ready" if cpu_load_ready else "warming", cpu_source),
        ),
        sensor_cards=(
            MonitoringHudCard(
                card_id="cpu",
                label="CPU",
                summary=cpu_load_value if cpu_load_ready else "Provider warming",
                badge="Ready" if cpu_load_ready else "Setup",
                meta=(
                    "Native CPU load is real; CPU thermal waits for a validated provider."
                    if cpu_load_ready
                    else "Native CPU load warms first; CPU thermal waits for a validated provider."
                ),
                state=cpu_state,
                sensors=(
                    MonitoringHudSensor(
                        sensor_id="cpu-load",
                        label="CPU Load",
                        value=cpu_load_value,
                        source=cpu_source,
                        state="native-live" if cpu_load_ready else "native-provider-pending",
                    ),
                    MonitoringHudSensor(
                        sensor_id="cpu-thermal",
                        label="CPU Thermal",
                        value="Provider required",
                        source="Thermal source pending",
                        state="blocked-until-provider",
                    ),
                ),
            ),
            MonitoringHudCard(
                card_id="gpu",
                label="GPU",
                summary="Provider required",
                badge="No data",
                meta="GPU load and thermal values require a validated provider route.",
                state="no-data",
                sensors=(
                    MonitoringHudSensor(
                        sensor_id="gpu-load",
                        label="GPU Load",
                        value="Unavailable",
                        source="GPU source pending",
                        state="blocked-until-provider",
                    ),
                    MonitoringHudSensor(
                        sensor_id="gpu-thermal",
                        label="GPU Thermal",
                        value="Unavailable",
                        source="Thermal source pending",
                        state="blocked-until-provider",
                    ),
                ),
            ),
        ),
    )
