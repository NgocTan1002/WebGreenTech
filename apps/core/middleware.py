from django.utils.deprecation import MiddlewareMixin


class SEOMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if response.status_code == 200:
            response['X-Canonical-URL'] = request.build_absolute_uri(request.path)
        return response


class CartMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.session.session_key:
            request.session.modified = True