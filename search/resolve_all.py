#!/usr/bin/env python3
"""Resolve every DOI and arXiv id in the bibliography; report dead links.

Sends a lightweight request per identifier (HEAD to doi.org, GET to the arXiv
abstract page) and records the HTTP status. Prints a table of anything that
does not resolve to 2xx/3xx so it can be fixed or annotated.
"""

import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

BIB = Path(__file__).resolve().parent.parent / "cloud-db-metasurvey.bib"
UA = "cloud-db-metasurvey-resolve (mailto:hello@swiftride.net)"


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None  # don't follow into the publisher (which bot-blocks)


_opener = urllib.request.build_opener(NoRedirect)


def status(url):
    """For DOIs, resolve only the doi.org layer: a valid DOI returns a 3xx
    redirect to the publisher; an unregistered DOI returns 404 from doi.org.
    We deliberately do NOT follow the redirect, since publishers reject
    automated HEAD/GET with 403/420 even for valid content."""
    try:
        req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": UA})
        with _opener.open(req, timeout=30) as r:
            return r.status
    except urllib.error.HTTPError as e:
        if 300 <= e.code < 400:
            return e.code  # redirect surfaced as error by the no-redirect handler
        return e.code
    except Exception as e:
        return repr(e)


def main():
    text = BIB.read_text()
    dead = []
    n = 0
    for m in re.finditer(r"@\w+\{([^,]+),(.*?)\n\}", text, re.S):
        key, body = m.group(1).strip(), m.group(2)
        dm = re.search(r"doi\s*=\s*\{([^}]+)\}", body)
        am = re.search(r"(?:howpublished\s*=\s*\{arXiv:|note\s*=\s*\{arXiv:|eprint\s*=\s*\{)([\d.]+)", body)
        if dm:
            n += 1
            s = status("https://doi.org/" + dm.group(1))
            if not (isinstance(s, int) and 200 <= s < 400):
                dead.append((key, "DOI", dm.group(1), s))
            time.sleep(0.2)
        elif am:
            n += 1
            s = status("https://arxiv.org/abs/" + am.group(1))
            if not (isinstance(s, int) and 200 <= s < 400):
                dead.append((key, "arXiv", am.group(1), s))
            time.sleep(0.2)
    print(f"checked {n} identifiers")
    if dead:
        print(f"{len(dead)} unresolved:")
        for key, kind, ident, s in dead:
            print(f"  {key}: {kind} {ident} -> {s}")
        sys.exit(1)
    print("all identifiers resolve")


if __name__ == "__main__":
    main()
