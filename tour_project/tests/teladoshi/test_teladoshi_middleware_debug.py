import pytest
from django.db import connection
from django_tenants.utils import get_tenant_domain_model, get_tenant_model


@pytest.mark.django_db
def test_domain_lookup(client, db):
    """Test that the domain can be found in the middleware"""
    TenantModel = get_tenant_model()
    DomainModel = get_tenant_domain_model()

    # Set to public schema to check domains
    connection.set_schema_to_public()

    # Check what domains exist
    all_domains = list(
        DomainModel.objects.all().values_list("domain", "tenant__schema_name")
    )
    print(f"\n=== BEFORE TEST: All domains: {all_domains}")

    # Get or create test tenant
    test_tenant, created = TenantModel.objects.get_or_create(
        schema_name="test", defaults={"schema_name": "test"}
    )

    # Create domain
    domain, created = DomainModel.objects.get_or_create(
        domain="testserver", tenant=test_tenant, defaults={"is_primary": True}
    )

    all_domains = list(
        DomainModel.objects.all().values_list("domain", "tenant__schema_name")
    )
    print(f"=== AFTER CREATE: All domains: {all_domains}")

    # Try to find the domain
    try:
        found_domain = DomainModel.objects.get(domain="testserver")
        print(
            f"=== FOUND: domain='{found_domain.domain}' \
              for tenant='{found_domain.tenant.schema_name}'"
        )
    except DomainModel.DoesNotExist:
        print("=== NOT FOUND: domain='testserver'")

    # Now try a request
    connection.set_tenant(test_tenant)
    resp = client.get("/api/expeditions/")
    print(
        f"=== RESPONSE: status_code={resp.status_code}, \
          url={client.get('/api/expeditions/').request.get('PATH_INFO', 'N/A')}"
    )
