#!/usr/bin/env python3

import sys
import os
import time
import uuid
from datetime import datetime, timezone

import json
import requests


# Strike api documentation
# docs.strike.me
#
# Strike api token should be set as a env variable
TOKEN = os.environ['TOKEN']

dry_run=False
if not TOKEN:
    dry_run=True


# Basic auth headers for strike api
HEADERS = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'Authorization': 'Bearer %s' % TOKEN
}


def create_invoice(description, amount):
    """
    Call strike's restful api to create a new invoice
    """

    cor_id = uuid.uuid4().hex
    url = "https://api.strike.me/v1/invoices"

    payload = json.dumps({
      "correlationId": cor_id,
      "description": description,
      "amount": {
        "currency": "USD",
        "amount": amount
      }
    })

    if dry_run:
        return {
            'created': str(datetime.utcnow().replace(tzinfo=timezone.utc)),
            'invoice_id': '000000000-0000-0000-0000-000000000000',
            'cor_id': cor_id,
            'description': description,
            'amount': amount
        }
    else:
        response = requests.request("POST", url, headers=HEADERS, data=payload)
        response.raise_for_status()
        rj = response.json()

        created = rj['created']
        invoice_id = rj['invoiceId']
        description = rj['description']
        price = rj['amount']['amount']
        state = 'CREATED'

        return {
            'created': created,
            'invoice_id': invoice_id,
            'cor_id': rj['correlationId'],
            'description': description,
            'amount': price
        }



def get_invoice(invoice_id):
    """
    Call strike's restful api to get an invoice by id
    """

    url = "https://api.strike.me/v1/invoices/%s" % invoice_id
    payload={}

    if dry_run:
        return {
            'created': str(datetime.utcnow().replace(tzinfo=timezone.utc)),
            'invoice_id': '000000000-0000-0000-0000-000000000000',
            'cor_id': 'b3c540adfe3b4185b481ae1a467afbeb',
            'description': 'Coffee',
            'amount': '0.01',
            'state': 'PAID'
        }
    else:
        response = requests.request("GET", url, headers=HEADERS, data=payload)
        response.raise_for_status()

        rj = response.json()

        created = rj['created']
        invoice_id = rj['invoiceId']
        description = rj['description']
        price = rj['amount']['amount']
        state = rj['state']

        return {
            'created': created,
            'invoice_id': invoice_id,
            'cor_id': rj['correlationId'],
            'description': description,
            'amount': price,
            'state': state
        }


def create_ln_invoice(invoice_id):
    """
    Call strike's restful api to create a new lightning quote
    """

    url = "https://api.strike.me/v1/invoices/%s/quote" % invoice_id
    payload={}

    if dry_run:
        return {
            'ln_invoice': 'lnbc1pvjluezsp5zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zygspp5qqqsyqcyq5rqwzqfqqqsyqcyq5rqwzqfqqqsyqcyq5rqwzqfqypqdpl2pkx2ctnv5sxxmmwwd5kgetjypeh2ursdae8g6twvus8g6rfwvs8qun0dfjkxaq9qrsgq357wnc5r2ueh7ck6q93dj32dlqnls087fxdwk8qakdyafkq3yap9us6v52vjjsrvywa6rt52cm9r9zqt8r2t7mlcwspyetp5h2tztugp9lfyql',
            'expiration_in_sec': 117
        }
    else:
        response = requests.request("POST", url, headers=HEADERS, data=payload)
        response.raise_for_status()

        rj = response.json()
        return {
            'ln_invoice': rj['lnInvoice'],
            'expiration_in_sec': rj['expirationInSec']
        }


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
