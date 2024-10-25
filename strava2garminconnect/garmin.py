# SPDX-FileCopyrightText: 2024 Steffen Vogel <post@steffenvogel.de>
# SPDX-License-Identifier: Apache-2.0

import io
import logging
import os
import time
from requests import HTTPError
from urllib import request

from urllib import parse
from garminconnect import Garmin as GarminClient, GarminConnectAuthenticationError
from garth.http import GarthHTTPError
from strava2garminconnect import image

class DuplicateActivityPhoto(Exception):
    
    def __init__(self, photo):
        self.photo = photo

    def __str__(self):
        return f"Photo already exists (id={self.photo['imageId']})"


class DuplicateActivityError(Exception):

    def __init__(self, e: HTTPError):
        self.error = e

    def __str__(self):
        return f"Failed to upload activity. Already exists (id={self.activity_id})"

    @property
    def activity_id(self):
        return self.__activity_id_from_error(self.error)

    @classmethod
    def __activity_id_from_error(cls, e: HTTPError):
        r = e.response.json()
        return r["detailedImportResult"]["failures"][0]["internalId"]

    @classmethod
    def is_valid(cls, e: GarthHTTPError) -> bool:
        if e.error.response.status_code != 409:
            return False

        try:
            cls.__activity_id_from_error(e.error)
            return True
        except:
            return False


class Client(GarminClient):

    def __init__(self, tokens: str, email: str, password: str, get_mfa):
        tokens = os.path.join(tokens, "garmin")

        try:
            super().__init__()
            self.login(tokens)

        except (FileNotFoundError, GarthHTTPError, GarminConnectAuthenticationError):
            super().__init__(
                email=email, password=password, is_cn=False, prompt_mfa=get_mfa
            )
            self.login()
            self.garth.dump(tokens)

    def upload_activity(self, name: str, content: bytes):
        files = {
            "file": ("upload.fit", io.BytesIO(content)),
        }

        try:
            resp = self.garth.post(
                "connectapi", "upload-service/upload/.fit", files=files, api=True
            )
        except GarthHTTPError as e:
            if DuplicateActivityError.is_valid(e):
                raise DuplicateActivityError(e.error)
            else:
                raise e

        location = parse.urlparse(resp.headers["location"])

        attempts = 0
        while True:
            try:
                resp = self.garth.get(
                    "connectapi",
                    location.path,
                    api=True,
                    headers={"Accept": "application/json"},
                )
                if resp.status_code == 201:
                    activity_status = resp.json()
                    activity_id = activity_status["detailedImportResult"]["successes"][
                        0
                    ]["internalId"]

                    return activity_id

            except GarthHTTPError as e:
                logging.error("Failed to get status: %s", e)

                if attempts > 5:
                    raise RuntimeError("Attempts exhausted")

            time.sleep(1)
            attempts += 1

    def upload_photo(self, activity_id: int, content: bytes):
        files = {
            "file": ("image.png", io.BytesIO(content)),
        }

        self.garth.post(
            "connectapi",
            f"activity-service/activity/{activity_id}/image",
            files=files,
            api=True,
        )

    def upload_photo_check_duplicate(self, activity_id: int, content: bytes, existing_photos = []):
        if len(existing_photos) == 0:
            activity = self.get_activity(activity_id)
            existing_photos += [i for i in activity["metadataDTO"]["activityImages"]]

        for existing_photo in existing_photos:
            if "content" not in existing_photo:
                resp = request.urlopen(existing_photo["url"])
                existing_photo["content"] = resp.read()

            existing_content = existing_photo["content"]

            if image.is_equal_bytes(existing_content, content, 5):
                raise DuplicateActivityPhoto(existing_photo)

        self.upload_photo(activity_id, content)    


    def link_activity_gear(self, activity_id, gear_uuid: str):
        """Link gear to activity with id."""

        url = f"/gear-service/gear/link/{gear_uuid}/activity/{activity_id}"
        return self.garth.put("connectapi", url, api=True)

    def unlink_activity_gear(self, activity_id, gear_uuid: str):
        """Unlink gear to activity with id."""

        url = f"/gear-service/gear/unlink/{gear_uuid}/activity/{activity_id}"
        return self.garth.put("connectapi", url, api=True)

    def set_activity_gear(self, activity_id, gear_uuid):
        found = False
        for gear in self.get_activity_gear(activity_id):
            if gear["uuid"] == gear_uuid:
                found = True
                continue

            self.unlink_activity_gear(activity_id, gear["uuid"])

        if not found:
            self.link_activity_gear(activity_id, gear_uuid)
