from django.contrib import admin
from .models import Course, Instructor
from .models import Payment
from django.utils.html import format_html


class InstructorAdmin(admin.ModelAdmin):
    list_display = ("name", "credentials")
    search_fields = ("name", "credentials")
    ordering = ("name",)


class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "instructor",
        "enrollment_year",
        "current_price",
        "original_price",
        "get_discount_percentage",
    )
    list_filter = ("instructor", "enrollment_year")
    search_fields = ("title", "instructor__name")
    ordering = ("title",)
    readonly_fields = ("image_preview",)

    def get_topics_count(self, obj):
        try:
            return obj.topics.count()
        except Exception:
            return 0

    get_topics_count.short_description = "Topics"

    def get_discount_percentage(self, obj):
        if obj.original_price > 0:
            discount = ((obj.original_price - obj.current_price) / obj.original_price) * 100
            return f"{int(discount)}%"
        return "0%"

    get_discount_percentage.short_description = "Discount"

    # legacy rating removed

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 200px;"/>', obj.image.url)
        return "No image uploaded"

    image_preview.short_description = "Image Preview"


admin.site.register(Instructor, InstructorAdmin)
admin.site.register(Course, CourseAdmin)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "course",
        "user_email",
        "amount",
        "currency",
        "status",
        "transaction_id",
        "created_at",
    )
    search_fields = ("user_email", "transaction_id", "session_key")
    list_filter = ("status", "currency")
