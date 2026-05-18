#!/usr/bin/env python3

import requests
import ipaddress
import argparse

# -------------------------
# RIPE API
# -------------------------
def get_prefixes(asn):
    try:
        url = f"https://stat.ripe.net/data/announced-prefixes/data.json?resource={asn}"
        r = requests.get(url, timeout=15)
        data = r.json()
        return [p["prefix"] for p in data["data"]["prefixes"]]
    except Exception as e:
        print(f"[!] API error: {e}")
        return []


# -------------------------
# FAST CIDR → IP WRITER
# -------------------------
def write_ips_fast(prefixes, outfile):
    with open(outfile, "w") as f:
        for cidr in prefixes:
            try:
                net = ipaddress.ip_network(cidr, strict=False)

                # iterate ALL IPs (faster than .hosts())
                for ip in net:
                    f.write(str(ip) + "\n")

            except Exception as e:
                print(f"[!] Skip {cidr}: {e}")


# -------------------------
# MAIN
# -------------------------
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--asn", required=True)
    parser.add_argument("-o", "--output", required=True)
    parser.add_argument("--no-expand", action="store_true")

    args = parser.parse_args()

    asn = args.asn.upper()

    print(f"[+] Fetching {asn} prefixes...")
    prefixes = get_prefixes(asn)

    if not prefixes:
        print("[!] No prefixes found")
        return

    print(f"[+] {len(prefixes)} CIDRs found")

    if args.no_expand:
        with open(args.output, "w") as f:
            for p in prefixes:
                f.write(p + "\n")
        print("[+] Saved CIDRs only")
        return

    print("[+] Expanding & writing IPs (FAST MODE)...")
    write_ips_fast(prefixes, args.output)

    print("[+] Done")


if __name__ == "__main__":
    main()
