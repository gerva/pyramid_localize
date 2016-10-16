"""Test catalogue related code."""

from pyramid_localize.views.catalogue import CatalogueView

try:
    from mock import Mock
except ImportError:
    from unittest.mock import Mock


def test_translation_file(monkeypatch):

    def mockreturn(request):
        return ''

    monkeypatch.setattr('pyramid_localize.views.catalogue.destination_path',
                        mockreturn)
    catalogue = CatalogueView(request='')
    catalogue._translation_file(language='', domain='', extension='po')


def test_translation_template_path(monkeypatch):

    def mockreturn(spec):
        return (None, __file__)

    monkeypatch.setattr('pyramid_localize.views.catalogue.resolve_asset_spec',
                        mockreturn)
    catalogue = CatalogueView(request='')
    path = catalogue._translation_template_path('')
    assert __file__ in path

    def mockreturn(spec):
        return ('pytest', __file__)

    monkeypatch.setattr('pyramid_localize.views.catalogue.resolve_asset_spec',
                        mockreturn)
    path = catalogue._translation_template_path('')
    assert __file__ in path


def test_catalogue(monkeypatch):
    request = Mock()
    request.registry = {'config': Mock()}
    path = '/some/path/to/translations'
    mock_configuration = {
        'localize.translation.destination': path,
        'localize.translation.sources': {'a': 'a', 'b': 'b'},
        'localize.locales.available': ['language1', 'language2']}
    request.registry['config'].configure_mock(**mock_configuration)

    def mockreturn(*args, **kwargs):
        return 0

    def mockHTTPFound(*args, **kwargs):
        return

    monkeypatch.setattr('subprocess.call', mockreturn)
    monkeypatch.setattr('pyramid_localize.views.catalogue.HTTPFound', mockHTTPFound)
    catalogue = CatalogueView(request=request)
    translations = catalogue.index()
    catalogue.update_catalogue()
    catalogue.compile_catalogue()


