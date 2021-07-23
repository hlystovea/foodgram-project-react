import io

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


pdfmetrics.registerFont(TTFont('Calibri-Light', '../fonts/Calibri-Light.ttf'))


def get_pdf(purchases):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)

    p.setFont('Calibri-Light', 18)
    p.drawString(50, 800, 'Foodgram. Список продуктов.')
    p.line(50, 790, 550, 790)

    p.setFont('Calibri-Light', 16)
    x = 50
    y = 750
    if purchases:
        for i in purchases:
            string = f'{i["name"].capitalize()} - {i["total"]} {i["unit"]}'
            p.drawString(x, y, string)
            y -= 20
    else:
        p.drawString(x, y, 'Список продуктов пуст.')

    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer


def get_limit(request):
    try:
        limit = int(request.query_params['recipes_limit'])
        if limit <= 0:
            raise ValueError()
        return limit
    except (KeyError, ValueError):
        pass
    return None
