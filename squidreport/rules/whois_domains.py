from socket import gaierror
import time
from .topdnsqueried import verifiy_dns
from .library.read_log_file import get_known_hosts_file, get_conn_file
import arrow
from . import BaseRule


def get_host_list(dataframe_known_host):
    known_hosts_list = list(dataframe_known_host["host"])
    return known_hosts_list


def get_ip_resp_list(dataframe_connections):
    id_resp_list = list(dataframe_connections["id_resp_h"])
    return id_resp_list


def soustract_ip_list_by_known_host_list(id_resp_list, known_hosts_list):
    ip_list_without_known_host = set(set(id_resp_list) - set(known_hosts_list))
    return ip_list_without_known_host


def found_info_name_servers(ip_list_without_known_host):
    from whois import whois
    from whois.parser import PywhoisError

    ip_ts_name_server_dict = {}
    for ip in set(ip_list_without_known_host):
        try:
            w = whois(ip)
            if w.creation_date is not None:
                ip_ts_name_server_dict.setdefault(ip, {})
                list_ts = []
                if isinstance(w.creation_date, list):
                    for date in w.creation_date:
                        list_ts.append(arrow.get(date).timestamp)
                else:
                    list_ts.append(arrow.get(w.creation_date).timestamp)
                ts_name_server_dict = {
                    "timestamp": list_ts,
                    "name_server": set(w.name_servers),
                }
                ip_ts_name_server_dict[ip].update(ts_name_server_dict)
            time.sleep(1)

        except PywhoisError:
            # if domain name doesn't exist by example for .net or .com
            pass
        except gaierror:
            # it's a problem with sockets
            pass
        except ConnectionRefusedError:
            # bad internet connection or firewall blocking whois requests
            pass

    return ip_ts_name_server_dict


def calculate_time_not_valide_new_domains(now=None):
    if now is None:
        now = arrow.now()
    limit = now.shift(months=-3).timestamp
    return limit


def compare_domain_name_with_dns_scraping(dns_list):
    return len(verifiy_dns(dns_list)), len(dns_list)


def compare_creation_domain_with_actual_date(data):
    date_ts = calculate_time_not_valide_new_domains()
    name_server_list = []
    count_new_domains = 0
    count_domains = 0

    for k in data:
        value = data[k]
        for ts in value["timestamp"]:
            count_domains += 1
            if date_ts > ts:
                pass
            elif date_ts < ts or date_ts == ts:
                count_new_domains += 1
                name_server_list = list(value["name_server"])
    return dict(
        {
            "nb_domains": count_domains,
            "nb_new_domains": count_new_domains,
            "name_server": name_server_list,
        }
    )


def calculate_ratio(total_domains, new_domains):
    return (new_domains * 100) / total_domains


class WhoIsDomainsRule(BaseRule):
    @property
    def code(self):
        return "WHOISDOMAINS"

    def evaluate(self):
        ip_list = get_ip_resp_list(get_conn_file(self.config))
        host_list = get_host_list(get_known_hosts_file(self.config))
        final_list = soustract_ip_list_by_known_host_list(ip_list, host_list)
        dict_info = compare_creation_domain_with_actual_date(
            found_info_name_servers(final_list)
        )

        dns_in_top_list, dns_suspect = compare_domain_name_with_dns_scraping(
            dict_info["name_server"]
        )

        if dns_in_top_list != dns_suspect:
            ratio = calculate_ratio(
                dict_info["nb_domains"], dict_info["nb_new_domains"]
            )
            self.alert(ratio=int(ratio))
