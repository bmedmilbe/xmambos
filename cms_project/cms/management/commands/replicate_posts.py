# cms_project/cms/management/commands/replicate_posts.py
from django.core.management.base import BaseCommand, CommandError
from django.utils.timezone import now
from django_tenants.utils import get_tenant_model, tenant_context

# Import your real Post and PostImage models directly from your app layer
from cms.models import Post, PostImage


class Command(BaseCommand):
    help = "Copies and clones all Post records from the 'cecab' tenant workspace into 'teladoshi'."

    def handle(self, *args, **options):
        TenantModel = get_tenant_model()

        # 1. Grab our source and target tenant object profiles safely
        try:
            cecab_tenant = TenantModel.objects.get(schema_name="cecab")
            teladoshi_tenant = TenantModel.objects.get(schema_name="teladoshi")
        except TenantModel.DoesNotExist as e:
            raise CommandError(f"Critical tenant workspace record missing: {str(e)}")

        self.stdout.write(self.style.WARNING("Reading source data from 'cecab' workspace..."))
        posts_to_copy = []

        # 2. Extract posts along with related image definitions out of the source schema scope
        with tenant_context(cecab_tenant):
            # Fetch all posts matching cecab tenant
            source_posts = Post.objects.all()
            
            for post in source_posts:
                # Capture post field records and keep track of individual child images
                images = list(post.post_images.all())
                posts_to_copy.append({
                    "post_instance": post,
                    "images_instances": images
                })

        if not posts_to_copy:
            self.stdout.write(self.style.SUCCESS("No post entries found in 'cecab' schema to duplicate."))
            return

        self.stdout.write(self.style.WARNING(f"Injecting {len(posts_to_copy)} items into 'teladoshi' schema..."))

        # 3. Enter target tenant environment and write database items cleanly
        with tenant_context(teladoshi_tenant):
            cloned_count = 0
            
            for data in posts_to_copy:
                old_post = data["post_instance"]
                
                # Check for an existing duplicate record in target layout to avoid duplicate rows
                if Post.objects.filter(slug=old_post.slug).exists():
                    self.stdout.write(f"Skipping slug '{old_post.slug}' (Already exists in teladoshi)")
                    continue

                # Generate a brand new primary key tracking reference block
                new_post = Post(
                    
                    title=old_post.title,
                    slug=old_post.slug,
                    picture=old_post.picture,
                    user=None, # Clear user mapping to prevent missing cross-tenant user record faults
                    text_file=old_post.text_file,
                    processed_text_file=old_post.processed_text_file,
                    active=old_post.active,
                    date=now(), # Assign current operational runtime date values
                    featured=old_post.featured,
                    is_a_service=old_post.is_a_service,
                    is_social_service=old_post.is_social_service,
                    is_to_front=old_post.is_to_front,
                    description=old_post.description,
                    text=old_post.text
                )
                new_post.save()
                cloned_count += 1

                # 4. Clone any individual child sub-images belonging to this parent article post asset block
                for old_img in data["images_instances"]:
                    PostImage.objects.create(
                        tenant=teladoshi_tenant,
                        post=new_post,
                        picture=old_img.picture
                    )

            self.stdout.write(self.style.SUCCESS(f"Successfully replicated {cloned_count} custom posts into 'teladoshi'!"))
