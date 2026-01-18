# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class smart_recommender(models.Model):
#     _name = 'smart_recommender.smart_recommender'
#     _description = 'smart_recommender.smart_recommender'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

