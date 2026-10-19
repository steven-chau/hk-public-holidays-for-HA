# Hong Kong Public Holiday for Home Assistant

A minimal [Home Assistant](https://www.home-assistant.io/) integration that adds a binary sensor which is `on` when the current day is a public holiday in Hong Kong and `off` otherwise.

- Data source: the [Hong Kong government (1823)](https://www.1823.gov.hk/en/statutory-holidays) holiday calendar, via [data.gov.hk](https://data.gov.hk/en-data/dataset/hk-dpo-statistic-cal).
- The holiday list is downloaded when Home Assistant starts and refreshed every year on 30 December, when the data for the following year is published.
- "Today" is evaluated in Hong Kong time (`Asia/Hong_Kong`), regardless of where Home Assistant runs.
- When the sensor is `on`, the `holiday_name` attribute contains the name of the holiday.

## Installation

### Via HACS

1. Make sure [HACS](https://hacs.xyz/) is installed.
2. In HACS, add this repository as a **custom repository** of category *Integration*.
3. Search for and install **Hong Kong Public Holiday**, then restart Home Assistant.
4. Go to **Settings → Devices & Services → Add Integration** and select **Hong Kong Public Holiday**. Confirm the prompt (no configuration is needed).

### Manual

Copy the `custom_components/hk_public_holiday` folder into the `custom_components` folder of your Home Assistant installation, restart Home Assistant, then add the integration via **Settings → Devices & Services** as described above.

## Sensor

The integration creates the binary sensor `binary_sensor.hong_kong_public_holiday`.

| State | Meaning |
|-------|---------|
| `on`  | Today is a public holiday in Hong Kong |
| `off` | Today is not a public holiday in Hong Kong |

| Attribute      | Description                                        |
|----------------|----------------------------------------------------|
| `holiday_name` | Name of today's holiday (present when `on`)        |
