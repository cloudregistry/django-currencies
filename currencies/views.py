from django.http import HttpResponseRedirect
from django.utils.http import is_safe_url
from currencies.models import Currency


def set_currency(request):
    currency_code = request.POST.get('currency', request.GET.get('currency'))
    next = request.POST.get('next', request.GET.get('next'))
    if next:
        if not is_safe_url(url=next, host=request.get_host()):
            next = '/'
    else:
        next = request.META.get('HTTP_REFERER', None) or '/'

    response = HttpResponseRedirect(next)
    if currency_code:
        try:
            Currency.objects.get(code__exact=currency_code)
        except Currency.DoesNotExist:
            # ignore
            return response

        if hasattr(request, 'session'):
            request.session['currency'] = currency_code
        else:
            response.set_cookie('currency', currency_code)
    return response
