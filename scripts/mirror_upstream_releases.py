#!/usr/bin/env python3
"""Preserve upstream release assets without publishing them as DragonForge builds."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request

SOURCE = "opencode-ai/opencode"
DESTINATION = "HenricHuntsman/dragonforge-code"
API = "https://api.github.com"


def request_json(path, token, data=None, method=None):
    payload = None if data is None else json.dumps(data).encode()
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "DragonForge-upstream-archive"}
    if token:
        headers["Authorization"] = "Bearer " + token
    if payload is not None:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(API + path, data=payload, headers=headers, method=method)
    for attempt in range(6):
        try:
            with urllib.request.urlopen(req, timeout=120) as response:
                return json.load(response)
        except urllib.error.HTTPError as error:
            if error.code == 404:
                return None
            detail = error.read().decode("utf-8", errors="replace")
            limited = error.code in (403, 429) and (
                error.headers.get("Retry-After") is not None
                or error.headers.get("X-RateLimit-Remaining") == "0"
                or "rate limit" in detail.lower()
                or "abuse" in detail.lower())
            if attempt < 5 and (limited or error.code in (502, 503, 504)):
                delay = min(3600, max(60, int(error.headers.get("Retry-After", "60"))))
                if error.headers.get("X-RateLimit-Remaining") == "0":
                    delay = min(3600, max(delay, int(error.headers.get("X-RateLimit-Reset", "0")) - int(time.time()) + 5))
                print(f"GitHub temporarily unavailable ({error.code}); retrying in {delay}s", flush=True)
                time.sleep(delay)
                continue
            raise RuntimeError(f"GitHub API {error.code} for {path}: {detail}") from error


def archive_tag(tag):
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", tag):
        raise ValueError("Unsupported upstream tag: " + tag)
    return "upstream-" + tag


def safe_asset_name(name):
    if not name or name in (".", "..") or "/" in name or "\\" in name:
        raise ValueError("Unsafe asset filename")
    return name


def verify_digest(path, expected=None):
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if expected and digest.lower() != expected.removeprefix("sha256:").lower():
        raise ValueError("Checksum mismatch for " + path.name)
    return digest


def download_asset(asset, directory):
    name = safe_asset_name(asset["name"])
    url = asset["browser_download_url"]
    prefix = f"https://github.com/{SOURCE}/releases/download/"
    if not url.startswith(prefix):
        raise ValueError("Asset URL is not from the expected source repository")
    target = directory / name
    # Public asset downloads never carry the destination API token.
    req = urllib.request.Request(url, headers={"User-Agent": "DragonForge-upstream-archive"})
    with urllib.request.urlopen(req, timeout=180) as response, target.open("wb") as output:
        while chunk := response.read(1024 * 1024):
            output.write(chunk)
    if target.stat().st_size != asset["size"]:
        raise ValueError("Downloaded size differs for " + name)
    return target, verify_digest(target, asset.get("digest"))


def source_commit(tag, token):
    ref = request_json(f"/repos/{SOURCE}/git/ref/tags/{urllib.parse.quote(tag, safe='')}", token)
    if ref is None:
        raise RuntimeError("Upstream tag no longer available: " + tag)
    obj = ref["object"]
    for _ in range(10):
        if obj["type"] == "commit":
            return obj["sha"]
        if obj["type"] != "tag":
            break
        annotation = request_json(f"/repos/{SOURCE}/git/tags/{obj['sha']}", token)
        obj = annotation["object"]
    raise RuntimeError("Cannot resolve upstream tag to a commit")


def upload_asset(release, path, digest, token):
    assets = request_json(f"/repos/{DESTINATION}/releases/{release['id']}/assets?per_page=100", token)
    existing = next((a for a in assets if a["name"] == path.name), None)
    if existing:
        if existing.get("digest") == "sha256:" + digest and existing["size"] == path.stat().st_size:
            return
        raise RuntimeError("Existing asset differs; refusing overwrite: " + path.name)
    url = release["upload_url"].split("{", 1)[0] + "?" + urllib.parse.urlencode({"name": path.name})
    expected_prefix = f"https://uploads.github.com/repos/{DESTINATION}/releases/"
    if not url.startswith(expected_prefix):
        raise ValueError("Unexpected upload URL")
    req = urllib.request.Request(url, data=path.read_bytes(), method="POST", headers={
        "Authorization": "Bearer " + token, "Content-Type": "application/octet-stream",
        "User-Agent": "DragonForge-upstream-archive"})
    with urllib.request.urlopen(req, timeout=300) as response:
        result = json.load(response)
    if result.get("digest") != "sha256:" + digest:
        raise RuntimeError("Uploaded asset digest could not be verified: " + path.name)


def mirror_release(original, token, history_bundle=None):
    catalog_release = original
    live = request_json(f"/repos/{SOURCE}/releases/{original['id']}", token)
    inventory = lambda r: sorted((a['id'], a['name'], a['size']) for a in r['assets'])
    if live is None or live['tag_name'] != original['tag_name'] or inventory(live) != inventory(original):
        raise RuntimeError("Upstream release changed since the reviewed catalog")
    original = live
    source_tag = original["tag_name"]
    tag = archive_tag(source_tag)
    commit = source_commit(source_tag, token)
    ref_path = f"/repos/{DESTINATION}/git/ref/tags/{tag}"
    ref = request_json(ref_path, token)
    if ref is None:
        # Tags for preserved binaries use a known destination snapshot. Historical
        # commits can introduce workflow files that GITHUB_TOKEN cannot authorize.
        # Exact upstream source remains attached and recorded in the metadata.
        target = os.environ["ARCHIVE_BASE_SHA"]
        request_json(f"/repos/{DESTINATION}/git/refs", token, {"ref": "refs/tags/" + tag, "sha": target})
    elif ref["object"]["sha"] not in (commit, os.environ["ARCHIVE_BASE_SHA"]):
        raise RuntimeError("Archive tag points at an unexpected commit; refusing to move it")
    release = request_json(f"/repos/{DESTINATION}/releases/tags/{tag}", token)
    if release and not release["draft"]:
        print("Already published historical copy:", tag, flush=True)
        # Verify its complete asset inventory below; never silently skip missing files.
    if release is None:
        notes = (f"Historical upstream OpenCode release {source_tag}.\n\n"
                 f"Original: {original['html_url']}\n"
                 f"Originally published: {original['published_at']}\n"
                 f"Original release author: {original['author']['login']}\n"
                 f"Original source commit: {commit}\n\n"
                 "These are preserved upstream binaries, not new DragonForge builds. "
                 "Original authorship and licence notices remain applicable. "
                 "Use the attached upstream-source archives for the exact original source. "
                 "Archive tags may point at the preservation snapshot for workflow authorization or disconnected history; "
                 "GitHub's automatic Source code links may therefore differ. "
                 "See upstream-release-metadata.json for provenance.\n\n"
                 "---\n\n" + (original.get("body") or ""))
        release = request_json(f"/repos/{DESTINATION}/releases", token, {
            "tag_name": tag, "name": "Historical OpenCode " + source_tag,
            "body": notes, "draft": True, "prerelease": original["prerelease"], "make_latest": "false"})
    with tempfile.TemporaryDirectory(prefix="dragonforge-archive-") as temp:
        directory = Path(temp)
        downloads = [download_asset(a, directory) for a in original["assets"]]
        checksums = directory / "checksums.txt"
        if checksums.exists():
            expected = {}
            for line in checksums.read_text().splitlines():
                match = re.fullmatch(r"([a-fA-F0-9]{64})\s+\*?(.+)", line)
                if match:
                    expected[match[2]] = match[1]
            for path, _ in downloads:
                if path.name in expected:
                    verify_digest(path, expected[path.name])
        for suffix, kind in [("tar.gz", "tarball"), ("zip", "zipball")]:
            path = directory / ("upstream-source-" + source_tag + "." + suffix)
            url = f"https://github.com/{SOURCE}/archive/{commit}.{suffix}"
            with urllib.request.urlopen(url, timeout=180) as response, path.open("wb") as output:
                while chunk := response.read(1024 * 1024):
                    output.write(chunk)
            downloads.append((path, verify_digest(path)))
        if history_bundle is not None:
            downloads.append((history_bundle, verify_digest(history_bundle)))
        metadata = directory / "upstream-release-metadata.json"
        metadata.write_text(json.dumps({"source_repository": SOURCE, "source_commit": commit,
                                       "original_release": catalog_release,
                                       "upstream_api_url": f"{API}/repos/{SOURCE}/releases/{original['id']}",
                                       "verified_sha256": {p.name: d for p, d in downloads}}, indent=2) + "\n")
        for path, digest in downloads + [(metadata, verify_digest(metadata))]:
            upload_asset(release, path, digest, token)
    if release["draft"]:
        request_json(f"/repos/{DESTINATION}/releases/{release['id']}", token,
                     {"draft": False, "make_latest": "false"}, method="PATCH")
    print("Verified historical release:", tag, flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path, default=Path("docs/upstream/catalog.json"))
    parser.add_argument("--history-bundle", type=Path)
    parser.add_argument("--publish", action="store_true", help="Mirror verified assets into historical destination releases")
    args = parser.parse_args()
    catalog = json.loads(args.catalog.read_text())
    if catalog["source_repository"] != SOURCE:
        raise ValueError("Unexpected source repository")
    releases = catalog["releases"]
    print(json.dumps({"releases": len(releases), "assets": sum(len(r["assets"]) for r in releases),
                      "bytes": sum(a["size"] for r in releases for a in r["assets"])}, indent=2), flush=True)
    for release in releases:
        archive_tag(release["tag_name"])
        for asset in release["assets"]:
            safe_asset_name(asset["name"])
    if not args.publish:
        return
    if os.environ.get("GITHUB_REPOSITORY") != DESTINATION:
        raise RuntimeError("Publishing is restricted to the DragonForge repository workflow")
    token = os.environ["GH_TOKEN"]
    for release in sorted(releases, key=lambda r: r["published_at"] or ""):
        if not release["draft"]:
            bundle = args.history_bundle if release["tag_name"] == releases[0]["tag_name"] else None
            mirror_release(release, token, bundle)


if __name__ == "__main__":
    main()
