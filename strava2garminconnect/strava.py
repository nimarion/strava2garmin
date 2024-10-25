# SPDX-FileCopyrightText: 2024 Steffen Vogel <post@steffenvogel.de>
# SPDX-License-Identifier: Apache-2.0

import os
import json
import logging
from datetime import datetime

import stravalib
import stravalib.client
from stravaweblib import WebClient as StravaWebClient
from stravalib import Client as StravaClient


class Client(StravaWebClient):
    def __init__(
        self,
        tokens: str,
        email: str,
        password: str,
        client_id: str,
        client_secret: str,
        get_code,
    ):
        tokens = os.path.join(tokens, "strava", "tokens.json")

        try:
            with open(tokens, "r") as f:
                token = json.load(f)

            expires_at = datetime.fromtimestamp(token["expires_at"])

            if expires_at < datetime.now():
                client = StravaClient()

                token = client.refresh_access_token(
                    client_id=client_id,
                    client_secret=client_secret,
                    refresh_token=token["refresh_token"],
                )

        except:
            c = StravaClient()

            url = c.authorization_url(
                client_id=client_id,
                redirect_uri="http://127.0.0.1:5000/authorization",
            )

            token = c.exchange_code_for_token(
                client_id=client_id, client_secret=client_secret, code=get_code(url)
            )

        if "jwt" in token:
            super().__init__(access_token=token["access_token"], jwt=token["jwt"])
        else:
            super().__init__(
                access_token=token["access_token"], email=email, password=password
            )

        token["jwt"] = self.jwt

        with open(tokens, "w+") as f:
            json.dump(token, f)

    def get_activity_photos(
        self, activity_id: int, size: str = "5000"
    ) -> stravalib.client.BatchedResultsIterator[stravalib.model.ActivityPhoto]:

        def result_fetcher(**kwargs):
            photos = self.protocol.get(
                "/activities/{id}/photos",
                id=activity_id,
                photo_sources="true",
                size=size,
                **kwargs,
            )

            for photo in photos:
                photo["created_at"] = photo["uploaded_at"]
                photo["created_at_local"] = photo["uploaded_at"]

            return photos

        return stravalib.client.BatchedResultsIterator(
            entity=stravalib.model.ActivityPhoto,
            bind_client=self,
            result_fetcher=result_fetcher,
        )
