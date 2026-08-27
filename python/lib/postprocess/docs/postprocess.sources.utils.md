<!-- markdownlint-disable -->

<a href="../../../../python/lib/postprocess/src/postprocess/sources/utils.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

# <kbd>module</kbd> `postprocess.sources.utils`
Common utility and shared resources for the postprocess.sources subpackage.


## Table of Contents
- [`URLBuilder`](./postprocess.sources.utils.md#class-urlbuilder): A fluent builder for incrementally constructing well-formed web URLs.
	- [`URLBuilder.__init__`](./postprocess.sources.utils.md#constructor-urlbuilder__init__): Initialise a URLBuilder instance.
	- [`URLBuilder.resolve`](./postprocess.sources.utils.md#method-urlbuilderresolve): Resolve a path relative to the configured base URL.
	- [`URLBuilder.resolve_root`](./postprocess.sources.utils.md#method-urlbuilderresolve_root): Resolve a path relative to the configured URL origin, ignoring the base path.
	- [`URLBuilder.resolve_root_subdomain`](./postprocess.sources.utils.md#method-urlbuilderresolve_root_subdomain): Resolve a path relative to the specified subdomain, ignoring the configured base path.
	- [`URLBuilder.resolve_subdomain`](./postprocess.sources.utils.md#method-urlbuilderresolve_subdomain): Resolve a path relative to the specified subdomain and configured base path.
- [`advance_one_month`](./postprocess.sources.utils.md#function-advance_one_month): Advance a date or datetime by one calendar month, clamping to month end.
- [`generate_monthly_dates`](./postprocess.sources.utils.md#function-generate_monthly_dates): Generate monthly dates while they are less than or equal to end date, preserving the start date's day when possible.
- [`haversine_distance`](./postprocess.sources.utils.md#function-haversine_distance): Computes great-circle distance between two geographic coordinates.
- [`round_to_nearest_05`](./postprocess.sources.utils.md#function-round_to_nearest_05): Round value to nearest 0.05.



<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/sources/utils.py#L41"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `haversine_distance`

```python
haversine_distance(coord1, coord2, radius=6371.0)
```

Computes great-circle distance between two geographic coordinates.

Applies the Haversine formula to find the shortest spherical distance between
points. Converts inputs from decimal degrees to radians, validates bounds, 
and scales the angular separation by the specified planetary radius.


**Args:**

- <b>`coord1`</b> (tuple): Starting point as (latitude, longitude) coordinate pair in decimal degrees.
- <b>`coord2`</b> (tuple): Ending point as (latitude, longitude) coordinate pair in decimal degrees.
- <b>`radius`</b> (float, Optional): Sphere radius. Defaults to 6371.0 (Earth kilometers).


**Returns:**

- <b>`float`</b>: Great-circle distance in the same unit as radius.

TypeError: Coordinates is not a tuple or either coordinate is not an
    integer or float.
ValueError: Coordinates does not contain exactly two values or either
    coordinate is outside its valid range latitudes exceed [-90, 90] or
    longitudes exceed [-180, 180].



<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/sources/utils.py#L91"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `round_to_nearest_05`

```python
round_to_nearest_05(x)
```

Round value to nearest 0.05.



<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/sources/utils.py#L96"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `advance_one_month`

```python
advance_one_month(dt)
```

Advance a date or datetime by one calendar month, clamping to month end.



<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/sources/utils.py#L109"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `generate_monthly_dates`

```python
generate_monthly_dates(start_date, end_date, end_date_behaviour='exclude')
```

Generate monthly dates while they are less than or equal to end date,
preserving the start date's day when possible.


**Args:**

- <b>`start_date`</b> (date | datetime): The date or datetime to start generating
    from. Must be the same type as ``end_date``.
- <b>`end_date`</b> (date | datetime): The date or datetime to stop generating at.
    Must be the same type as ``start_date``.
- <b>`end_date_behaviour`</b> (str, optional): Controls how an ``end_date`` that does
    not fall on the monthly sequence is handled. Defaults to ``"exclude"``.
    - ``"exclude"``: Do not include ``end_date``.
    - ``"unique"``: Include ``end_date`` if its month is not already
    represented.
    - ``"append"``: Always include ``end_date``.


**Returns:**

- <b>`list[date | datetime]`</b>: Dates from ``start_date`` through ``end_date``,
    according to ``end_date_behaviour``.


**Raises:**

- <b>`ValueError`</b>: If ``end_date_behaviour`` is not one of ``"exclude"``,
    ``"unique"``, or ``"append"``.



<hr style="height: 6px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/sources/utils.py#L170"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>class</kbd> `URLBuilder`
A fluent builder for incrementally constructing well-formed web URLs.


<a href="../../../../python/lib/postprocess/src/postprocess/sources/utils.py#L173"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>constructor</kbd> `URLBuilder.__init__`

```python
URLBuilder(domain, subdomain='', path='', scheme='https')
```

Initialise a URLBuilder instance.


**Args:**

- <b>`domain`</b> (str): Target host or domain.
- <b>`subdomain`</b> (str, optional): Target subdomain.
    Defaults to None.
- <b>`path`</b> (str, optional): Base url path.
- <b>`scheme`</b> (str, optional): url scheme. i.e. `ftp` or `http`
    Defaults to `https`.



<hr style="height: 2px; border: none; background-color: currentColor;">

#### <kbd>property</kbd> URLBuilder.base_url

Return the full URL by joining base URL and base path.


<hr style="height: 2px; border: none; background-color: currentColor;">

#### <kbd>property</kbd> URLBuilder.netloc

Returns URL Net location.


<hr style="height: 2px; border: none; background-color: currentColor;">

#### <kbd>property</kbd> URLBuilder.origin

Return the origin (scheme + netloc).




<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/sources/utils.py#L205"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>method</kbd> `URLBuilder.resolve`

```python
resolve(path)
```

Resolve a path relative to the configured base URL.


<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/sources/utils.py#L209"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>method</kbd> `URLBuilder.resolve_root`

```python
resolve_root(path)
```

Resolve a path relative to the configured URL origin, ignoring the base path.


<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/sources/utils.py#L219"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>method</kbd> `URLBuilder.resolve_root_subdomain`

```python
resolve_root_subdomain(subdomain, path='')
```

Resolve a path relative to the specified subdomain, ignoring the configured base path.


<hr style="height: 2px; border: none; background-color: currentColor;">

<a href="../../../../python/lib/postprocess/src/postprocess/sources/utils.py#L213"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

### <kbd>method</kbd> `URLBuilder.resolve_subdomain`

```python
resolve_subdomain(subdomain, path='')
```

Resolve a path relative to the specified subdomain and configured base path.



