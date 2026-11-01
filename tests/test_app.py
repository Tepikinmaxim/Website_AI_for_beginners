from html import unescape
from pathlib import Path

import pytest

from app import app, cards

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def client():
    app.config.update(TESTING=True)
    with app.test_client() as test_client:
        yield test_client


def test_cards_count_and_fields():
    assert 8 <= len(cards) <= 10
    assert len({card["id"] for card in cards}) == len(cards)

    for card in cards:
        assert set(card) == {"id", "title", "subtitle", "image_url"}
        assert card["title"].strip()
        assert card["subtitle"].strip()
        assert card["image_url"].startswith("https://images.unsplash.com/photo-")
        assert "w=800" in card["image_url"]
        assert "q=80" in card["image_url"]


def test_index_renders_all_cards(client):
    response = client.get("/")
    assert response.status_code == 200

    html = response.get_data(as_text=True)
    decoded_html = unescape(html)
    assert html.count('class="card"') == len(cards)
    assert html.count('class="cta-button"') == len(cards)

    for card in cards:
        assert card["title"] in html
        assert card["subtitle"] in html
        assert card["image_url"] in decoded_html
        assert f'href="/material/{card["id"]}"' in html

    assert 'name="viewport"' in html
    assert "Смотреть дайджест" in html
    assert "bootstrap" not in html.lower()
    assert "tailwind" not in html.lower()


def test_material_pages(client):
    for card in cards:
        response = client.get(f"/material/{card['id']}")
        assert response.status_code == 200

        html = response.get_data(as_text=True)
        assert f"Материал №{card['id']}" in html
        assert "Здесь будет подробный разбор для новичков" in html
        assert card["title"] in html


def test_unknown_material_returns_404(client):
    response = client.get("/material/999")
    assert response.status_code == 404
    assert "Такого материала пока нет" in response.get_data(as_text=True)


def test_header_and_footer_have_logo(client):
    html = client.get("/").get_data(as_text=True)

    assert html.count('alt="AiMaximum"') >= 2
    assert "footer-logo" in html
    assert "Сделано компанией AiMaximum" in html

    logo = ROOT / "static" / "img" / "logo.png"
    assert logo.exists()
    assert logo.stat().st_size > 1000
    assert logo.read_bytes().startswith(b"\x89PNG")


def test_css_contract():
    css = (ROOT / "static" / "css" / "style.css").read_text(encoding="utf-8")

    assert "--bg: #f4f6fa" in css
    assert "--accent: #0e7490" in css
    assert "--text: #121722" in css
    assert "color-scheme: light" in css

    assert "grid-template-columns: repeat(2, minmax(0, 1fr))" in css
    assert "grid-template-columns: repeat(3, minmax(0, 1fr))" in css
    assert "grid-template-columns: repeat(4, minmax(0, 1fr))" in css
    assert "@media (min-width: 640px)" in css
    assert "@media (min-width: 1024px)" in css
    assert "@media (min-width: 1320px)" in css

    assert ".card:hover" in css
    assert "translateY(-8px)" in css
    assert ".card-image" in css
    assert "transition:" in css

    assert ".main-nav a.is-active" in css
    assert "text-decoration: none" in css
    assert "linear-gradient" in css
    assert "@media (prefers-reduced-motion: reduce)" in css


def test_javascript_contract():
    script = (ROOT / "static" / "js" / "main.js").read_text(encoding="utf-8")

    assert "IntersectionObserver" in script
    assert "prefers-reduced-motion" in script
    assert "is-visible" in script
    assert "aria-current" in script
