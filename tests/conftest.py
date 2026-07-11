import re
import pytest

AD_PATTERN = re.compile(r"(doubleclick|googlesyndication|google_vignette|adservice\.google)")


@pytest.fixture
def page(context):
    page = context.new_page()
    page.route(AD_PATTERN, lambda route: route.abort())
    yield page
    page.close()
