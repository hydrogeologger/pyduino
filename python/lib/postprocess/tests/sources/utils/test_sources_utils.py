"""Tests for utility functions used by meteorological data sources."""

from datetime import (
    date,
    datetime,
)

import pytest

from postprocess.sources.utils import (
    URLBuilder,
    advance_one_month,
    generate_monthly_dates,
    round_to_nearest_05,
)


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (0.00, 0.00),
        (0.01, 0.00),
        (0.02, 0.00),
        (0.03, 0.05),
        (0.05, 0.05),
        (0.06, 0.05),
        (0.07, 0.05),
        (0.08, 0.10),
        (1.00, 1.00),
        (1.02, 1.00),
        (1.03, 1.05),
        (1.07, 1.05),
        (1.08, 1.10),
        (-0.02, 0.00),
        (-0.03, -0.05),
        (-1.02, -1.00),
        (-1.03, -1.05),
    ],
)
def test_rounds_to_nearest_05(value, expected):
    """Round values to the nearest 0.05."""
    assert round_to_nearest_05(value) == expected


@pytest.mark.parametrize(
    "dt, expected",
    [
        (
            date(2024, 1, 15),
            date(2024, 2, 15),
        ),
        (
            date(2024, 11, 15),
            date(2024, 12, 15),
        ),
        (
            date(2024, 12, 15),
            date(2025, 1, 15),
        ),
        (
            date(2024, 1, 31),
            date(2024, 2, 29),
        ),
        (
            date(2023, 1, 31),
            date(2023, 2, 28),
        ),
        (
            date(2024, 3, 31),
            date(2024, 4, 30),
        ),
        (
            datetime(2024, 1, 31, 14, 30, 45),
            datetime(2024, 2, 29, 14, 30, 45),
        ),
    ],
)
def test_advance_one_month(dt, expected):
    """Advance a date or datetime by one calendar month."""
    assert advance_one_month(dt) == expected


def test_generate_monthly_dates():
    """Generate monthly dates while preserving the start date's day."""
    assert generate_monthly_dates(
        date(2026, 1, 31),
        date(2026, 5, 31),
    ) == [
        date(2026, 1, 31),
        date(2026, 2, 28),
        date(2026, 3, 31),
        date(2026, 4, 30),
        date(2026, 5, 31),
    ]


@pytest.mark.parametrize(
    "behaviour, end_date, expected",
    [
        (
            "exclude",
            date(2026, 5, 2),
            [date(2026, 4, 30)],
        ),
        (
            "unique_month",
            date(2026, 5, 20),
            [date(2026, 5, 20)],
        ),
        (
            "append",
            date(2026, 5, 20),
            [date(2026, 4, 30), date(2026, 5, 20)],
        ),
    ],
)
def test_generate_monthly_dates_end_date_behaviour(
    behaviour, end_date, expected
):
    """Handle end_date according to the specified behaviour."""
    dates = generate_monthly_dates(
        date(2026, 1, 31),
        end_date,
        behaviour,
    )

    assert dates[-len(expected):] == expected


def test_generate_monthly_dates_invalid_behaviour():
    """Raise ValueError for an invalid end_date_behaviour."""
    with pytest.raises(ValueError):
        generate_monthly_dates(
            date(2026, 1, 15),
            date(2026, 5, 15),
            "invalid",
        )


class TestURLBuilder:
    """Tests for URLBuilder."""

    @pytest.mark.parametrize(
        "domain, subdomain, scheme, expected",
        [
            (
                "example.com",
                "api",
                "https",
                "api.example.com",
            ),
            (
                "/example.com/",
                ".api.",
                "HTTPS://",
                "api.example.com",
            ),
            (
                "example.com",
                "",
                "http",
                "example.com",
            ),
        ],
    )
    def test_netloc(self, domain, subdomain, scheme, expected):
        """Return the normalised netloc."""
        builder = URLBuilder(
            domain=domain,
            subdomain=subdomain,
            scheme=scheme,
        )

        assert builder.netloc == expected

    @pytest.mark.parametrize(
        "scheme, subdomain, expected",
        [
            (
                "https",
                "api",
                "https://api.example.com",
            ),
            (
                "HTTP://",
                "api",
                "http://api.example.com",
            ),
            (
                "ftp:",
                "",
                "ftp://example.com",
            ),
        ],
    )
    def test_origin(self, scheme, subdomain, expected):
        """Return the scheme and netloc."""
        builder = URLBuilder(
            domain="example.com",
            subdomain=subdomain,
            scheme=scheme,
        )

        assert builder.origin == expected

    @pytest.mark.parametrize(
        "path, expected",
        [
            (
                "",
                "https://api.example.com",
            ),
            (
                "v1/data",
                "https://api.example.com/v1/data",
            ),
            (
                "/v1/data",
                "https://api.example.com/v1/data",
            ),
        ],
    )
    def test_base_url(self, path, expected):
        """Return the origin joined with the configured base path."""
        builder = URLBuilder(
            domain="example.com",
            subdomain="api",
            path=path,
        )

        assert builder.base_url == expected

    @pytest.mark.parametrize(
        "path",
        [
            "stations",
            "/stations",
        ],
    )
    def test_resolve(self, path):
        """Resolve a path relative to the configured base URL."""
        builder = URLBuilder(
            domain="example.com",
            subdomain="api",
            path="v1/data",
        )

        assert (
            builder.resolve(path)
            == "https://api.example.com/v1/data/stations"
        )

    @pytest.mark.parametrize(
        "path",
        [
            "stations",
            "/stations",
        ],
    )
    def test_resolve_root(self, path):
        """Resolve a path relative to the configured origin."""
        builder = URLBuilder(
            domain="example.com",
            subdomain="api",
            path="v1/data",
        )

        assert (
            builder.resolve_root(path)
            == "https://api.example.com/stations"
        )

    @pytest.mark.parametrize(
        "method, subdomain, path, expected",
        [
            (
                "resolve_subdomain",
                "cdn",
                "stations",
                "https://cdn.example.com/v1/data/stations",
            ),
            (
                "resolve_subdomain",
                "cdn",
                "/stations",
                "https://cdn.example.com/v1/data/stations",
            ),
            (
                "resolve_root_subdomain",
                "cdn",
                "stations",
                "https://cdn.example.com/stations",
            ),
            (
                "resolve_root_subdomain",
                "cdn",
                "/stations",
                "https://cdn.example.com/stations",
            ),
        ],
    )
    def test_resolve_subdomain(
        self,
        method,
        subdomain,
        path,
        expected,
    ):
        """Resolve paths using a specified subdomain."""
        builder = URLBuilder(
            domain="example.com",
            subdomain="api",
            path="v1/data",
        )

        assert getattr(builder, method)(subdomain, path) == expected

    def test_resolve_subdomain_does_not_modify_builder(self):
        """Resolve using a subdomain without modifying the builder."""
        builder = URLBuilder(
            domain="example.com",
            subdomain="api",
            path="v1/data",
        )

        builder.resolve_subdomain("cdn", "stations")

        assert builder.netloc == "api.example.com"
        assert builder.base_url == "https://api.example.com/v1/data"
