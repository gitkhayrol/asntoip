# asn-expand

Fetch all announced IP prefixes for a given ASN via the RIPE API and expand them to individual IPs — fast.

Built for bug bounty recon to quickly map out a target's full IP space.

---

## Usage

```bash
python3 asn-expand.py -a AS12345 -o ips.txt
```

### Options

| Flag | Description |
|------|-------------|
| `-a`, `--asn` | Target ASN (e.g. `AS12345`) |
| `-o`, `--output` | Output file path |
| `--no-expand` | Save CIDRs only, skip IP expansion |

---

## Examples

**Expand all IPs from an ASN:**
```bash
python3 asn-expand.py -a AS15169 -o google-ips.txt
```

**Save CIDRs only (no expansion):**
```bash
python3 asn-expand.py -a AS15169 -o google-cidrs.txt --no-expand
```

---

## Requirements

```bash
pip install requests
```

---

## How it works

1. Queries the [RIPE Stat API](https://stat.ripe.net) for all announced prefixes of the given ASN
2. Iterates every IP in each CIDR block
3. Writes all IPs line by line to the output file

> Large ASNs (e.g. cloud providers) can have millions of IPs — use `--no-expand` if you only need the CIDR ranges.

---

## License

MIT
