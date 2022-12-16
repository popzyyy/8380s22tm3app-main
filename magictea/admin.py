from django.contrib import admin
from .models import Unit, Category, Product, Order, OrderItem
from django.http import HttpResponse
import csv
import datetime
from django.urls import reverse
from django.utils.safestring import mark_safe
# Register your models here.


class UnitAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_date', 'updated_date']
    list_filter = ['name', 'description', 'created_date', 'updated_date']
    prepopulated_fields = {'description': ('name',)}


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_date', 'updated_date']
    list_filter = ['name', 'created_date', 'updated_date']


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'image', 'price', 'available', 'product_unit', 'product_category',
                    'created_date', 'updated_date']
    list_filter = ['name', 'description', 'image', 'price', 'available', 'product_unit', 'product_category',
                   'created_date', 'updated_date']


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    content_disposition = f'attachment; filename={opts.verbose_name}.csv'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = content_disposition
    writer = csv.writer(response)
    fields = [field for field in opts.get_fields() if not field.many_to_many \
              and not field.one_to_many]
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


def order_pdf(obj):
    url = reverse('magictea:admin_order_pdf', args=[obj.id])
    return mark_safe(f'<a href="{url}">PDF</a>')
    order_pdf.short_description = 'Invoice'


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'address', 'postal_code', 'city', 'braintree_id',
                    'created_date', 'updated_date', 'paid', order_pdf]
    list_filter = ['paid', 'created_date', 'updated_date']
    inlines = [OrderItemInline]
    actions = [export_to_csv]


admin.site.register(Unit, UnitAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
