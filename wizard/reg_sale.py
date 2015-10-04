# coding: utf-8


from xlwt import Workbook, easyxf, Formula
from openerp import models, fields, api


class RegSale(models.TransientModel):
    _name = 'reg.sale'

    company_id = fields.Many2one('res.company', 'Compañia', required=True,
                                 default=lambda self: self.env['res.company']._company_default_get('reg.sale'))
    period_id = fields.Many2one('account.period', required=True)



class RegSaleXls(models.AbstractModel):
    _inherit = 'download.file.base.model'
    _name = 'reg.sale.xls'

    def init(self, record_id):
        super(RegSaleXls, self).init(record_id)

    def get_filename(self):
        return "RegistroVentas.xls"

    def get_content(self):
        invoice = self.env['account.invoice']
        reg_sale = self.env['reg.sale'].browse(self.record_id)

        wbk = Workbook()
        style0 = easyxf('font: height 160, name Times new Roman, bold on;''align: wrap on, horiz justified;')
        style1 = easyxf('font: height 160, name Times new Roman, bold on;''align: wrap on, horiz justified;''borders: left thin, right thin, top thin, bottom thin')
        style2 = easyxf('font: height 200, name Times new Roman, bold on;''borders: top thin;', num_format_str='0.00')
        style3 = easyxf(num_format_str='0.00')

        s0 = 0
        s1 = 1
        s2 = 2
        s3 = 3
        s4 = 4
        s5 = 5
        s6 = 6
        s7 = 7
        s8 = 8

        ws = wbk.add_sheet('Registro de Venta')
        ws.row(5).height = 200 * 2
        ws.row(6).height = 1000
        ws.col(8).width = 10000

        ws.write_merge(s0, s0, 0, 1, 'FORMATO 14.1', style0)
        ws.write_merge(s0, s0, 2, 3, 'REGISTRO DE VENTAS E INGRESO', style0)
        ws.write(s1, 0, 'PERIODO', style0)
        ws.write(s1, 1, reg_sale.period_id.name, style0)
        ws.write_merge(s2, s2, 0, 3, 'APELLIDOS Y NOMBRES, DENOMINACION O RAZON SOCIAL', style0)
        ws.write_merge(s2, s2, 4, 6, reg_sale.company_id.name, style0)
        ws.write_merge(s4, s6, 0, 0, 'NUMERO CORRELATIVO DE REGISTRO O CODIGO UNICO DE LA OPERACION', style1)
        ws.write_merge(s4, s6, 1, 1, 'FECHA DE EMISION DE COMPROBANTE DE PAGO O DOCUMENTO', style1)
        ws.write_merge(s4, s6, 2, 2, 'FECHA DE PAGO Y/O VENCIMIENTO', style1)
        ws.write_merge(s4, s4, 3, 5, 'COMPROBANTE DE PAGO O DOCUMENTO', style1)
        ws.write_merge(s4, s4, 6, 8, 'INFORMACION DEL CLIENTE', style1)
        ws.write_merge(s5, s6, 3, 3, 'TIPO (TABLA 10)', style1)
        ws.write_merge(s5, s6, 4, 4, 'N° SERIE O N° SERIE DE LA MAQUINA REGISTRADORA'.decode('utf-8'), style1)
        ws.write_merge(s5, s6, 5, 5, 'NUMERO', style1)
        ws.write_merge(s5, s5, 6, 7, 'DOCUMENTO DE IDENTIDAD', style1)
        ws.write(s6, 6, 'TIPO (TABLA 2)', style1)
        ws.write(s6, 7, 'NUMERO', style1)
        ws.write_merge(s5, s6, 8, 8, 'APELLIDOS Y NOMBRES, DENOMICACION O RAZON SOCIAL', style1)
        ws.write_merge(s4, s6, 9, 9, 'VALOR FACTURADO DE LA EXPORTACION', style1)
        ws.write_merge(s4, s6, 10, 10, 'BASE IMPONIBLE DE LA OPERACION GRAVADA', style1)
        ws.write_merge(s4, s4, 11, 12, 'IMPORTE DE LA OPERACION EXONERADA O INAFECTA', style1)
        ws.write_merge(s5, s6, 11, 11, 'EXONERADA', style1)
        ws.write_merge(s5, s6, 12, 12, 'INAFECTA', style1)
        ws.write_merge(s4, s6, 13, 13, 'IGV Y/0 IPM', style1)
        ws.write_merge(s4, s6, 14, 14, 'IMPORTE DEL COMPROBANTE DE PAGO', style1)
        ws.write_merge(s4, s6, 15, 15, 'TIPO DE CAMBIO', style1)
        ws.write_merge(s4, s4, 16, 19, 'REFERENCIA DE COMPROBANTE DE PAGO O DOCUMENTO ORIGINAL QUE SE MODIFICA', style1)
        ws.write_merge(s5, s6, 16, 16, 'FECHA', style1)
        ws.write_merge(s5, s6, 17, 17, 'TIPO (TABLA 10)', style1)
        ws.write_merge(s5, s6, 18, 18, 'SERIE', style1)
        ws.write_merge(s5, s6, 19, 19, 'N° DEL COMPROBANTE DE PAGO O DOCUMENTO'.decode('utf-8'), style1)

        args = [('state', 'not in', ('draft', 'proforma', 'proforma2')),
                ('period_id', '=', reg_sale.period_id.id),
                ('type', 'in', ('out_invoice', 'out_refund')),
                ('company_id', '=', reg_sale.company_id.id)]
        invoice_id = invoice.search(args)
        if invoice_id:
            count = 1
            for obj_invoice in invoice_id:
                date_refund = ''
                table10_refund = 0
                serie_refund = ''
                number_refund = ''
                exchange_rate = 0
                operation_untaxed = 0.00
                total = obj_invoice.move_id.amount
                igv = obj_invoice.amount_tax
                base_impo = 0.00
                # company_currency = obj_invoice.currency_id
                currency_invoice = obj_invoice.currency_id
                currency_company = obj_invoice.company_id.currency_id
                cut_number = obj_invoice.voucher_number.split('-') if obj_invoice.voucher_number else '0'
                customer = obj_invoice.partner_id.name
                vat = obj_invoice.partner_id.vat
                num_origin = 0
                if obj_invoice.type == 'out_refund':
                    num_origin = obj_invoice.name
                    arg2 = [('voucher_number', '=', num_origin)]
                    origin_id = invoice.search(arg2, limit=1)
                    if origin_id:
                        date_refund = origin_id.date_invoice
                        table10_refund = 3
                        serie_refund = num_origin.split('-')[0]
                        number_refund = num_origin.split('-')[1]
                for invoice_line in obj_invoice.invoice_line:
                    for tax in invoice_line.invoice_line_tax_id:
                        if tax.operation_untaxed:
                            operation_untaxed += invoice_line.price_subtotal
                        else:
                            base_impo += invoice_line.price_subtotal
                if currency_invoice != currency_company:
                    currency = obj_invoice.currency_id.with_context(date=obj_invoice.date_invoice)
                    exchange_rate = obj_invoice.exchange_rate
                    igv = currency.compute(igv, currency_company)
                    operation_untaxed = currency.compute(operation_untaxed, currency_company)
                    base_impo = currency.compute(base_impo, currency_company)
                if obj_invoice.state == 'cancel' and obj_invoice.voucher_number:
                    total = 0.00
                    igv = 0.00
                    base_impo = 0.00
                    customer = 'ANULADO'
                    vat = '99999999999'
                    operation_untaxed = 0.00
                if len(cut_number) == 2:
                    ws.write(s7, 0, count)
                    ws.write(s7, 1, obj_invoice.date_invoice)
                    ws.write(s7, 2, obj_invoice.date_due)
                    ws.write(s7, 3, obj_invoice.journal_id.document_id.code if obj_invoice.journal_id.document_id else False)
                    ws.write(s7, 4, cut_number[0])
                    ws.write(s7, 5, cut_number[1])
                    ws.write(s7, 6, obj_invoice.partner_id.document_type)
                    ws.write(s7, 7, vat)
                    ws.write(s7, 8, customer)
                    ws.write(s7, 9, count)
                    ws.write(s7, 10, base_impo)
                    ws.write(s7, 11, operation_untaxed)
                    ws.write(s7, 13, igv)
                    ws.write(s7, 14, total)
                    ws.write(s7, 15, exchange_rate)
                    ws.write(s7, 16, date_refund)
                    ws.write(s7, 17, table10_refund)
                    ws.write(s7, 18, serie_refund)
                    ws.write(s7, 19, number_refund)
                    count += 1
                    s7 += 1
            ws.write(s7, 10, Formula('SUM($K8:$k%d)' % (s7)), style2)
            ws.write(s7, 11, Formula('SUM($L8:$L%d)' % (s7)), style2)
            ws.write(s7, 13, Formula('SUM($N8:$N%d)' % (s7)), style2)
            ws.write(s7, 14, Formula('SUM($O8:$O%d)' % (s7)), style2)
        file_data = StringIO.StringIO()
        wbk.save(file_data)
        return file_data.getvalue()
