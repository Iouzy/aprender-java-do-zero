#!/usr/bin/env python3
"""Abre o site no computador e no telemóvel, tira capturas e procura estragos.

Corre antes de cada commit que mexa no aspeto do site:

    python3 bibi-capturas.py              # todos os ecrãs
    python3 bibi-capturas.py telemovel    # só alguns (nomes em ECRAS)

As capturas ficam em capturas/<ecrã>/ (fora do git). No fim aparece a lista
das verificações; se alguma falhar, o script sai com erro.

Não usa as contas verdadeiras: entra com uma sessão a fingir e responde às
chamadas do Supabase e do LRCLIB com dados de teste. Nada sai deste
computador a não ser os tipos de letra e o GSAP.
Precisa do Playwright:  pip install playwright && playwright install chromium
"""
import datetime
import functools
import http.server
import json
import pathlib
import sys
import threading
import time

from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT / "capturas"
PAGINA = "java-bancada.html"   # --pagina=outra.html para testar uma cópia
CATEGORIAS = 4                 # linhas do placar

ECRAS = {
    "computador": {"viewport": {"width": 1440, "height": 900}},
    "portatil": {"viewport": {"width": 1280, "height": 720}},
    # a janela do browser a meio do monitor
    "meio-monitor": {"viewport": {"width": 960, "height": 1000}},
    "telemovel": {"viewport": {"width": 390, "height": 844}, "device_scale_factor": 3, "is_mobile": True, "has_touch": True},
}

SECCOES = [
    ("02-veredicto", 'section[aria-labelledby="nowTitle"]'),
    ("03-almanaque", 'section[aria-label="Almanaque"]'),
    ("04-estante", 'section[aria-labelledby="pathTitle"]'),
    ("05-fichas", 'section[aria-labelledby="dictTitle"]'),
    ("06-jogo", 'section[aria-labelledby="gameTitle"]'),
    ("07-swandoku", 'section[aria-labelledby="sdTitle"]'),
    ("09-placar", "#placar"),
    ("10-cartas", 'section[aria-label="Cartas"]'),
]


# ---------- dados de teste ----------
def partidas():
    hoje = datetime.date.today()
    dia = lambda n: (hoje - datetime.timedelta(days=n)).isoformat()
    rows, i = [], 0
    def add(nome, jogo, nivel, valor, d):
        nonlocal i
        i += 1
        rows.append({"id": i, "criado": d + "T20:00:00Z", "nome": nome, "jogo": jogo, "nivel": nivel, "dia": d, "valor": valor})
    for n in range(6):
        add("bibi", "swandoku", 6, 190 + n * 7, dia(n))
    for n in (0, 1, 3):
        add("louzy", "swandoku", 6, 205 - n * 4, dia(n))
    add("bibi", "cerejas", 0, 42, dia(0))
    add("louzy", "cerejas", 0, 38, dia(1))
    add("bibi", "swandoku", 9, 811, dia(2))
    return rows


def cartas():
    return [{"id": 1, "criado": datetime.datetime.now().isoformat(), "autor": "teste-louzy", "nome": "louzy", "tipo": "carta", "texto": "Carta de teste.", "selo": "swan"}]


def letra_falsa(titulo):
    linhas = [f"[00:{10 + k:02d}.00] linha de teste {k + 1} de uma música qualquer" for k in range(12)]
    return [{"trackName": titulo, "artistName": "Lana Del Rey", "duration": 200, "plainLyrics": "", "syncedLyrics": "\n".join(linhas)}]


def responder(route):
    req, url = route.request, route.request.url
    if "/rest/v1/" in url:
        if req.method != "GET":
            return route.fulfill(status=201, body="")
        tabela = url.split("/rest/v1/")[1].split("?")[0]
        body = {"partidas": partidas(), "cartas": cartas()}.get(tabela, [])
        return route.fulfill(status=200, content_type="application/json", body=json.dumps(body))
    if "/auth/v1/" in url:
        return route.fulfill(status=200, content_type="application/json", body="{}")
    if "lrclib.net" in url:
        from urllib.parse import parse_qs, urlparse
        q = parse_qs(urlparse(url).query)
        titulo = (q.get("track_name") or q.get("q") or ["?"])[0]
        return route.fulfill(status=200, content_type="application/json", body=json.dumps(letra_falsa(titulo)))
    if "supabase-js" in url:
        return route.fulfill(status=200, content_type="application/javascript", body="")   # sem tempo real nos testes
    if "youtube.com" in url:
        return route.abort()
    return route.continue_()


SESSAO = """
try{ localStorage.setItem("java-sessao", JSON.stringify({access:"teste", refresh:"teste", exp:Date.now() + 864e5, id:"teste-bibi", nome:"bibi"})); }catch(e){}
"""


# ---------- verificações ----------
class Resultado:
    def __init__(self):
        self.linhas, self.falhas = [], 0

    def check(self, ecra, nome, ok, detalhe=""):
        self.linhas.append(f"  {'✔' if ok else '✘'} {ecra:13} {nome}{'' if ok else ' — ' + detalhe}")
        if not ok:
            self.falhas += 1


SEM_SCROLL_LATERAL = "() => document.documentElement.scrollWidth - innerWidth"

ESTANTE = """() => {
  const shelf = document.querySelector("#books");
  if(!shelf) return {erro:"sem #books"};
  const s = shelf.getBoundingClientRect(), w = shelf.parentElement.getBoundingClientRect();
  const books = [...shelf.querySelectorAll(".book")].map(b => b.getBoundingClientRect());
  return {livros:books.length, fora:books.filter(r => r.left < s.left - 1 || r.right > s.right + 1).length,
          finos:books.filter(r => r.width < 10).length, largura:Math.round(s.width), wrap:Math.round(w.width)};
}"""

# o título da cena do lago e o botão «só o lago» não podem ficar por baixo da janela do vídeo
JANELA = """() => {
  const win = document.querySelector("#discoWin");
  const parts = [win.querySelector(".vwin-card"), win.querySelector(".vwin-bar")].map(e => e.getBoundingClientRect());
  const alvo = [...document.querySelectorAll('#chLago [data-beat="1"] > *, #lakeOnly')];
  const bate = (a, b) => a.left < b.right && a.right > b.left && a.top < b.bottom && a.bottom > b.top;
  return alvo.filter(el => { const r = el.getBoundingClientRect(); return r.width && parts.some(p => bate(p, r)); })
             .map(el => el.id || el.tagName.toLowerCase());
}"""


def ir_para(page, seletor):
    y = page.evaluate("s => { const el = document.querySelector(s); return el ? el.getBoundingClientRect().top + scrollY : null; }", seletor)
    if y is None:
        return False
    page.evaluate("y => window.scrollTo(0, y)", y)
    page.mouse.move(5, 5)
    page.wait_for_timeout(1500)
    return True


def correr(p, base, nome, opts, res):
    pasta = OUT / nome
    pasta.mkdir(parents=True, exist_ok=True)
    browser = p.chromium.launch()
    erros = []

    # bancada e cadeado, sem sessão
    ctx = browser.new_context(**opts, locale="pt-PT")
    ctx.route("**/*", responder)
    page = ctx.new_page()
    page.on("pageerror", lambda e: erros.append(str(e)))
    page.goto(base + "/" + PAGINA, wait_until="networkidle")
    page.wait_for_timeout(600)
    page.screenshot(path=pasta / "00-bancada.png")
    res.check(nome, "bancada sem scroll para o lado", page.evaluate(SEM_SCROLL_LATERAL) <= 1, f"{page.evaluate(SEM_SCROLL_LATERAL)} px a mais")
    page.goto(base + "/" + PAGINA + "#bibi", wait_until="networkidle")
    page.wait_for_timeout(600)
    page.screenshot(path=pasta / "00-cadeado.png")
    ctx.close()

    # Modo Bibi com a sessão a fingir
    ctx = browser.new_context(**opts, locale="pt-PT")
    ctx.add_init_script(SESSAO)
    ctx.route("**/*", responder)
    page = ctx.new_page()
    page.on("pageerror", lambda e: erros.append(str(e)))
    page.goto(base + "/" + PAGINA + "#bibi", wait_until="networkidle")
    page.wait_for_timeout(2600)   # o título aparece como tinta
    page.mouse.move(5, 5)
    page.screenshot(path=pasta / "01-lago.png")

    # a janela do vídeo à vista, no sítio de sempre
    page.evaluate("document.querySelector('#discoWin').classList.remove('off')")
    page.wait_for_timeout(1400)   # os textos desviam-se devagar
    page.mouse.move(5, 5)
    page.screenshot(path=pasta / "01-lago-com-video.png")
    tapados = page.evaluate(JANELA)
    res.check(nome, "janela do vídeo não tapa o «Olá, Bibi»", not tapados, "tapa " + ", ".join(tapados))
    page.evaluate("document.querySelector('#discoWin').classList.add('off')")

    for ficheiro, seletor in SECCOES:
        if not ir_para(page, seletor):
            res.check(nome, f"secção {ficheiro}", False, "não existe")
            continue
        page.screenshot(path=pasta / f"{ficheiro}.png")

    e = page.evaluate(ESTANTE)
    res.check(nome, "estante: livros dentro das prateleiras", "erro" not in e and not e["fora"] and not e["finos"], json.dumps(e))
    res.check(nome, "estante: ocupa a largura da página", "erro" not in e and abs(e["largura"] - e["wrap"]) <= 2, json.dumps(e))
    res.check(nome, "Modo Bibi sem scroll para o lado", page.evaluate(SEM_SCROLL_LATERAL) <= 1, f"{page.evaluate(SEM_SCROLL_LATERAL)} px a mais")
    linhas = page.evaluate("document.querySelectorAll('#plRows li').length")
    res.check(nome, f"placar com as {CATEGORIAS} categorias", linhas == CATEGORIAS, f"{linhas} linhas")

    res.check(nome, "sem erros de JavaScript", not erros, " | ".join(erros[:3]))
    ctx.close()
    browser.close()


def main():
    escolhidos = [a for a in sys.argv[1:] if a in ECRAS] or list(ECRAS)
    global PAGINA
    PAGINA = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--pagina=")), PAGINA)
    class Calado(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a):
            pass
    handler = functools.partial(Calado, directory=str(ROOT))
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{srv.server_address[1]}"
    res, t0 = Resultado(), time.time()
    with sync_playwright() as p:
        for nome in escolhidos:
            print(f"· {nome}…", flush=True)
            correr(p, base, nome, ECRAS[nome], res)
    srv.shutdown()
    print("\n".join(res.linhas))
    print(f"\nCapturas em {OUT.relative_to(ROOT)}/ · {round(time.time() - t0)} s · "
          + ("tudo certo" if not res.falhas else f"{res.falhas} {'falha' if res.falhas == 1 else 'falhas'}"))
    sys.exit(1 if res.falhas else 0)


if __name__ == "__main__":
    main()
