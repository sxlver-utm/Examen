import requests
BASE = "https://httpbin.org"
PATHS = ["/get", "/redirect/2", "/delay/1", "/status/404", "/delay/5"]
# Partea 1: parametri în URL
def search(params):
    """GET pe /get cu parametri în URL; returnează parametrii primiți de
    server."""
    response = requests.get(BASE + "/get", params=params)
    return response.json()["args"]
def search_url(params):
    """Returnează adresa completă construită de requests, cu tot cu
parametri."""
    response = requests.get(BASE + "/get", params=params)
    return response.url
# Partea 2: anteturi
def fetch_with_agent(agent):
    """GET pe /headers cu User-Agent=agent; returnează User-Agent-ul văzut de
    server."""
    response = requests.get(BASE + "/headers", headers={"User-Agent": agent})
    return response.json()["headers"]["User-Agent"]
def default_agent():
    """Returnează User-Agent-ul trimis de requests când nu setezi nimic."""
    response = requests.get(BASE + "/headers")
    return response.json()["headers"]["User-Agent"]
# Partea 3: trimiterea datelor
def post_json(data):
    """POST cu datele ca JSON pe /post; returnează JSON-ul primit de
    server."""
    response = requests.post(BASE + "/post", json=data)
    return response.json()["json"]
def post_form(data):
    """POST cu datele ca formular pe /post; returnează formularul primit de
    server."""
    return requests.post(BASE + "/post", data=data).json()["form"]
# Partea 4: coduri de stare
def describe_status(code):
    """GET pe /status/<code>; returnează 'succes', 'eroare client' sau
    'eroare server'."""
    status = requests.get(f"{BASE}/status/{code}").status_code
    if 200 <= status < 300:
        return "succes"
    if 400 <= status < 500:
        return "eroare client"
    if 500 <= status < 600:
        return "eroare server"
    return "eroare client"
def is_ok(code):
    """GET pe /status/<code>; returnează True dacă cererea a reușit, altfel
    False."""
    try:
        response = requests.get(f"{BASE}/status/{code}")
        response.raise_for_status()
        return True
    except requests.RequestException:
        return False
# Partea 5: redirecționări
def count_redirects(n):
    """GET pe /redirect/<n>; returnează câte redirecționări au fost urmate."""
    return len(requests.get(f"{BASE}/redirect/{n}").history)
def final_url(n):
    """GET pe /redirect/<n>; returnează adresa la care ai ajuns."""
    return requests.get(f"{BASE}/redirect/{n}").url
def first_hop(n):
    """GET pe /redirect/<n> FĂRĂ a urma redirecționarea; returnează antetul
    Location."""
    return requests.get(f"{BASE}/redirect/{n}", allow_redirects=False).headers.get("Location")
# Partea 6: sesiuni și cookie-uri
def cookie_demo(name, value):
    """Setează un cookie, apoi citește cookie-urile înapoi folosind O SINGURĂ
    sesiune."""
    with requests.Session() as session:
        session.get(f"{BASE}/cookies/set", params={name: value})
        return session.get(BASE + "/cookies").json()["cookies"]
def no_session_demo(name, value):
    """Fă același lucru cu apeluri simple requests.get; returnează cookieurile văzute de server."""
    requests.get(f"{BASE}/cookies/set", params={name: value})
    return requests.get(BASE + "/cookies").json()["cookies"]
# Partea 7: raportul de timp
def report(path):
    """Returnează un dicționar care descrie pagina de la BASE + path."""
    try:
        response = requests.get(BASE + path, timeout=3)
        return {
            "status": response.status_code,
            "url": response.url,
            "redirects": len(response.history),
            "seconds": response.elapsed.total_seconds(),
            "content_type": response.headers.get("Content-Type", "")  
        }
    except requests.Timeout:
        return{"status": None, "error": "timeout"}
    except requests.RequestException:
        return{"status": None, "error": "request error"}
def main():
    rezultate = []
    for path in PATHS:
        rezultat = report(path)
        rezultat["path"] = path
        rezultate.append(rezultat)  

    reusite = []
    for rezultat in rezultate:
        if rezultat["status"] == 200:
            reusite.append(rezultat)

    reusite.sort(key=lambda rezultat: rezultat["seconds"], reverse=True)
    for rezultat in reusite:
        print(f"{rezultat['path']}: {rezultat['seconds']:.2f} secunde")
    esuate = len(rezultate) - len(reusite)
    print(f"{len(reusite)} reușite, {esuate} eșuate")

# Bonus: autentificare

def check_login(user, password):
    """Returnează True dacă serverul acceptă datele de autentificare, altfel
    False."""
    try:
        response = requests.get(
        BASE + "/basic-auth/admin/secret",
        auth=(user, password),
        timeout=3
)
        return response.status_code == 200
    except requests.RequestException:
        return False


if __name__ == "__main__":
    main()
