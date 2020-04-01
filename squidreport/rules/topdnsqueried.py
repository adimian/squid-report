from . import BaseRule
from .scraping import uniq_sort_list
from .read_log_file import get_dns_file


def extract_dns_list_log(df):
    dns_list = []
    for dns in df["query"]:
        dns_list.append(dns)
    return dns_list


def verifiy_dns(receive_dns_list_log):
    top_urls = uniq_sort_list()
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


class TopDNSQueriedRule(BaseRule):

    TRIGGER_TRESHOLD = 10

    @property
    def code(self):
        return "TOPDNS"

    def evaluate(self):
        df = get_dns_file(self.config)
        logs_list = extract_dns_list_log(df)
        validate_list = verifiy_dns(logs_list)
        logs_without_local = delete_local_site(logs_list)
        ratio = calculate_found_addresses_ratio(
            validate_list, logs_without_local
        )

        if ratio > self.TRIGGER_TRESHOLD:
            self.alert(ratio=ratio, max=self.TRIGGER_TRESHOLD)
