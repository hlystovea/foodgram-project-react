import io
from http import HTTPStatus

from django.utils.translation import gettext_lazy as _
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from rest_framework.response import Response

from . import serializers


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


def binder(request, recipe, m2m_model):
    user = request.user
    if request.method == 'GET':
        obj, created = m2m_model.objects.get_or_create(
            user=user,
            recipe=recipe,
        )
        if created:
            serializer = serializers.RecipeLiteSerializer(recipe)
            return Response(serializer.data, status=HTTPStatus.CREATED)
    message = {'errors': _(f'Рецепт {recipe} уже добавлен.')}
    if request.method == 'DELETE':
        obj = m2m_model.objects.filter(user=user, recipe=recipe)
        if obj.exists():
            obj.delete()
            return Response(status=HTTPStatus.NO_CONTENT)
        message = {'errors': _('Рецепта {recipe} нет в списке.')}
    return Response(message, status=HTTPStatus.BAD_REQUEST)
