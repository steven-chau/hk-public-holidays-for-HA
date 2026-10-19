"""Config flow for the Hong Kong public holiday integration."""

from __future__ import annotations

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow

from .const import DOMAIN


class HkPublicHolidayConfigFlow(ConfigFlow, domain=DOMAIN):
    """Config flow with a single confirmation step and no options."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if self._async_current_entries():
            return self.async_abort(reason="already_configured")
        if user_input is not None:
            return self.async_create_entry(title="Hong Kong Public Holiday", data={})
        return self.async_show_form(step_id="user", data_schema=vol.Schema({}))
