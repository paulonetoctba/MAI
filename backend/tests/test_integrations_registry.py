import importlib
import pytest
import sys
import os

# Ensure project root is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_integration_modules_import():
    """
    Regression Test: Ensure all integration modules can be imported.
    This verifies that the massive refactoring didn't break module resolution
    or introduce syntax errors in the new files.
    """
    modules_to_test = [
        "app.integrations.ads.social_ads",
        "app.integrations.ads.retail_media",
        "app.integrations.ads.programmatic",
        "app.integrations.ads.google_ads",
        "app.integrations.ads.meta_ads",
        "app.integrations.ads.tiktok_ads",
        "app.integrations.analytics.clients",
        "app.integrations.crm.clients",
        "app.integrations.communication.clients",
        "app.integrations.ecommerce.clients",
        "app.integrations.ecommerce.latam_clients",
        "app.integrations.ecommerce.headless_clients",
    ]

    for module_name in modules_to_test:
        try:
            if module_name in sys.modules:
                importlib.reload(sys.modules[module_name])
            else:
                importlib.import_module(module_name)
        except Exception as e:
            pytest.fail(f"Failed to import {module_name}: {str(e)}")

def test_config_structure():
    """
    Regression Test: Ensure Config has expected fields.
    """
    from app.config import settings
    
    # Check a few random new fields from different categories
    assert hasattr(settings, "NUVEMSHOP_ACCESS_TOKEN"), "Missing Latam field"
    assert hasattr(settings, "COMMERCETOOLS_CLIENT_ID"), "Missing Headless field"
    assert hasattr(settings, "LINKEDIN_CLIENT_ID"), "Missing Social Ads field"
    assert hasattr(settings, "SALESFORCE_MC_CLIENT_ID"), "Missing CRM field"
