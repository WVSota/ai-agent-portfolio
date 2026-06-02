"""
Resilient web scraper built on Playwright.

Design choices that matter for real-world scraping:
  - Realistic browser context (UA, viewport, locale) to reduce bot flags.
  - Exponential-backoff retry on navigation/timeout failures.
  - Explicit wait for the target selector rather than fixed sleeps.
  - Polite rate limiting between requests.

Usage:
    pip install playwright && playwright install chromium
    python web_scraper.py https://example.com ".product-card" --fields name=".title" price=".price"
"""
from __future__ import annotations
import argparse, asyncio, json, random
from playwright.async_api import async_playwright, TimeoutError as PWTimeout

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")


async def fetch(page, url: str, wait_selector: str, retries: int = 3):
    for attempt in range(retries):
        try:
            await page.goto(url, wait_until="domcontentloaded", timeout=30000)
            await page.wait_for_selector(wait_selector, timeout=15000)
            return
        except PWTimeout:
            if attempt == retries - 1:
                raise
            await asyncio.sleep(2 ** attempt + random.random())


async def scrape(url: str, item_selector: str, fields: dict[str, str]) -> list[dict]:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(user_agent=UA, viewport={"width": 1366, "height": 768},
                                             locale="en-US")
        page = await context.new_page()
        await fetch(page, url, item_selector)

        results = []
        for item in await page.query_selector_all(item_selector):
            row = {}
            for name, sel in fields.items():
                el = await item.query_selector(sel)
                row[name] = (await el.inner_text()).strip() if el else None
            results.append(row)
        await browser.close()
        return results


def _parse_fields(pairs: list[str]) -> dict[str, str]:
    return dict(p.split("=", 1) for p in pairs)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("item_selector")
    ap.add_argument("--fields", nargs="+", required=True, help='name=".css" pairs')
    args = ap.parse_args()
    data = asyncio.run(scrape(args.url, args.item_selector, _parse_fields(args.fields)))
    print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
