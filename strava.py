# SPDX-FileCopyrightText: 2024 Steffen Vogel <post@steffenvogel.de>
# SPDX-License-Identifier: Apache-2.0

import stravalib
import stravalib.client
from stravaweblib import WebClient as StravaWebClient
from stravalib import Client as StravaClient


class Client(StravaWebClient):
    def __init__(
        self,
        refresh_token: str,
        email: str,
        password: str,
        client_id: str,
        client_secret: str,
    ):
        client = StravaClient()

        token = client.refresh_access_token(
                    client_id=client_id,
                    client_secret=client_secret,
                    refresh_token=refresh_token,
                )
        if "jwt" in token:
            super().__init__(access_token=token["access_token"], jwt=token["jwt"])
        else:
            super().__init__(
                access_token=token["access_token"], email=email, password=password
            )


    def get_activity_photos(
        self, activity_id: int, size: str = "5000"
    ):

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
