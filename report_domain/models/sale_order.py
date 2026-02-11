from odoo import models, fields, api, _
from odoo.exceptions import UserError
import base64
import hashlib
import json
import requests

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_phone_pay_payment(self):
        """
        Action to initiate PhonePe payment.
        This generates a payment request to PhonePe and redirects the user to the payment page.
        """
        self.ensure_one()
        
        # NOTE: These credentials should ideally be moved to System Parameters or Settings
        # Using Sandbox credentials for demonstration.
        # Test mode configuration
        is_test_mode = True 
        
        if is_test_mode:
            # Sandbox/UAT URL
            url = "https://api-preprod.phonepe.com/apis/hermes/pg/v1/pay"
            # Standard Sandbox Credentials (Verified to work)
            merchant_id = "PGTESTPAYUAT"
            salt_key = "099eb0cd-02cf-4e2a-8aca-3e6c6aff0399"
            salt_index = "1"
        else:
            # Production Credentials (User Provided)
            merchant_id = "M235OZBIZA1D0"
            # Production URL
            url = "https://api.phonepe.com/apis/hermes/pg/v1/pay"
            salt_key = "YOUR_PRODUCTION_SALT_KEY"
            salt_index = "YOUR_PRODUCTION_SALT_INDEX"
        
        # Generate a unique transaction ID
        transaction_id = f"SO{self.id}_{fields.Datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Amount should be in paise (total * 100)
        amount_in_paise = int(self.amount_total * 100)
        
        if amount_in_paise <= 0:
            raise UserError(_("The total amount must be greater than zero to initiate a payment."))

        # Payload for PhonePe
        payload = {
            "merchantId": merchant_id,
            "merchantTransactionId": transaction_id,
            "merchantUserId": f"USER_{self.partner_id.id}",
            "amount": amount_in_paise,
            "redirectUrl": f"{self.get_base_url()}/payment/phonepe/callback", # Placeholder callback
            "redirectMode": "POST",
            "callbackUrl": f"{self.get_base_url()}/payment/phonepe/callback",
            "mobileNumber": (self.partner_id.mobile or self.partner_id.phone or "9999999999").replace(" ", ""),
            "paymentInstrument": {
                "type": "PAY_PAGE"
            }
        }

        # JSON to Base64
        payload_json = json.dumps(payload)
        payload_base64 = base64.b64encode(payload_json.encode('utf-8')).decode('utf-8')
        
        # SHA256(base64Payload + "/pg/v1/pay" + saltKey) + "###" + saltIndex
        main_string = payload_base64 + "/pg/v1/pay" + salt_key
        checksum = hashlib.sha256(main_string.encode('utf-8')).hexdigest() + "###" + salt_index
        
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "X-VERIFY": checksum
        }
        
        data = {
            "request": payload_base64
        }
        
        import logging
        _logger = logging.getLogger(__name__)
        
        _logger.info(f"PhonePe Debug - Merchant ID: {merchant_id}")
        _logger.info(f"PhonePe Debug - Salt Key: {salt_key}")
        _logger.info(f"PhonePe Debug - Checksum: {checksum}")
        _logger.info(f"PhonePe Debug - Payload Base64: {payload_base64}")
        
        try:
            response = requests.post(url, json=data, headers=headers)
            _logger.info(f"PhonePe Debug - Response Status: {response.status_code}")
            _logger.info(f"PhonePe Debug - Response Body: {response.text}")
            
            res_json = response.json()
            
            if res_json.get('success'):
                # Redirect to the PhonePe payment page
                payment_url = res_json['data']['instrumentResponse']['redirectInfo']['url']
                return {
                    'type': 'ir.actions.act_url',
                    'url': payment_url,
                    'target': 'new',
                }
            else:
                message = res_json.get('message', 'Unknown error occurred with PhonePe API')
                # DEBUG: Show which Merchant ID was used in the error to verify code update
                raise UserError(_("PhonePe Error: %s (Merchant: %s)") % (message, merchant_id))
                
        except Exception as e:
            raise UserError(_("Error connecting to PhonePe: %s") % str(e))
