"""Flask-приложение «AI-дайджест для новичков».

Здесь нет базы данных: все материалы хранятся в обычном списке словарей.
Так проще читать код и менять контент.
"""

from flask import Flask, abort, render_template

app = Flask(__name__)

# 9 карточек дайджеста. У каждой карточки ровно четыре поля:
# id, заголовок, подзаголовок и ссылка на обложку.
# Ссылки ведут на Unsplash с фиксированной шириной 800 px.
cards = [
    {
        "id": 1,
        "title": "Что такое нейросеть",
        "subtitle": "Объясняем на пальцах, без формул и сложных терминов.",
        "image_url": "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=800&q=80",
    },
    {
        "id": 2,
        "title": "Первый промпт",
        "subtitle": "Как разговаривать с ИИ, чтобы получать точные ответы.",
        "image_url": "https://images.unsplash.com/photo-1620712943543-bcc4688e7485?w=800&q=80",
    },
    {
        "id": 3,
        "title": "ChatGPT за 15 минут",
        "subtitle": "Практический старт: регистрация, диалог и первые задачи.",
        "image_url": "https://images.unsplash.com/photo-1531746790731-6c087fecd65a?w=800&q=80",
    },
    {
        "id": 4,
        "title": "ИИ в учёбе",
        "subtitle": "Конспекты, перевод и проверка текста без зубрёжки.",
        "image_url": "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=800&q=80",
    },
    {
        "id": 5,
        "title": "ИИ в работе",
        "subtitle": "Какие рутинные задачи можно отдать ассистенту уже сегодня.",
        "image_url": "https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=800&q=80",
    },
    {
        "id": 6,
        "title": "Безопасность и данные",
        "subtitle": "Что не стоит отправлять в чат и как защитить себя.",
        "image_url": "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=800&q=80",
    },
    {
        "id": 7,
        "title": "Картинки из текста",
        "subtitle": "Генерация изображений: первый результат за пару минут.",
        "image_url": "https://images.unsplash.com/photo-1541701494587-cb58502866ab?w=800&q=80",
    },
    {
        "id": 8,
        "title": "Свои GPT-ассистенты",
        "subtitle": "Собираем помощника под свою задачу без единой строки кода.",
        "image_url": "https://images.unsplash.com/photo-1518770660439-4636190af475?w=800&q=80",
    },
    {
        "id": 9,
        "title": "Куда двигаться дальше",
        "subtitle": "Карта обучения новичка: от любопытства до первого проекта.",
        "image_url": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=800&q=80",
    },
]


@app.route("/")
def index():
    """Главная страница: передаём в шаблон список карточек."""
    return render_template("index.html", cards=cards)


@app.route("/material/<int:material_id>")
def material(material_id):
    """Страница-заглушка конкретного материала.

    Если такого id нет, возвращаем честную ошибку 404,
    а не пустую карточку.
    """
    card = next((item for item in cards if item["id"] == material_id), None)
    if card is None:
        abort(404)
    return render_template("material.html", card=card)


@app.errorhandler(404)
def page_not_found(_error):
    """Единая страница 404 в стиле сайта."""
    return render_template("404.html"), 404


if __name__ == "__main__":
    # debug=True удобен при обучении: код перезапускается сам.
    # Для публичного запуска отключите debug.
    app.run(debug=True, port=5000)
