"""Config flow for TownGas Meter — two-step: get OAuth URL → paste authCode."""

from __future__ import annotations

import base64
from io import BytesIO
import logging
from typing import Any

import aiohttp
import qrcode
import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult, OptionsFlow
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import TownGasApi
from .const import (
    CONF_ACCESS_TOKEN,
    CONF_AUTH_CODE,
    CONF_REFRESH_TOKEN,
    CONF_SCAN_INTERVAL,
    CONF_SUBS_CODE,
    CONF_SUBS_ID,
    CONF_TOKEN_CREATE_TIME,
    CONF_TOKEN_EXPIRES_IN,
    CONF_TOKEN_REFRESH_INTERVAL,
    DEFAULT_SCAN_INTERVAL,
    DEFAULT_TOKEN_REFRESH_INTERVAL,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)


class TownGasConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for TownGas Meter."""

    VERSION = 1

    @staticmethod
    def async_get_options_flow(config_entry: Any) -> OptionsFlow:
        """Return the options flow handler."""
        return TownGasOptionsFlow(config_entry)

    def __init__(self) -> None:
        """Init flow."""
        self._oauth_url: str = ""

    def _oauth_qr_markdown(self) -> str:
        """Generate markdown image from OAuth URL QRCode."""
        if not self._oauth_url:
            return ""
        qr = qrcode.QRCode(border=2, box_size=5)
        qr.add_data(self._oauth_url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        buf = BytesIO()
        img.save(buf, format="PNG")
        b64 = base64.b64encode(buf.getvalue()).decode("ascii")
        return f"![oauth_qr](data:image/png;base64,{b64})"

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None,
    ) -> ConfigFlowResult:
        """Step 1: show OAuth QR link → user scans → goes to step 2."""
        if user_input is not None:
            return await self.async_step_auth()

        session = async_get_clientsession(self.hass, verify_ssl=False)
        api = TownGasApi(session)
        try:
            self._oauth_url = await api.get_oauth_url()
        except Exception:
            _LOGGER.exception("Failed to get OAuth URL")
            return self.async_abort(reason="oauth_url_failed")

        return self.async_show_form(
            step_id="user",
            description_placeholders={
                "oauth_url": self._oauth_url,
                "oauth_qr_markdown": self._oauth_qr_markdown(),
            },
            data_schema=vol.Schema({}),
        )

    async def async_step_auth(
        self, user_input: dict[str, Any] | None = None,
    ) -> ConfigFlowResult:
        """Step 2: user pastes authCode, we exchange for tokens."""
        errors: dict[str, str] = {}

        if user_input is not None:
            auth_code = user_input[CONF_AUTH_CODE].strip()
            for sep in ("authCode=", "code="):
                if sep in auth_code:
                    auth_code = auth_code.split(sep, 1)[1].split("&", 1)[0]
                    break

            session = async_get_clientsession(self.hass, verify_ssl=False)
            api = TownGasApi(session)
            try:
                data = await api.exchange_token(auth_code)
            except Exception:
                _LOGGER.exception("Token exchange failed")
                errors["base"] = "exchange_failed"
                data = {}

            if data.get("access_token"):
                subs_id = user_input[CONF_SUBS_ID].strip()
                subs_code = user_input[CONF_SUBS_CODE].strip()
                if not subs_id or not subs_code:
                    errors["base"] = "subs_required"
                else:
                    await self.async_set_unique_id(subs_id)
                    self._abort_if_unique_id_configured()
                    scan_interval = int(
                        user_input.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
                    )
                    title = f"港华燃气 {subs_code}"
                    token_refresh_interval = int(
                        user_input.get(CONF_TOKEN_REFRESH_INTERVAL, DEFAULT_TOKEN_REFRESH_INTERVAL)
                    )
                    return self.async_create_entry(
                        title=title,
                        data={
                            CONF_ACCESS_TOKEN: api.access_token,
                            CONF_REFRESH_TOKEN: api.refresh_token,
                            CONF_TOKEN_EXPIRES_IN: api.token_expires_in,
                            CONF_TOKEN_CREATE_TIME: api.token_create_time,
                            CONF_SUBS_ID: subs_id,
                            CONF_SUBS_CODE: subs_code,
                        },
                        options={
                            CONF_SCAN_INTERVAL: scan_interval,
                            CONF_TOKEN_REFRESH_INTERVAL: token_refresh_interval,
                        },
                    )
            if not errors:
                errors["base"] = "auth_failed"

        return self.async_show_form(
            step_id="auth",
            description_placeholders={
                "oauth_url": self._oauth_url,
                "oauth_qr_markdown": self._oauth_qr_markdown(),
            },
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_AUTH_CODE): str,
                    vol.Required(CONF_SUBS_ID): str,
                    vol.Required(CONF_SUBS_CODE): str,
                    vol.Optional(
                        CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL
                    ): vol.All(int, vol.Range(min=60, max=86400)),
                    vol.Optional(
                        CONF_TOKEN_REFRESH_INTERVAL, default=DEFAULT_TOKEN_REFRESH_INTERVAL
                    ): vol.All(int, vol.Range(min=300, max=7140)),
                }
            ),
            errors=errors,
        )

    # ------------------------------------------------------------------
    #  Re-authentication flow (triggered by ConfigEntryAuthFailed)
    # ------------------------------------------------------------------

    async def async_step_reauth(
        self, entry_data: dict[str, Any],
    ) -> ConfigFlowResult:
        """Start re-auth when the stored tokens are permanently invalid."""
        return await self.async_step_reauth_confirm()

    async def async_step_reauth_confirm(
        self, user_input: dict[str, Any] | None = None,
    ) -> ConfigFlowResult:
        """Step 1 of reauth: show a fresh OAuth QR code."""
        if user_input is not None:
            return await self.async_step_reauth_token()

        session = async_get_clientsession(self.hass, verify_ssl=False)
        api = TownGasApi(session)
        try:
            self._oauth_url = await api.get_oauth_url()
        except Exception:
            _LOGGER.exception("Reauth: failed to get OAuth URL")
            return self.async_abort(reason="oauth_url_failed")

        return self.async_show_form(
            step_id="reauth_confirm",
            description_placeholders={
                "oauth_url": self._oauth_url,
                "oauth_qr_markdown": self._oauth_qr_markdown(),
            },
            data_schema=vol.Schema({}),
        )

    async def async_step_reauth_token(
        self, user_input: dict[str, Any] | None = None,
    ) -> ConfigFlowResult:
        """Step 2 of reauth: exchange new authCode and update the entry."""
        errors: dict[str, str] = {}

        if user_input is not None:
            auth_code = user_input[CONF_AUTH_CODE].strip()
            for sep in ("authCode=", "code="):
                if sep in auth_code:
                    auth_code = auth_code.split(sep, 1)[1].split("&", 1)[0]
                    break

            session = async_get_clientsession(self.hass, verify_ssl=False)
            api = TownGasApi(session)
            try:
                data = await api.exchange_token(auth_code)
            except Exception:
                _LOGGER.exception("Reauth: token exchange failed")
                errors["base"] = "exchange_failed"
                data = {}

            if data.get("access_token"):
                entry = self._get_reauth_entry()
                new_data = {
                    **entry.data,
                    CONF_ACCESS_TOKEN: api.access_token,
                    CONF_REFRESH_TOKEN: api.refresh_token,
                    CONF_TOKEN_EXPIRES_IN: api.token_expires_in,
                    CONF_TOKEN_CREATE_TIME: api.token_create_time,
                }
                return self.async_update_reload_and_abort(entry, data=new_data)

            if not errors:
                errors["base"] = "auth_failed"

        return self.async_show_form(
            step_id="reauth_token",
            description_placeholders={
                "oauth_url": self._oauth_url,
                "oauth_qr_markdown": self._oauth_qr_markdown(),
            },
            data_schema=vol.Schema({vol.Required(CONF_AUTH_CODE): str}),
            errors=errors,
        )


class TownGasOptionsFlow(OptionsFlow):
    """Options flow — lets the user change scan_interval after setup."""

    def __init__(self, config_entry: Any) -> None:
        self._entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None,
    ) -> ConfigFlowResult:
        """Show the options form."""
        if user_input is not None:
            return self.async_create_entry(
                title="",
                data={
                    CONF_SCAN_INTERVAL: user_input[CONF_SCAN_INTERVAL],
                    CONF_TOKEN_REFRESH_INTERVAL: user_input[CONF_TOKEN_REFRESH_INTERVAL],
                },
            )

        current_scan = self._entry.options.get(
            CONF_SCAN_INTERVAL,
            self._entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL),
        )
        current_token = self._entry.options.get(
            CONF_TOKEN_REFRESH_INTERVAL,
            self._entry.data.get(CONF_TOKEN_REFRESH_INTERVAL, DEFAULT_TOKEN_REFRESH_INTERVAL),
        )
        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional(CONF_SCAN_INTERVAL, default=current_scan): vol.All(
                        int, vol.Range(min=60, max=86400)
                    ),
                    vol.Optional(CONF_TOKEN_REFRESH_INTERVAL, default=current_token): vol.All(
                        int, vol.Range(min=300, max=7140)
                    ),
                }
            ),
        )
