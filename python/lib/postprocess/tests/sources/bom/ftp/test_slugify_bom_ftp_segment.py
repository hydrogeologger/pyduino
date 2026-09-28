"""Tests for :func:`slugify_bom_ftp_segment`."""

import pytest

from postprocess.sources.bom.ftp import slugify_bom_ftp_segment


@pytest.mark.parametrize(
    "text_segment, expected",
    [
        ("ADELAIDE (WEST TERRACE / NGAYIRDAPIRA)", "adelaide_(west_terrace___ngayirdapira)"),
        ("SALMON GUMS RES.STN.", "salmon_gums_resstn"),
        ("Holsworthy - Defence", "holsworthy_-_defence"),
        ("TAS ", "tas_"),
        ("Brisbane Airport", "brisbane_airport"),
        ("QUEENSLAND", "queensland"),
        ("A-B", "a-b"),
        ("A (B)", "a_(b)"),
        ("A  B", "a__b"),
        ("", ""),
    ],
)
def test_slugifies_bom_ftp_segment(text_segment, expected):
    """Test conversion of BOM text into an FTP-compatible slug."""
    assert slugify_bom_ftp_segment(text_segment) == expected
