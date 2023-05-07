class PaginatedResponseMixin(object):
    def paginated_response(self, queryset=[], serializer_class=None, pagination_class=None,
                           context={}, **kwargs):
        context['request'] = self.request
        queryset = queryset or self.queryset
        pagination_class = pagination_class or self.pagination_class
        paginator = pagination_class()
        serializer_class = serializer_class or self.get_serializer_class()
        for k, v in kwargs.items():
            setattr(paginator, k, v)
        page = paginator.paginate_queryset(queryset, self.request, view=self)
        serializer = serializer_class(page, context=context, many=True)
        return paginator.get_paginated_response(serializer.data)
