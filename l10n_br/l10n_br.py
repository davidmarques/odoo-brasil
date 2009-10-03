# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution	
#    Copyright (C) 2004-2008 Tiny SPRL (<http://tiny.be>). All Rights Reserved
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from osv import osv, fields

##############################################################################
# Municipios e Códigos do IBGE
##############################################################################
class l10n_br_city(osv.osv):
    _name = 'l10n_br.city'
    _description = 'Municipios e Códigos do IBGE'
    _columns = {
        'name': fields.char('Nome', size=64, required=True),
        'state_id': fields.many2one('res.country.state', 'Estado', required=True),
        'ibge_code': fields.char('Codigo IBGE', size=7),
    }
l10n_br_city()

##############################################################################
# CEP - Código de endereçamento Postal
##############################################################################
class l10n_br_cep(osv.osv):
    _name = 'l10n_br.cep'
    _rec_name = 'code'
    _columns = {
        'code': fields.char('CEP', size=8, required=True),
        'street_type': fields.char('Tipo', size=26),
        'street': fields.char('Logradouro', size=72),
        'district': fields.char('Bairro', size=72),
        'state_id': fields.many2one('res.country.state', 'Estado', required=True),
    }
l10n_br_cep()

##############################################################################
# CFOP - Código Fiscal de Operações e Prestações
##############################################################################
class l10n_br_cfop(osv.osv):
    _description = 'CFOP - Código Fiscal de Operações e Prestações'
    _name = 'l10n_br.cfop'
    _columns = {
        'code': fields.char('Código', size=4),
        'name': fields.char('Nome', size=256),
        'small_name': fields.char('Nome Reduzido', size=32),
        'description': fields.text('Descrição'),
        'type': fields.selection([('input', 'Entrada'), ('output', 'Saida')], 'Tipo'),
        'parent_id': fields.many2one('l10n_br.cfop', 'CFOP Pai'),
        'child_ids': fields.one2many('l10n_br.cfop', 'parent_id', 'CFOP filhos'),
    }
l10n_br_cfop()

##############################################################################
# NCM - Nomeclatura Comun do Mercosul
##############################################################################
class l10n_br_ncm(osv.osv):
    _name = 'l10n_br.ncm'
    _description = 'NCM - Nomeclatura Comun do Mercosul'
    _columns = {
        'code': fields.char('Codigo', size=10),
        'name': fields.char('Nome', size=68),
        'aliquot': fields.float('Aliquota'),
        'tax_id': fields.many2one('account.tax', 'Imposto'),
    }

    def name_search(self, cr, user, name='', args=None, operator='ilike', context=None, limit=80):
        if not args:
            args = []
        if not context:
            context = {}
        if name:
            ids = self.search(cr, user, [('code', '=', name)] + args, limit=limit, context=context)
            if not len(ids):
                ids = self.search(cr, user, [('name', '=', name)] + args, limit=limit, context=context)
            if not len(ids):
                ids = self.search(cr, user, [('code', operator, name)] + args, limit=limit, context=context)
                ids += self.search(cr, user, [('name', operator, name)] + args, limit=limit, context=context)
        else:
            ids = self.search(cr, user, args, limit=limit, context=context)
        return self.name_get(cr, user, ids, context)

l10n_br_ncm()

##############################################################################
# Tipo de Documento Fiscal
##############################################################################
class l10n_br_fiscal_document(osv.osv):
    _name = 'l10n_br.fiscal.document'
    _description = 'Tipo de Documento Fiscal'
    _columns = {
        'code': fields.char('Codigo', size=8),
        'name': fields.char('Descrição', size=64),
        'nfe': fields.boolean('NFe'),
    }
l10n_br_fiscal_document()

##############################################################################
# Nota Fiscal
##############################################################################
#class l10n_br_nf(osv.osv):
#    _description = 'Nota Fiscal'
#    _name = 'l10n_br.nf'
#    _columns = {
#        'company_id': fields.many2one('res.company', 'Empresa'),
#        'partner_id': fields.many2one('res.partner', 'Parceiro'),
#        'partner_address_id': fields.many2one('res.partner.address', 'Contato'),
#        'partner_adr_delivery_id': fields.many2one('res.partner.address', 'Endereço'),
#        'cnpj_cpf': fields.char('CNPJ/CPF', size=16),
#        'insc_est': fields.char('Inscrição Estadual', size=16),
#        'street': fields.char('Endereço', size=128),
#        'street_number': fields.char('Número', size=16),
#        'district': fields.char('Bairro', size=64),
#        'country_id': fields.many2one('res.country', 'Pais'),
#        'state_id': fields.many2one('res.country.state', 'Estado'),
#        'city_id': fields.many2one('l10n_br.city', 'Cidade'),
#        'zip': fields.char('CEP', size=10),
#        'contact_phone': fields.char('Telefone', size=12),
#        'number': fields.integer('Número'),
#        'canceled': fields.boolean('Cancelada'),
#        'printed': fields.boolean('Impressa'),
#        'cfop_id': fields.many2one('l10n_br.cfop', 'CFOP'),
#        'date': fields.date('Data', required=True),
#        'date_out': fields.date('Data Saida'),
#        'type': fields.selection([('input', 'Entrada'), ('output', 'Saida')], 'Tipo'),
#        'amount_products': fields.float('Total Mercadoria'),
#        'amount_total': fields.float('Total Geral'),
#        'amount_icms': fields.float('Total ICMS'),
#        'base_icms': fields.float('Base ICMS'),
#        'amount_ipi': fields.float('Total IPI'),
#        'base_ipi': fields.float('Base IPI'),
#        'nf_line': fields.one2many('l10n_br.nf.line', 'nf_id', 'Order Lines'),
#        'body_note': fields.text('Observações Corpo'),
#        'foot_note': fields.text('Observações Rodapé'),
#    }
#
#    def onchange_partner_id(self, cr, uid, ids, part):
#        if not part:
#            return {'value':{'partner_address_id': False}}
#        addr = self.pool.get('res.partner').address_get(cr, uid, [part], ['default'])
#        part = self.pool.get('res.partner').browse(cr, uid, part)
#        street = addr['default'].street
#        street_number = addr['default'].number
#        district = addr['default'].street2
#        cep = addr['default'].zip
#        contact_phone = addr['default'].phone
#        state_id = addr['default'].state_id.id
#        country_id = addr['default'].country_id.id
#        return {'value':{'partner_address_id': addr['default'], 'street': street, 'street_number': street_number, 'district' : district, 'cep' : cep, 'contact_phone' : contact_phone, 'state_id' : contact_phone, 'country_id' : country_id}}
#
#l10n_br_nf()

##############################################################################
# Linhas da Nota Fiscal
##############################################################################
#class l10n_br_nf_line(osv.osv):
#    _name = 'l10n_br.nf.line'
#    _description = 'Linhas da Nota Fiscal'
#    _columns = {
#        'nf_id': fields.many2one('l10n_br.nf', 'Nota Fiscal', required=True, ondelete='cascade', select=True),
#        'sequence': fields.integer('Sequência'),
#        'product_id': fields.many2one('product.product', 'Produto', change_default=True),
#        'name': fields.char('Descrição', size=256, required=True, select=True),
#        'product_qty': fields.float('Quantidade', digits=(16, 2), required=True),
#        'product_uom': fields.many2one('product.uom', 'Unidade', required=True),
#        'price_unit': fields.float('Preço Unit', required=True),
#        'price_subtotal': fields.float('Total'),
#    }
#l10n_br_nf_line()

##############################################################################
# Configurações fiscais das Empresas
##############################################################################
#l10n_br_company_config(osv.osv):
#    _name = 'l10n_br.company.config'
#    _description = 'Configurações fiscais das Empresas'
#    _columns = {
#        'company_id': fields.many2one('res.company','Empresa', required=True),
#    }
#l10n_br_company_config()


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
