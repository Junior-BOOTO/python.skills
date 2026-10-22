"""Optional browser smoke check for the HTML demo (requires Playwright + Chromium)."""
from pathlib import Path
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from functools import partial
from threading import Thread
from playwright.sync_api import sync_playwright

root = Path(__file__).parents[1].joinpath('demo').resolve()
server = ThreadingHTTPServer(('127.0.0.1', 0), partial(SimpleHTTPRequestHandler, directory=str(root)))
Thread(target=server.serve_forever, daemon=True).start()
page_url = f'http://127.0.0.1:{server.server_port}/phonofle_ai_demo.html'
with sync_playwright() as pw:
    browser = pw.chromium.launch(executable_path='/usr/bin/chromium', headless=True, args=['--no-sandbox'])
    page = browser.new_page(viewport={'width': 1280, 'height': 950}, accept_downloads=True)
    errors=[]
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.goto(page_url)
    page.screenshot(path='/mnt/data/PhonoFLE_AI_V1/demo/aperçu_desktop.png', full_page=True)
    assert page.title().startswith('PhonoFLE AI')
    page.get_by_role('button', name='ES').click()
    assert 'Mi recorrido auditivo' in page.locator('#testTitle').inner_text()
    page.get_by_role('button', name='FR').click()
    page.locator('#startBtn').click()
    for number in range(10):
        assert f'{number+1} / 10' in page.locator('#stepCount').inner_text()
        page.locator('#choices button').first.click()
        assert page.locator('#feedback').is_visible()
        page.locator('#nextBtn').click()
    assert page.locator('#final').is_visible()
    assert '%' in page.locator('#score').inner_text()
    with page.expect_download() as download_info:
        page.locator('#exportBtn').click()
    download=download_info.value
    assert download.suggested_filename == 'phonofle_resultat_anonyme.json'
    page.screenshot(path='/mnt/data/PhonoFLE_AI_V1/demo/aperçu_bilan.png', full_page=True)
    assert not errors, errors
    print('HTML Playwright smoke check OK: FR/ES, 10 questions, feedback, results and export')
    browser.close()
    server.shutdown()
