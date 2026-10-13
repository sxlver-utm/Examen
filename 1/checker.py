import requests

SITES = [
    "https://example.com",
    "https://httpbin.org/html",
    "https://httpbin.org/json",
    "https://httpbin.org/status/200",
    "https://httpbin.org/redirect/1",
    "https://httpbin.org/delay/2",
    "https://httpbin.org/status/404",
    "https://httpbin.org/status/500",
    "https://httpbin.org/delay/10",
    "http://this-site-does-not-exist.invalid",
    "https://httpbin.org/response-headers?X-Frame-Options=DENY&X-Content-Type-Options=nosniff",
    "https://httpbin.org/response-headers?x-frame-options=DENY",
    "https://httpbin.org/status/200,500",
]

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
]


def build_url(host, path):
    """Construiește URL-ul, indiferent dacă path începe cu /."""
    if not host.startswith(("http://", "https://")):
        host = "https://" + host

    return host.rstrip("/") + "/" + path.lstrip("/")


def is_https(url):
    """Verifică dacă adresa folosește HTTPS."""
    return url.startswith("https://")


def show_response(url):
    """Afișează statusul și Content-Type."""
    try:
        response = requests.get(url, timeout=5)
        print(f"Status: {response.status_code}")
        print(f"Content-Type: {response.headers.get('Content-Type', 'unknown')}")
    except requests.Timeout:
        print("Eroare: Timeout")
    except requests.RequestException:
        print("Eroare: Eroare de conexiune")


def check_site(url):
    """Returnează informațiile site-ului sau un mesaj de eroare."""
    try:
        response = requests.get(url, timeout=5)

        return {
            "status": response.status_code,
            "content_type": response.headers.get("Content-Type", "unknown"),
            "length": len(response.content),
            "server": response.headers.get("Server", "unknown"),
        }
    except requests.Timeout:
        return {"status": None, "error": "Timeout"}
    except requests.RequestException:
        return {"status": None, "error": "Eroare de conexiune"}


def scan_sites():
    """Afișează site-urile cu status 200, sortate după dimensiune."""
    rezultate = []

    for url in SITES:
        rezultat = check_site(url)
        rezultate.append((url, rezultat))

    reusite = [
        (url, rezultat)
        for url, rezultat in rezultate
        if rezultat["status"] == 200
    ]

    reusite.sort(key=lambda item: item[1]["length"], reverse=True)

    for url, rezultat in reusite:
        print(f"{url:<85} -> 200, {rezultat['length']} octeți")

    esuate = len(rezultate) - len(reusite)
    print(f"Reușite: {len(reusite)} | Eșuate: {esuate}")


def check_headers(url):
    """Verifică antetele de securitate și calculează scorul."""
    try:
        response = requests.get(url, timeout=5)

        present = []
        missing = []

        for header in SECURITY_HEADERS:
            if header in response.headers:
                present.append(header)
            else:
                missing.append(header)

        score = int(len(present) / len(SECURITY_HEADERS) * 100)

        return {
            "present": present,
            "missing": missing,
            "score": score,
        }
    except requests.Timeout:
        return {"status": None, "error": "Timeout"}
    except requests.RequestException:
        return {"status": None, "error": "Eroare de conexiune"}


def retry_check(url, attempts=3):
    """Repetă cererea la erori de conexiune sau statusuri >= 500."""
    status = None
    error = None
    count = 0

    for _ in range(attempts):
        count += 1

        try:
            response = requests.get(url, timeout=5)
            status = response.status_code

            # Ne oprim inclusiv pentru statusuri precum 404.
            if status < 500:
                return {"status": status, "attempts": count}

        except requests.Timeout:
            error = "Timeout"
        except requests.RequestException:
            error = "Eroare de conexiune"

    if status is None and error is not None:
        return {"status": None, "error": error, "attempts": count}

    return {"status": status, "attempts": count}