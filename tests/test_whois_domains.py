from mock import patch
import unittest
import arrow

import pandas as pd

from squidreport.rules.whois_domains import (
    get_host_list,
    get_ip_resp_list,
    soustract_ip_list_by_known_host_list,
    found_info_name_servers,
    compare_creation_domain_with_actual_date,
    compare_domain_name_with_dns_scraping,
    calculate_ratio,
    calculate_time_not_valide_new_domains,
)


class TestMyMethod(unittest.TestCase):

    maxDiff = None

    def test_get_host_list(self):
        data = {"ts": [1, 2], "host": ["192.168.10.1", "10.0.0.53"]}
        df = pd.DataFrame(data=data)

        expected = ["192.168.10.1", "10.0.0.53"]
        self.assertEqual(get_host_list(df), expected)

    def test_get_ip_list(self):
        data = {"ts": [1, 2], "id_resp_h": ["35.98.63.89", "152.78.02.83"]}
        df = pd.DataFrame(data=data)

        expected = ["35.98.63.89", "152.78.02.83"]
        self.assertEqual(get_ip_resp_list(df), expected)

    def test_soustract_ip_list_by_known_host_list(self):
        input_host = ["192.168.10.1", "10.0.0.53"]
        input_ip_resp = ["35.98.63.89", "152.78.02.83", "192.168.10.1"]
        expected = {"35.98.63.89", "152.78.02.83"}
        self.assertEqual(
            soustract_ip_list_by_known_host_list(input_ip_resp, input_host),
            expected,
        )

    @patch("whois.whois")
    def test_found_info_name_servers(self, mock_whois):
        class FakeWhoisResponse:
            name_servers = ["ns1.mydomain.local"]
            creation_date = ["2010-01-01 12:00:28", "2010-01-05 12:00:28"]

        ip = ["xxx:xxx:xxx:xxx::yyyy"]
        mock_whois.return_value = FakeWhoisResponse()
        result = found_info_name_servers(ip)

        expected = {
            "xxx:xxx:xxx:xxx::yyyy": {
                "timestamp": [1262347228, 1262692828],
                "name_server": {"ns1.mydomain.local"},
            }
        }

        self.assertDictEqual(result, expected)

    def test_calculate_time_not_valide_new_domains(self):
        input = arrow.get("2020-04-08T12:17:41.866935+02:00")
        expected = 1578478661

        self.assertEqual(
            calculate_time_not_valide_new_domains(now=input), expected
        )

    def test_compare_creation_domain_with_actual_date(self):
        input = {
            "2a00:1450:4007:808::2006": {
                "timestamp": [1253850003.0, 1253824803.0],
                "name_server": {
                    "NS1.GOOGLE.COM",
                    "NS2.GOOGLE.COM",
                    "NS3.GOOGLE.COM",
                    "NS4.GOOGLE.COM",
                    "ns4.google.com",
                    "ns2.google.com",
                    "ns3.google.com",
                    "ns1.google.com",
                },
            },
            "52.129.74.12": {
                "timestamp": [1047444129.0],
                "name_server": {
                    "NS1.P20.DYNECT.NET",
                    "NS2.P20.DYNECT.NET",
                    "NS3.P20.DYNECT.NET",
                    "NS4.P20.DYNECT.NET",
                },
            },
        }

        expected = {"name_server": [], "nb_domains": 3, "nb_new_domains": 0}

        self.assertEqual(
            compare_creation_domain_with_actual_date(input), expected
        )

    def test_compare_domain_name_with_dns_scraping(self):
        list_dns = ["dns.notexist.com", "dns49.notexist.com"]
        expected = (0, 2)
        self.assertEqual(
            compare_domain_name_with_dns_scraping(list_dns), expected
        )

    def test_calculate_ratio(self):
        total_domains = 10
        new_domains = 2
        expected = 20

        self.assertEqual(calculate_ratio(total_domains, new_domains), expected)
