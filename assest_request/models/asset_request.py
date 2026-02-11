from odoo import models, fields, api, _, exceptions
from odoo.exceptions import UserError

class AssetType(models.Model):
    _name = 'asset.type'
    _description = 'Asset Type'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')

class AssetRequest(models.Model):
    _name = 'asset.request'
    _description = 'Asset Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    name = fields.Char(
        string='Reference', 
        required=True, 
        copy=False, 
        readonly=True, 
        default=lambda self: _('New')
    )
    employee_id = fields.Many2one(
        'hr.employee', 
        string='Employee', 
        required=True, 
        tracking=True
    )
    department_id = fields.Many2one(
        'hr.department', 
        string='Department', 
        related='employee_id.department_id',
        readonly=False,
        store=True,
        tracking=True
    )
    asset_type_ids = fields.Many2many(
        'asset.type', 
        string='Asset Types',
        tracking=True
    )
    reason = fields.Text(
        string='Reason',
        tracking=True
    )
    request_date = fields.Date(
        string='Request Date', 
        default=fields.Date.context_today, 
        tracking=True
    )
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], string='Status', default='draft', tracking=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('asset.request') or _('New')
        return super().create(vals_list)

    def action_submit(self):
        self.state = 'submitted'

    def action_approve(self):
        for record in self:
            if record.department_id and record.department_id.manager_id and record.department_id.manager_id.user_id != self.env.user:
                raise UserError(_("Only the Manager of %s can approve this request.") % record.department_id.name)
        self.state = 'approved'

    def action_reject(self):
        for record in self:
            if record.department_id and record.department_id.manager_id and record.department_id.manager_id.user_id != self.env.user:
                raise UserError(_("Only the Manager of %s can reject this request.") % record.department_id.name)
        self.state = 'rejected'
