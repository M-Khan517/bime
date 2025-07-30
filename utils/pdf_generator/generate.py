# import arabic_reshaper
# from bidi.algorithm import get_display
# from django.http import FileResponse
# from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# from reportlab.lib.pagesizes import A4
# from reportlab.lib import colors
# from io import BytesIO
# from apps.account_module.models import SubUser
from django.conf import settings

# from apps.home_module.models import SettingSite


# def reshape_text(text):
#     return get_display(arabic_reshaper.reshape(text))


# def generate_pdf_file(insurance_code, items, insurance_name=None, manager=None):
#     buffer = BytesIO()
#     pdfmetrics.registerFont(TTFont("Vazir", settings.FONT_PATH))
#     p = canvas.Canvas(buffer, pagesize=A4)
#     width, height = A4
#     p.setFont("Vazir", 18)

#     # عنوان
#     if SettingSite.objects.exists():
#         setting = SettingSite.objects.first()
#         p.drawCentredString(
#             width / 2, height - 30, reshape_text(f"سامانه {setting.name}")
#         )
#     else:
#         p.drawCentredString(width / 2, height - 30, reshape_text("سامانه بیمه زائر"))

#     if manager:
#         p.drawCentredString(
#             width / 2,
#             height - 45,
#             reshape_text(
#                 f"مدیر کاروان : {manager.full_name} - {manager.national_code}"
#             ),
#         )
#     if insurance_name:
#         p.drawCentredString(width / 2, height - 65, reshape_text(f"{insurance_name}"))

#     p.setFont("Vazir", 14)
#     p.drawCentredString(
#         width / 2,
#         height - 80,
#         reshape_text(
#             f"کدرهگیری بیمه نامه : {insurance_code}"
#             if insurance_code != None
#             else "لیست زیر مجموعه ها"
#         ),
#     )

#     y = height - 130
#     counter = 1
#     subs = items

#     for sub in subs:

#         if y < 100:
#             p.showPage()
#             p.setFont("Vazir", 14)
#             y = height - 100

#         p.drawRightString(
#             width - 50,
#             y,
#             reshape_text(f"{counter} - نام و نام خانوادگی: {sub.full_name}"),
#         )
#         p.drawRightString(
#             width - 50, y - 40, reshape_text(f"کد ملی: {sub.national_code}")
#         )

#         p.setStrokeColor(colors.grey)
#         p.setLineWidth(0.5)
#         p.line(50, y - 50, width - 50, y - 50)
#         y -= 80
#         counter += 1

#     p.showPage()
#     p.save()
#     buffer.seek(0)
#     return buffer


from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from io import BytesIO
from bidi.algorithm import get_display
import arabic_reshaper


def reshape_text(text):
    reshaped = arabic_reshaper.reshape(text)
    return get_display(reshaped)


def generate_pdf_file(insurance_code, items, caravan_name=None, manager=None):
    buffer = BytesIO()
    pdfmetrics.registerFont(TTFont("Vazir", settings.FONT_PATH))
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    p.setFont("Vazir", 16)

    # عنوان اصلی
    p.drawCentredString(width / 2, height - 50, reshape_text("سامانه بیمه زائر"))

    # مشخصات مدیر کاروان
    if manager:
        manager_info = f"{manager.full_name}        {manager.national_code:<15}"
        p.setFont("Vazir", 14)
        p.drawRightString(
            width - 50,
            height - 100,
            reshape_text(f"مدیر کاروان: {manager_info}"),
        )

    if caravan_name:
        p.drawRightString(
            width - 50,
            height - 130,
            reshape_text(f"نام کاروان: {caravan_name}"),
        )

    if insurance_code:
        # کد رهگیری بیمه‌نامه یا متن جایگزین
        p.drawRightString(
            width - 50,
            height - 160,
            reshape_text(
                f"کد رهگیری بیمه نامه: {insurance_code if insurance_code else 'لیست زیرمجموعه‌ها'}"
            ),
        )

    # عنوان لیست زائران
    p.setFont("Vazir", 15)
    p.drawRightString(width - 50, height - 200, reshape_text("لیست زائران:"))

    # لیست زائرها
    y = height - 240
    counter = 1

    for sub in items:
        if y < 100:
            p.showPage()
            p.setFont("Vazir", 14)
            y = height - 100

        p.setFont("Vazir", 13)
        p.drawRightString(
            width - 50,
            y,
            reshape_text(f"{sub.national_code}            {sub.full_name}-{counter}"),
        )
        y -= 30
        counter += 1

    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer
