import pandas as pd
import os.path


def get_dns_file(config):
    columns_dns_log = [
        "ts",
        "uid",
        "id_orig_h",
        "id_orig_p",
        "id_resp_h",
        "id_resp_p",
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
    dns_file = pd.read_csv(
        os.path.join(config.ZEEK_LOGS_DIRECTORY, "dns.log"),
        sep="\t",
        comment="#",
        names=columns_dns_log,
    )
    return dns_file


def get_conn_file(config):
    columns_conn_log = [
        "ts",
        "uid",
        "id_orig_h",
        "id_orig_p",
        "id_resp_h",
        "id_resp_p",
        "proto",
        "service",
        "duration",
        "orig_bytes",
        "resp_bytes",
        "conn_state",
        "local_orig",
        "local_resp",
        "missed_bytes",
        "history",
        "orig_pkts",
        "orig_ip_bytes",
        "resp_pkts",
        "resp_ip_bytes",
        "tunnel_parents",
    ]
    conn_file = pd.read_csv(
        os.path.join(config.ZEEK_LOGS_DIRECTORY, "conn.log"),
        sep="\t",
        comment="#",
        names=columns_conn_log,
    )
    return conn_file


def get_known_hosts_file(config):
    columns_known_hosts = ["ts", "host"]
    known_hosts_file = pd.read_csv(
        os.path.join(config.ZEEK_LOGS_DIRECTORY, "known_hosts.log"),
        sep="\t",
        comment="#",
        names=columns_known_hosts,
    )
    return known_hosts_file
