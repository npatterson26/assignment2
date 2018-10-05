import csv
import datetime
from django.http import HttpResponse
from django.contrib import admin
from .models import Customer, Service, Product


def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;' \
                                      'filename={}.csv'.format(opts.verbose_name)
    writer = csv.writer(response)

    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
    # Write a first row with header information
    writer.writerow([field.verbose_name for field in fields])
    # Write data rows
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response


export_to_csv.short_description = 'Export to CSV'

class CustomerList(admin.ModelAdmin):
    list_display = ( 'cust_name', 'organization', 'phone_number' )
    list_filter = ( 'cust_name', 'organization')
    search_fields = ('cust_name', )
    ordering = ['cust_name']
    actions = [export_to_csv]


class ServiceList(admin.ModelAdmin):
    list_display = ( 'cust_name', 'service_category', 'setup_time')
    list_filter = ( 'cust_name', 'setup_time')
    search_fields = ('cust_name', )
    ordering = ['cust_name']
    actions = [export_to_csv]


class ProductList(admin.ModelAdmin):
    list_display = ( 'cust_name', 'product', 'pickup_time')
    list_filter = ( 'cust_name', 'pickup_time')
    search_fields = ('cust_name', )
    ordering = ['cust_name']
    actions = [export_to_csv]


admin.site.register(Customer, CustomerList)
admin.site.register(Service, ServiceList)
admin.site.register(Product, ProductList)
