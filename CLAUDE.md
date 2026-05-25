# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

Home Assistant custom integration for Shandong TownGas (山东港华燃气) gas meter reading. Available via HACS. Queries the Shandong TownGas WeChat H5 API to fetch cumulative gas usage (m³) and exposes it to the HA energy dashboard.

## Architecture

Standard HA integration structure under `custom_components/shandongtowngas/`:

- **`__init__.py`** — Entry point. Creates a `TownGasApi` instance and a `DataUpdateCoordinator`, then forwards setup to sensor/button platforms. The coordinator's `_update` function calls `api.pre_check(subs_id)` to fetch meter data.
- **`api.py`** — Async HTTP client (`aiohttp`) wrapping the TownGas VCC API. Handles OAuth (WeChat QR → authCode → access/refresh token), token refresh with MD5-signed requests, and the business endpoint (`/charge/preCheck`). SSL verification is disabled (self-signed upstream cert).
- **`config_flow.py`** — Two-step config flow: (1) show WeChat OAuth QR code, (2) user pastes authCode + subsId/subsCode. Also handles reauth when tokens are permanently invalid. Options flow lets user adjust scan/token refresh intervals.
- **`sensor.py`** — `TownGasMeterSensor` (CoordinatorEntity): exposes currReading as a `TOTAL_INCREASING` gas sensor in m³ with extra state attributes (subsName, subsAddr, bill details, next refresh times).
- **`button.py`** — `TownGasRefreshButton`: triggers `coordinator.async_request_refresh()` on press.
- **`const.py`** — Domain name, config keys, defaults, API host/credentials/salt.
- **`strings.json` / `translations/`** — UI strings (Chinese in `zh-Hans.json`, English in `en.json`).

### Two-timer pattern

Data refresh and token refresh are decoupled:
- **Data fetch** runs on `scan_interval` (default 21600s / 6h) via the coordinator.
- **Token refresh** runs on its own independent `async_call_later` one-shot timer (default 1800s / 30min). The next refresh is always scheduled `min(interval, bearer_remain - 60)` seconds ahead. If the token is already expired at data-fetch time, there's a safety-net refresh.
- This avoids coupling token lifetime to the data polling cadence.

### Maintenance window

Daily 23:30–00:30 CST, the coordinator skips data fetches (API is down for maintenance). Sensors hold their last known value. Token refresh is unaffected.

### Token persistence

After every successful token refresh or data fetch, `_persist_tokens` writes the current access/refresh token pair back into the config entry via `async_update_entry`, so tokens survive HA restarts.

### Auth failure → reauth

If `refresh_access_token` returns a definitive error code (not a network failure), `AuthError` is raised. The coordinator converts this to `ConfigEntryAuthFailed`, which triggers HA's reauth flow — user re-scans WeChat QR to get fresh tokens.

## Commands

There is no build step, test suite, or linter config in this project. To test changes:

1. Copy/symlink `custom_components/shandongtowngas/` into a running HA instance's `config/custom_components/`
2. Restart HA (`ha core restart` or via UI)
3. Add the integration via **Settings → Devices & Services → Add Integration → 山东港华燃气**

## Release

Tag a `v*` commit and push — the GitHub Actions workflow in `.github/workflows/release.yml` packages `custom_components/shandongtowngas/` as `shandongtowngas.zip` and creates a GitHub Release for HACS.