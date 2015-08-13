from datascience import *
from unittest.mock import MagicMock, patch
import pytest
import copy


@pytest.fixture(scope='function')
def states():
    """Read a map of US states."""
    return Map.read_geojson('tests/us-states.json')


############
# Overview #
############


def test_draw_map(states):
    """ Tests that draw_map returns HTML """
    assert isinstance(states.show(), HTML)


def test_setup_map():
    """ Tests that passing kwargs doesn't error. """
    kwargs = {
        'tiles': 'Stamen Toner',
        'zoom_start': 17,
        'width': 960,
        'height': 500,
        'features': [],
    }
    map_html = Map(**kwargs).show()
    assert isinstance(map_html, HTML)


def test_map_marker():
    """ Tests that a Map can contain a Marker. """
    marker = Marker(51.514, -0.132)
    map_html = Map([marker]).show()
    assert isinstance(map_html, HTML)


def test_map_region(states):
    """ Tests that a Map can contain a Region. """
    region = states['CA']
    map_html = Map([region]).show()
    assert isinstance(map_html, HTML)


##########
# Marker #
##########


def test_marker_html():
    """ Tests that a Marker can be rendered. """
    map_html = Marker(51.514, -0.132).show()
    assert isinstance(map_html, HTML)


def test_marker_map():
    """ Tests that Marker.map generates a map """
    lats = [51, 52, 53]
    lons = [-1, -2, -3]
    labels = ['A', 'B', 'C']
    map_html = Marker.map(lats, lons).show()
    assert isinstance(map_html, HTML)
    map_html = Marker.map(lats, lons, labels).show()
    assert isinstance(map_html, HTML)


#############
# MapRegion #
#############


def test_region_html(states):
    map_html = states['CA'].show()
    assert isinstance(map_html, HTML)


def test_geojson(states):
    """ Tests that geojson returns the correct data """
    data = json.load(open('tests/us-states.json', 'r'))
    geo = states.geojson()
    assert data == geo, '{}\n{}'.format(data, geo)


###############
# TEST BOUNDS #
###############


def test_bounds():
    """ Tests that generated bounds are correct """
    points = [Marker(0, 0), Marker(-89.9, 180), Marker(90, -180)]
    bounds = Map(points)._autobounds()
    assert bounds['max_lat'] == 90
    assert bounds['min_lat'] == -89.9
    assert bounds['max_lon'] == 180
    assert bounds['min_lon'] == -180


def test_bounds_limits():
    """ Tests that too-large lats and lons are truncated to real bounds. """

    points = [Marker(0, 0), Marker(-190, 280), Marker(190, -280)]
    bounds = Map(points)._autobounds()
    assert bounds['max_lat'] == 90
    assert bounds['min_lat'] == -90
    assert bounds['max_lon'] == 180
    assert bounds['min_lon'] == -180
