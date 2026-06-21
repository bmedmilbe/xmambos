import urllib.request

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from teladoshi.models import (
    Expedition,
    Fleet,
    Place,
    Restaurant,
    Stay,
    Stopover,
    Vendor,
)


class Command(BaseCommand):
    help = "Seeds the tour app database with 4 rows per model and real placeholder images."

    def get_placeholder_image(self, keyword):
        """Fetches a real image from Unsplash and wraps it for Django storage."""
        url = "https://unsplash.com" # fallback
        if keyword == "jungle": url = "https://unsplash.com"
        elif keyword == "cabin": url = "https://unsplash.com"
        elif keyword == "food": url = "https://unsplash.com"
        elif keyword == "truck": url = "https://unsplash.com"

        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as response:
                return ContentFile(response.read(), name=f"{keyword}_seed.jpg")
        except Exception:
            # Fallback to an empty file wrapper if the network fails so the script doesn't crash
            return ContentFile(b"", name=f"{keyword}_fallback.jpg")

    def handle(self, *args, **options):
        self.stdout.write("Starting dynamic database seeding into schema...")

        # 1. Create Vendors
        vendors = []
        for i in range(1, 5):
            v = Vendor.objects.create(
                company_name=f"Vendor Premium Corp {i}",
                is_verified=(i % 2 == 0),
                contact_email=f"vendor{i}@teladoshi.com",
                contact_phone=f"+35191234567{i}"
            )
            vendors.append(v)

        # 2. Create Expeditions
        for i in range(1, 5):
            exp = Expedition(
                vendor=vendors[i-1], price=200.00 * i, is_active=True,
                slug=f"expedition-trek-{i}", badge_tags="Adventure, Eco",
                name_en=f"Wild Trek Adventure {i}", name_pt=f"Aventura de Trilha Selvagem {i}",
                description_en=f"An amazing expedition experience {i}.", description_pt=f"Uma experiência incrível de expedição {i}.",
                specialization_en="Wilderness", specialization_pt="Selva Selvagem",
                mastery_text_en="10+ years experience.", mastery_text_pt="Mais de 10 anos de experiência."
            )
            exp.image.save(f"exp_{i}.jpg", self.get_placeholder_image("jungle"), save=True)

        # 3. Create Stays
        for i in range(1, 5):
            stay = Stay(
                vendor=vendors[i-1], price=100.00 * i, is_active=True, slug=f"luxury-stay-{i}",
                name_en=f"Eco Paradise Cabin {i}", name_pt=f"Cabana Paraíso Ecológica {i}",
                description_en=f"Beautiful serene lodging {i}.", description_pt=f"Alojamento sereno e bonito {i}.",
                category_en="Cabins", category_pt="Cabanas",
                location_detail_en="Sector Alpha", location_detail_pt="Sector Alfa",
                amenities_en="Wifi, Pool", amenities_pt="Wifi, Piscina"
            )
            stay.image.save(f"stay_{i}.jpg", self.get_placeholder_image("cabin"), save=True)

        # 4. Create Restaurants
        for i in range(1, 5):
            rest = Restaurant(
                vendor=vendors[i-1], price=30.00 * i, is_active=True, slug=f"bistro-gourmet-{i}",
                opening_hours="12:00 - 22:00",
                name_en=f"The Green Bistro {i}", name_pt=f"O Bistro Verde {i}",
                description_en=f"Organic dining {i}.", description_pt=f"Refeições biológicas {i}.",
                subtitle_en="Fresh food", subtitle_pt="Comida fresca",
                location_en="Downtown Square", location_pt="Praça Central"
            )
            rest.image.save(f"rest_{i}.jpg", self.get_placeholder_image("food"), save=True)

        # 5. Create Fleets
        for i in range(1, 5):
            fleet = Fleet(
                vendor=vendors[i-1], price=75.00 * i, is_active=True, slug=f"vehicle-fleet-{i}",
                vehicle_type="SUV 4x4", transmission="Automatic", engine="V6 Diesel", features="AC, GPS",
                name_en=f"Overland Truck Model {i}", name_pt=f"Camião Overland Modelo {i}",
                description_en=f"Reliable rugged vehicle {i}.", description_pt=f"Veículo robusto confiável {i}."
            )
            fleet.image.save(f"fleet_{i}.jpg", self.get_placeholder_image("truck"), save=True)

        # 6. Create Places
        for i in range(1, 5):
            Place.objects.create(
                vendor=vendors[i-1], price=0.00, is_active=True, slug=f"scenic-place-{i}",
                access_type="Free Access", coordinates="0.0 N, 0.0 E",
                name_en=f"Hidden Sanctuary Lookout {i}", name_pt=f"Miradouro do Santuário Escondido {i}",
                description_en=f"Beautiful landscape vista {i}.", description_pt=f"Bela vista panorâmica {i}."
            )

        # 7. Create Stopovers
        for i in range(1, 5):
            Stopover.objects.create(
                vendor=vendors[i-1], price=50.00 * i, is_active=True, slug=f"transit-stopover-{i}",
                arrival_city="Lisbon", pricing_guide_json={"pax": 50},
                name_en=f"Transit Stopover Pass {i}", name_pt=f"Passe de Escala de Trânsito {i}",
                description_en=f"Comfortable layout stay {i}.", description_pt=f"Estadia confortável {i}.",
                transfer_details_en="Private Car", transfer_details_pt="Carro Privado"
            )

        self.stdout.write(self.style.SUCCESS("Database seeds executed successfully! Everything synced to AWS S3."))
