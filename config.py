#!/usr/bin/env python
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
"""Configuration for the bot."""

import os


class DefaultConfig:
    """Configuration for the bot."""

    PORT = 3978
    # Configuration chat bot
    APP_ID = os.environ.get("MicrosoftAppId", "")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "")
    # Configuration Luis
    LUIS_APP_ID = os.environ.get("LuisAppId", "5a1ffd5c-f47a-49c7-8f17-2c91c3b53eab")
    LUIS_API_KEY = os.environ.get("LuisAPIKey", "ad25e2608a7b496ca39d639f74a0dcd8")
    LUIS_API_HOST_NAME = os.environ.get("LuisAPIHostName", "https://westeurope.api.cognitive.microsoft.com/")
    # Configuration app insights
    APPINSIGHTS_INSTRUMENTATION_KEY = os.environ.get("AppInsightsInstrumentationKey", "a519bfb1-ca03-4851-a37e-a3dd4e58b4df"  )
