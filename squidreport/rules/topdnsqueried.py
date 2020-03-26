import pandas as pd
import os

from . import BaseRule
from .scraping import uniq_sort_list

columns_conn = [
    "ts",
    "uid",
    "id.orig_h",
    "id.orig_p",
    "id.resp_h",
    "id.resp_p",
    "proto",
    "trans_id",
    "rtt",
    "query",
    "qclass",
    "qclass_name",
    "qtype",
    "qtype_name",
    "rcode",
    "rcode_name",
    "AA",
    "TC",
    "RD",
    "RA",
    "Z",
    "answers",
    "TTLs",
    "rejected",
]


def extract_dns_list_log(df):
    dns_list = []
    for dns in df["query"]:
        dns_list.append(dns)
    return dns_list


def verifiy_dns(receive_dns_list_log, top_urls):
    validate_dns_list = []
    for url in top_urls:
        for log in receive_dns_list_log:
            if url in log:
                validate_dns_list.append(log)
    return validate_dns_list


def calculate_found_addresses_ratio(found_list, dns_list):
    calculation = len(found_list) / len(dns_list)
    calculation = round(calculation * 100, 2)
    return calculation


def delete_local_site(log_list):
    log_list_whitout_local = []
    first_char = "_"
    for log in log_list:
        if not log.startswith(first_char):
            log_list_whitout_local.append(log)
    return log_list_whitout_local


def read_dns_log_file(config):
    return pd.read_csv(
        os.path.join(config.ZEEK_LOGS_DIRECTORY, "dns.log"),
        sep="\t",
        comment="#",
        names=columns_conn,
    )


class TopDNSQueriedRule(BaseRule):
    @property
    def code(self):
        return "TOPDNS"

    def evaluate(self):
        top_urls = uniq_sort_list()
        df = read_dns_log_file(self.config)
        logs_list = extract_dns_list_log(df)
        validate_list = verifiy_dns(logs_list, top_urls)
        logs_without_local = delete_local_site(logs_list)
        ratio = calculate_found_addresses_ratio(
            validate_list, logs_without_local
        )

        if ratio > 0.5:
            self.alert()
