# -*- coding: utf-8 -*-
# from odoo import http


# class SmartRecommender(http.Controller):
#     @http.route('/smart_recommender/smart_recommender', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/smart_recommender/smart_recommender/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('smart_recommender.listing', {
#             'root': '/smart_recommender/smart_recommender',
#             'objects': http.request.env['smart_recommender.smart_recommender'].search([]),
#         })

#     @http.route('/smart_recommender/smart_recommender/objects/<model("smart_recommender.smart_recommender"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('smart_recommender.object', {
#             'object': obj
#         })

