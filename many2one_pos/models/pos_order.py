from odoo import fields, models, api


class PosOrder(models.Model):
    _inherit = 'pos.order'

    # 📝 1. Define the Many2one field
    custom_partner_id = fields.Many2one(
        'res.partner',
        string='Custom Partner',
        store=True  # Ensure it's stored in the database
    )

    # 🚀 2. Load the field to the POS session
    # This is the Odoo 18 way to load fields to the frontend
    @api.model
    def _load_pos_data_fields(self, config_id):
        # Call super to get existing fields
        fields = super()._load_pos_data_fields(config_id)
        # Add your custom field
        fields.append('custom_partner_id')
        return fields