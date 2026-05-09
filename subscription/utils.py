def for_merchant(queryset, user):
    return queryset.filter(merchant=user.merchant)