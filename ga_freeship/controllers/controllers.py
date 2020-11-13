# -*- coding: utf-8 -*-
# from odoo import http


# class GaFreeship(http.Controller):
#     @http.route('/ga_freeship/ga_freeship/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ga_freeship/ga_freeship/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('ga_freeship.listing', {
#             'root': '/ga_freeship/ga_freeship',
#             'objects': http.request.env['ga_freeship.ga_freeship'].search([]),
#         })

#     @http.route('/ga_freeship/ga_freeship/objects/<model("ga_freeship.ga_freeship"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ga_freeship.object', {
#             'object': obj
#         })
