from checker import (
    SITES,
    build_url,
    is_https,
    show_response,
    check_site,
    scan_sites,
    check_headers,
    retry_check,
)


def main():
    # Partea 1: două exemple pentru fiecare funcție.
    print("\n--- Partea 1: Funcții ---")

    host = SITES[0].split("://", 1)[1]

    print(build_url(host, "login"))
    print(build_url(host, "/login"))

    print(is_https(SITES[0]))
    print(is_https(SITES[9]))

    # Partea 2: un site accesibil și unul inexistent.
    print("\n--- Partea 2: Trimiterea unei cereri ---")

    print(SITES[0])
    show_response(SITES[0])

    print(SITES[9])
    show_response(SITES[9])

    # Partea 3: testăm fiecare adresă din SITES.
    print("\n--- Partea 3: Verificator reutilizabil ---")

    for url in SITES:
        print(f"{url}:")
        print(check_site(url))

    # Partea 4: o singură apelare.
    print("\n--- Partea 4: Verificarea mai multor site-uri ---")

    scan_sites()

    # Partea 5: fără antete, cu antete, litere mici și eroare.
    print("\n--- Partea 5: Audit de securitate ---")

    for url in (SITES[0], SITES[10], SITES[11], SITES[9]):
        print(f"{url}:")
        print(check_headers(url))

    # Partea 6: cazurile din exemplele PDF-ului.
    print("\n--- Partea 6: Încercări repetate ---")

    print("Partea 6, retry_check status 200:")
    print(retry_check(SITES[3]))

    print("Partea 6, retry_check status 404:")
    print(retry_check(SITES[6]))

    print("Partea 6, retry_check status 500:")
    print(retry_check(SITES[7]))

    print("Partea 6, retry_check status 500, attempts=2:")
    print(retry_check(SITES[7], attempts=2))

    print("Partea 6, retry_check site inexistent:")
    print(retry_check(SITES[9]))

    print("Partea 6, retry_check status aleatoriu:")
    print(retry_check(SITES[12]))


if __name__ == "__main__":
    main()