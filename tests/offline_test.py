import json
import mock
from time import time
import unittest


from base_class import TestIPDetailsCacheBaseTests
from pierky.ipdetailscache import IPDetailsCache


class TestIPDetailsCache(TestIPDetailsCacheBaseTests):
    LIVE = False

    def setup_ixps(self, whenuse):

        def fetch_ixps_info(self):
            return None

        self.mock_fetch_ixps = mock.patch.object(
            IPDetailsCache,
            "FetchIXPsInfo",
            autospec=True
        ).start()
        self.mock_fetch_ixps.side_effect = fetch_ixps_info

        def load_ixps(self, cache_file):
            with open("tests/data/ixps.json", "r") as f:
                data = json.loads(f.read())
                data["TS"] = int(time())
                self.IXPsCache = data

        self.mock_load_ixps = mock.patch.object(
            IPDetailsCache,
            "LoadIXPsCache",
            autospec=True
        ).start()
        self.mock_load_ixps.side_effect = load_ixps

        self.cache.UseIXPs(
            WhenUse=whenuse,
            IXP_CACHE_FILE=None
        )

    def test_ixps_whenuse1_notannounced(self):
        """IXPs info, WhenUse = 1, IP not announced"""
        self.setup_ixps(1)
        ip = self.cache.GetIPInformation(self.IXPS_NOT_ANNOUNCED_IP)

        self.assertEquals(ip["ASN"], "not announced")
        self.verify_fetchipinfo_calls(1)
        self.assertEquals(ip["IsIXP"], True)
        self.assertEquals(ip["IXPName"], self.IXPS_NOT_ANNOUNCED_IP_IXPNAME)

        ip = self.cache.GetIPInformation(self.IXPS_NOT_ANNOUNCED_IP)
        self.verify_fetchipinfo_calls(1)

    def test_ixps_whenuse1_announced(self):
        """IXPs info, WhenUse = 1, announced IP"""
        self.setup_ixps(1)
        ip = self.cache.GetIPInformation(self.IXPS_ANNOUNCED_IP)

        self.assertEquals(ip["ASN"], self.IXPS_ANNOUNCED_IP_ASN)
        self.verify_fetchipinfo_calls(1)
        self.assertIsNone(ip["IsIXP"])

    def test_ixps_whenuse2_notannounced(self):
        """IXPs info, WhenUse = 2, IP not announced"""
        self.setup_ixps(2)
        ip = self.cache.GetIPInformation(self.IXPS_NOT_ANNOUNCED_IP)

        self.assertEquals(ip["ASN"], "not announced")
        self.verify_fetchipinfo_calls(1)
        self.assertEquals(ip["IsIXP"], True)
        self.assertEquals(ip["IXPName"], self.IXPS_NOT_ANNOUNCED_IP_IXPNAME)

        ip = self.cache.GetIPInformation(self.IXPS_NOT_ANNOUNCED_IP)
        self.verify_fetchipinfo_calls(1)
    
    def test_ixps_whenuse2_announced(self):
        """IXPs info, WhenUse = 2, announced IP"""
        self.setup_ixps(2)
        ip = self.cache.GetIPInformation(self.IXPS_ANNOUNCED_IP)

        self.assertEquals(ip["ASN"], self.IXPS_ANNOUNCED_IP_ASN)
        self.verify_fetchipinfo_calls(1)
        self.assertEquals(ip["IsIXP"], True)
        self.assertEquals(ip["IXPName"], self.IXPS_ANNOUNCED_IP_IXPNAME)

    def test_ixps_whenuse2_announced_not_ixp(self):
        """IXPs info, WhenUse = 2, announced IP, not an IXP"""
        self.setup_ixps(2)
        ip = self.cache.GetIPInformation(self.IP)

        self.assertEquals(ip["ASN"], self.ASN)
        self.assertEquals(ip["Prefix"], self.PREFIX)
        self.assertEquals(ip["Holder"], self.HOLDER)
        self.assertEquals(ip["IsIXP"], False)
        self.verify_fetchipinfo_calls(1)

    def test_ixps_whenuse0_notannounced(self):
        """IXPs info, WhenUse = 0, IP not announced"""
        self.setup_ixps(0)
        ip = self.cache.GetIPInformation(self.IXPS_NOT_ANNOUNCED_IP)

        self.assertEquals(ip["ASN"], "not announced")
        self.verify_fetchipinfo_calls(1)
        self.assertIsNone(ip["IsIXP"])

        ip = self.cache.GetIPInformation(self.IXPS_NOT_ANNOUNCED_IP)
        self.verify_fetchipinfo_calls(1)

    def test_ixps_whenuse0then1_notannounced(self):
        """IXPs info, WhenUse = 0, then WhenUse = 1, IP not announced"""
        self.setup_ixps(0)
        ip = self.cache.GetIPInformation(self.IXPS_NOT_ANNOUNCED_IP)

        self.assertEquals(ip["ASN"], "not announced")
        self.verify_fetchipinfo_calls(1)
        self.assertIsNone(ip["IsIXP"])

        self.cache.UseIXPs(
            WhenUse=1,
            IXP_CACHE_FILE=None
        )
        ip = self.cache.GetIPInformation(self.IXPS_NOT_ANNOUNCED_IP)

        self.assertEquals(ip["ASN"], "not announced")
        self.verify_fetchipinfo_calls(1)
        self.assertEquals(ip["IsIXP"], True)
        self.assertEquals(ip["IXPName"], self.IXPS_NOT_ANNOUNCED_IP_IXPNAME)

    def test_ixps_whenuse1then0_notannounced(self):
        """IXPs info, WhenUse = 1, then WhenUse = 0, IP not announced"""
        self.setup_ixps(1)
        ip = self.cache.GetIPInformation(self.IXPS_NOT_ANNOUNCED_IP)

        self.assertEquals(ip["ASN"], "not announced")
        self.verify_fetchipinfo_calls(1)
        self.assertEquals(ip["IsIXP"], True)
        self.assertEquals(ip["IXPName"], self.IXPS_NOT_ANNOUNCED_IP_IXPNAME)

        self.cache.UseIXPs(
            WhenUse=0,
            IXP_CACHE_FILE=None
        )
        ip = self.cache.GetIPInformation(self.IXPS_NOT_ANNOUNCED_IP)

        self.assertEquals(ip["ASN"], "not announced")
        self.verify_fetchipinfo_calls(1)
        self.assertEquals(ip["IsIXP"], True)
        self.assertEquals(ip["IXPName"], self.IXPS_NOT_ANNOUNCED_IP_IXPNAME)

    def test_ixps_whenuse1_notannounced_cached_prefix(self):
        """IXPs info, WhenUse = 1, IP not announced, cached prefix"""
        self.setup_ixps(1)
        ip = self.cache.GetIPInformation(self.IXPS_NOT_ANNOUNCED_IP)

        self.assertEquals(ip["ASN"], "not announced")
        self.verify_fetchipinfo_calls(1)
        self.assertEquals(ip["IsIXP"], True)

        # Invalidate addresses cache and verify if IP address info
        # obtained from prefixes cache contain the IXP info
        for k in self.cache.IPAddressesCache.keys():
            self.cache.IPAddressesCache[k]["TS"] = 0

        ip = self.cache.GetIPInformation(self.IXPS_NOT_ANNOUNCED_IP)

        self.assertEquals(ip["ASN"], "not announced")
        self.assertEquals(ip["IsIXP"], True)
        self.verify_fetchipinfo_calls(1)
