from dataclasses import dataclass
from zoneinfo import ZoneInfo


@dataclass(frozen=True)
class DashboardConfig:
    symbol: str = "FDAX.EX"
    fallback_symbols: tuple[str, ...] = ("DAX", "^GDAXI")
    interval: str = "5m"
    period: str = "60d"
    timezone: str = "Europe/Berlin"
    rolling_daily_window: int = 252
    rolling_weekly_window: int = 104
    rolling_monthly_window: int = 60

    @property
    def tzinfo(self) -> ZoneInfo:
        return ZoneInfo(self.timezone)


DEFAULT_CONFIG = DashboardConfig()
