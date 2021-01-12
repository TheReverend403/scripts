#!/usr/bin/env python3
import argparse
import errno
import logging as log
import socket
import subprocess
import sys
from ipaddress import ip_address


def shell(command):
    try:
        subprocess.run(command.split())
    except (FileNotFoundError, subprocess.SubprocessError) as exc:
        log.error(exc)
        sys.exit(1)


def reload_zone(zone):
    shell(f"rndc freeze {zone}")
    shell(f"rndc reload {zone}")
    shell(f"rndc thaw {zone}")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Add an IPv6 reverse PTR record for ZNC vhosts.", prog="zncreverse"
    )
    parser.add_argument("domain", help="Hostname to create a PTR record for")
    parser.add_argument(
        "-a", "--address", nargs="?", help="Address to use instead of querying DNS"
    )
    parser.add_argument(
        "-z",
        "--zone",
        nargs="?",
        default="3.0.0.6.0.0.0.0.3.5.7.0.6.2.ip6.arpa",
        help="Zone name",
    )
    parser.add_argument("-o", "--output", nargs="?", help="Output file for PTR record")
    return parser.parse_args()


def get_ip_address(domain: str):
    addrinfo = socket.getaddrinfo(domain, None, socket.AF_INET6)
    return addrinfo[0][4][0]


def get_reverse_ptr(address: str) -> str:
    return ip_address(address).reverse_pointer


def main():
    args = parse_args()
    domain = args.domain
    zone = args.zone
    zone_file = args.output or f"/var/lib/bind/{zone}.zone"

    try:
        address = args.address or get_ip_address(domain)
        reverse_ptr = get_reverse_ptr(address)
    except Exception as exc:
        log.error(exc)
        sys.exit(1)

    ptr_record = f"{reverse_ptr}.    IN    PTR    {domain}.\n"
    log.info(f"The following PTR record will be used for {domain} ({address})")
    log.info(ptr_record)

    try:
        input("Press Enter to proceed...")
    except KeyboardInterrupt:
        return

    try:
        with open(f"{zone_file}", "a") as fd:
            log.info(f"Writing to {zone_file}")
            fd.write(f"{ptr_record}")
            reload_zone(zone)
    except FileNotFoundError as exc:
        log.error(exc)
        sys.exit(errno.ENOENT)


if __name__ == "__main__":
    log.basicConfig(level=log.INFO, format="%(message)s")
    main()
