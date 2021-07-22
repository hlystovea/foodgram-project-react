import io
from reportlab.pdfgen import canvas


def get_shopping_list(ingredients=None):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)

    p.setFont('Helvetica-Bold', 18)
    p.drawString(50, 800, 'Foodgram. Shopping list.')
    p.line(50, 790, 550, 790)

    p.setFont('Courier-Bold', 16)
    x = 50
    y = 750
    if ingredients:
        for ingredient in ingredients:
            p.drawString(x, y, str(ingredient))
            y -= 20
    else:
        p.drawString(x, y, 'Список покупок пуст.')

    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer
