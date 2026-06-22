# Adjust the app name string below if your order app directory has a different name
from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from .models import (
    Post,
    Expedition,
    Fleet,
    Place,
    Restaurant,
    ServiceImage,
    Souvenir,
    Stay,
    Stopover,
    Vendor,
)


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = [
            "id",
            "company_name",
            "is_verified",
            "contact_email",
            "contact_phone",
            "logo",
        ]


class ServiceImageSerializer(serializers.ModelSerializer):
    attached_to = serializers.SerializerMethodField()

    class Meta:
        model = ServiceImage
        fields = ["id", "image", "alt_text", "object_id", "content_type", "attached_to"]

    def get_attached_to(self, obj):
        # 1. Fallback mechanisms to extract the ID and model type safely
        obj_id = obj.object_id
        model_name = obj.content_type.model if obj.content_type else None

        data = {"id": obj_id, "model_type": model_name}

        # # 2. Add resource-specific name/title fields dynamically if object is loaded
        # target = (
        #     getattr(obj, "content_object", None) if not isinstance(obj, dict)
        # else None
        # )
        # if target:
        #     data["display_name"] = getattr(target, "name"]

        return data


Review = apps.get_model("order", "Review")


class CatalogReviewSerializer(serializers.ModelSerializer):
    """Clean serialisation for customer reviews nested inside service responses."""

    attached_to = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = [
            "id",
            "customer",
            "content",
            "rating",
            "object_id",
            "content_type",
            "attached_to",
        ]

    def get_attached_to(self, obj):
        # 1. Fallback mechanisms to extract the ID and model type safely

        obj_id = obj.object_id
        model_name = obj.content_type.model if obj.content_type else None
        data = {"id": obj_id, "model_type": model_name}

        return data


# Base Serializer


class BaseServiceSerializer(serializers.ModelSerializer):
    vendor_name = serializers.ReadOnlyField(source="vendor.company_name")
    is_vendor_verified = serializers.ReadOnlyField(source="vendor.is_verified")
    # allow setting vendor by id when creating/updating services
    vendor_id = serializers.PrimaryKeyRelatedField(
        source="vendor", queryset=Vendor.objects.all(), write_only=True, required=False
    )
    gallery = ServiceImageSerializer(many=True, read_only=True)
    reviews = serializers.SerializerMethodField()

    def get_reviews(self, obj):
        """Fetches all generic reviews assigned to this specific service instance."""

        content_type = ContentType.objects.get_for_model(obj)
        reviews = Review.objects.filter(content_type=content_type, object_id=obj.id)
        return CatalogReviewSerializer(reviews, many=True).data


class ExpeditionSerializer(BaseServiceSerializer):
    vendor = VendorSerializer(read_only=True)

    class Meta:
        model = Expedition
        # Added 'reviews' to fields array
        fields = [
            "id",
            "vendor",
            "vendor_id",
            "is_vendor_verified",
            "name",
            "description",
            "price",
            "image",
            "is_active",
            "slug",
            "gallery",
            "reviews",
            "specialization",
            "badge_tags",
            "mastery_text",
            "languages"
        ]


class StaySerializer(BaseServiceSerializer):
    class Meta:
        model = Stay
        # Added 'reviews' to fields array
        fields = [
            "id",
            "vendor_name",
            "vendor_id",
            "is_vendor_verified",
            "name",
            "description",
            "price",
            "image",
            "is_active",
            "slug",
            "gallery",
            "reviews",
            "category",
            "location_detail",
            "amenities",
            "cap",
            "is_house",
            "rating"
        ]


class FleetSerializer(BaseServiceSerializer):
    class Meta:
        model = Fleet
        # Added 'reviews' to fields array
        fields = [
            "id",
            "vendor_name",
            "vendor_id",
            "is_vendor_verified",
            "name",
            "description",
            "price",
            "image",
            "is_active",
            "slug",
            "gallery",
            "reviews",
            "vehicle_type",
            "transmission",
            "engine",
            "features",
            "seats"
        ]


class RestaurantSerializer(BaseServiceSerializer):
    class Meta:
        model = Restaurant
        # Added 'reviews' to fields array
        fields = [
            "id",
            "vendor_name",
            "vendor_id",
            "is_vendor_verified",
            "name",
            "description",
            "price",
            "image",
            "is_active",
            "slug",
            "gallery",
            "reviews",
            "subtitle",
            "location",
            "opening_hours",
        ]


class PlaceSerializer(BaseServiceSerializer):
    class Meta:
        model = Place
        fields = [
            "id",
            "vendor_name",
            "vendor_id",
            "is_vendor_verified",
            "name",
            "description",
            "price",
            "image",
            "is_active",
            "slug",
            "gallery",
            "reviews",
            "access_type",
            "coordinates",
        ]


class StopoverSerializer(BaseServiceSerializer):
    class Meta:
        model = Stopover
        fields = [
            "id",
            "vendor_name",
            "vendor_id",
            "is_vendor_verified",
            "name",
            "description",
            "price",
            "image",
            "is_active",
            "slug",
            "gallery",
            "reviews",
            "arrival_city",
            "pricing_guide_json",
            "transfer_details",
        ]



class SouvenirSerializer(BaseServiceSerializer):
    # Displays the clean human-readable label ("Flavors") instead of the database value
    #  ("flavors")
    category_display = serializers.CharField(source='get_category_display',
                                              read_only=True)

    # Optional: Read-only representations of your Generic Relations if
    reviews_count = serializers.IntegerField(source='reviews.count', read_only=True)

    class Meta:
        model = Souvenir
        fields = [
            'id',
            'vendor',
            'name',
            'description',
            'price',
            'image',
            'is_active',
            'slug',
            'category',
            'category_display',
            'gallery',
            'reviews_count',
            'reviews',
        ]



class PostSerializer(serializers.ModelSerializer):
    beginning = serializers.SerializerMethodField(method_name="get_beginning")
    text = serializers.CharField(read_only=True)
    user = serializers.StringRelatedField(read_only=True)
    category = serializers.CharField(read_only=True)
    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 'picture', 'user','category',
                  'beginning', 'text', 'date', 'language', 'read_time']


    def get_beginning(self, post: Post):
        """Return first 100 chars from description (auto-generated by signal)."""
        if post.description:
            return post.description
        return ""

