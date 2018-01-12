#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import re
import hashlib
from requests.compat import urljoin
from requests.utils import dict_from_cookiejar

from sickbeard import logger, tvcache
from sickrage.providers.torrent.TorrentProvider import TorrentProvider


class FuzerProvider(TorrentProvider):  # pylint: disable=too-many-instance-attributes

    def __init__(self):

        # Provider Init
        TorrentProvider.__init__(self, "FuzerProvider")

        # Credentials
        self.username = None
        self.password = None

        # Torrent Stats
        self.minseed = None
        self.minleech = None

        # URLs
        self.url = "https://www.fuzer.me"
        self.urls = {
            "login": urljoin(self.url, "login.php"),
            "search": urljoin(self.url, "browse.php"),
        }

        # Proper Strings
        self.proper_strings = ["PROPER", "REPACK"]

        # Cache
        self.cache = tvcache.TVCache(self)

    def login(self):
        if any(dict_from_cookiejar(self.session.cookies).values()):
            return True

        login_params = {
            "vb_login_username": self.username.encode("utf-8"),
            "vb_login_password": '',
            "cookieuser": 1,
            "s": '',
            "securitytoken": 'guest',
            "vb_login_md5password": hashlib.md5(self.password.encode("utf-8").hexdigest()),
            "vb_login_md5password_utf": hashlib.md5(self.password.encode("utf-8").hexdigest()),
        }

        response = self.get_url(self.urls["login"] + "?do=login", post_data=login_params, returns="text")
        if not response:
            logger.log("Unable to connect to provider", logger.WARNING)
            return False

        if re.search('\xd7\x94\xd7\x94\xd7\xaa\xd7\x97\xd7\x91\xd7\xa8\xd7\x95\xd7\xaa \xd7\xa0\xd7\x9b\xd7\xa9\xd7\x9c\xd7\x94!', response, re.UNICODE):
            logger.log("Invalid username or password. Check your settings", logger.WARNING)
            return False

        return True
