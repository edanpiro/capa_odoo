# coding: utf-8


from openerp import models, api, fields


class ResParner(models.Model):
    _inherit = 'res.partner'

    apellido = fields.Char('Apellidos', size=20)

    @api.one
    def onchange_type(self, is_company):
        val = super(ResParner, self).onchange_type(is_company=is_company)
        val['value'].update({
            'apellido': 'hola'
        })
        return val


    @api.model
    def create(self, values):
        print values
        return super(ResParner, self).create(values)

    @api.one
    def write(self, values):
        return super(ResParner, self).write(values)
