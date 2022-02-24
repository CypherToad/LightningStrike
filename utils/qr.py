import base64
from io import BytesIO

from qrcode import QRCode


def create_qr(ln_invoice):
    """
    Generate a base64 encoded QR code of our lightning invoice
    """

    qr = QRCode()
    qr.add_data(ln_invoice)

    buffered = BytesIO()
    img = qr.make_image()
    img.save(buffered, format="PNG")

    buffered.seek(0)
    img_byte = buffered.getvalue()
    img_str = "data:image/png;base64," + base64.b64encode(img_byte).decode()

    return img_str
