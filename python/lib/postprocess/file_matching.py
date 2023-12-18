"""Utilities for matching files to external data records.

This module provides classes for parsing file metadata, storing file
information, and correlating files with data values based on matching
criteria such as timestamps or nearest numerical values.

The module is intended for workflows where files (e.g. images, rasters,
or other time-indexed datasets) need to be associated with observations
or processed data records.

Dependencies:
- numpy
"""

__all__ = ["MatchPair", "FileInfo", "FileCorrelator"]

import os as _os
import warnings as _warnings
from dataclasses import dataclass as _dataclass  # Decorator
from datetime import datetime as _datetime
from typing import TYPE_CHECKING

import numpy as _np

# Package imports
from . import transformation as _transformation

if TYPE_CHECKING:
    from typing import (
        Any,
        Iterable,
        Iterator,
    )

# Pylint, disable for python 2 compatibility
# pylint: disable=consider-using-f-string


@_dataclass
class MatchPair():
    """Represents a pair of matched/mapped value.

    Attributes:
        left (Any): The left-side value of the matched pair.
        right (Any): The right-side value of the matched pair.
    """

    def __init__(self, left, right):
        # type: (Any, Any) -> None
        """Initialize a MatchPair object.

        Args:
            left (any): Left value.
            right (any): Right value.
        """
        self._left = left
        """Private reference to 'left' value (`any`)."""
        self._right = right
        """Private reference to 'right' value (`any`)."""

    def __lt__(self, other):
        # type: (MatchPair) -> bool
        return self._left < other._left and self._right < other._right

    def __le__(self, other):
        # type: (MatchPair) -> bool
        return self._left <= other._left and self._right <= other._right

    def __eq__(self, other):
        # type: (MatchPair) -> bool
        return (self._left == other._left) and (self._right == other._right)

    def __iter__(self):
        # type: (...) -> Iterator
        return iter((self._left, self._right))

    def __reversed__(self):
        # type: (...) -> Iterator
        return iter((self._right, self._left))

    def __str__(self):
        return "{} <-> {}".format(self._left, self._right)

    def __repr__(self):
        return ("%s(%s, %s)" % (
            __class__.__name__,
            repr(self._left),
            repr(self._right)
        ))

    @property
    def left(self):
        # type: (...) -> Any
        """Getter for left match value (`any`, read-only)."""
        return self._left

    @property
    def right(self):
        # type: (...) -> Any
        """Getter for right match value (`any`, read-only)."""
        return self._right

    def swap(self):
        # type: (...) -> None
        """Performs in place left and right value swap."""
        self._left, self._right = self._right, self._left

    def delta(self, inverted=False):
        # type: (bool) -> Any
        """Calculates the mathematical difference (delta) between the left and right values.

        By default, calculates the difference moving left-to-right (Right minus Left).

        Args:
            inverted (bool, optional): If True, calculates Left minus Right 
                instead. Defaults to False.

        Returns:
            Any: Difference between the matched/mapped values.
        """
        if inverted:
            # Left minus Right
            return _transformation.calculate_delta(self._left, self._right, abs_=False)

        # Right minus Left
        return _transformation.calculate_delta(self._right, self._left, abs_=False)


@_dataclass
class FileInfo():
    """Represents a file detail used in storing file/image correlation info.

    Attributes:
        name (str): Name of file including extension.
        filepath (str): Full file path, includes filename and extension.
        date_time (datetime): Parsed timestamp of corresponding file.
        value (any): Value reference for any matching data corresponding with file.
    """

    def __init__(self, name, filepath, date_time=None, value=None):
        # type: (str, str, _datetime|None, Any|None) -> None
        """Initialize a FileInfo object.

        Args:
            name (str): Name of file including extension.
            filepath (str): Full file path, includes filename and extension.
            date_time (datetime, optional): Timestamp. Defaults to None.
            value (any, optional): Value that file is matched on. Defaults to None.
        """
        self.name = name
        """Filename including extension (`str`)."""
        self.filepath = _os.path.normpath(filepath)
        """Full file path, including filename and extension (`str`)."""
        self.date_time = date_time
        """Date time as parsed from filename, or None (`datetime | None`)."""
        self.value = value
        """Value reference for any matching data corresponding with file (`any`)."""

    def __lt__(self, other):
        # type: (FileInfo) -> bool
        return self.date_time < other.date_time

    def __le__(self, other):
        # type: (FileInfo) -> bool
        return self.date_time <= other.date_time

    def __eq__(self, other):
        # type: (FileInfo) -> bool
        return (self.name == other.name) and (self.date_time == other.date_time)

    def __iter__(self):
        return iter((self.name,
                     self.filepath,
                     self.date_time,
                     self.value))

    def __str__(self):
        return "{} {} {} {}".format(
            self.name,
            self.filepath,
            self.date_time,
            self.value
        )

    def __repr__(self):
        return "%s(%s, %s, %s, %s)" % (
            __class__.__name__,
            repr(self.name),
            repr(self.filepath),
            repr(self.date_time),
            repr(self.value)
        )

    def reset(self):
        """Resets value associated with file."""
        self.value = None


@_dataclass
class MappingRecord():
    """Represents a single cross-reference linking a file index to a matched value.

    Attributes:
        index (int): Index of the mapped file.
        value (any): Value linked to the file index.
    """

    def __init__(self, index, value):
        # type: (int, Any) -> None
        """Initialize a MappingRecord object.

        Args:
            index (int): Index of the mapped file.
            value (any): Value linked by the index.
        """
        self.index = index
        """Index of the mapped file (`int`)."""
        self.value = value
        """Value linked to the file index (`Any`)."""

    def __iter__(self):
        return iter((self.index, self.value))

    def __str__(self):
        return "({}, {})".format(
            self.index,
            self.value
        )

    def __repr__(self):
        return "%s(%s, %s)" % (
            __class__.__name__,
            repr(self.index),
            repr(self.value)
        )


@_dataclass
class FileMapping():
    """Manages cross-reference links between parsed files and matched data values."""

    def __init__(self, files):
        # type: (list) -> None
        """Initialize a FileMapping object."""
        self._files = files
        """Reference to list of parsed files (`list[FileInfo]`)."""
        self._xref = []  # List of Cross reference between files and mapped values
        """Reference to a list of cross reference records of files.
        See :class:`MappingRecord`.
        """

    def __iter__(self):
        return iter(self.files)

    def __getitem__(self, key):
        # type: (...) -> FileInfo
        index, value = self._xref[key]
        return FileInfo(self._files[index].name,
                        self._files[index].filepath,
                        self._files[index].date_time,
                        value)

    def __len__(self):
        return len(self._xref)

    @property
    def xref(self):
        # type: (...) -> list[MappingRecord]
        """List of undeciphered file index mapped value cross references
            (`list[MappingRecord[int, any]]`, read-only).
        """
        return self._xref

    @property
    def files(self):
        # type: (...) -> list[FileInfo]
        """List of deciphered cross referenced files with mapped values
            (`list[FileInfo]`, read-only).
        """
        return [
            FileInfo(self._files[index].name,
                     self._files[index].filepath,
                     self._files[index].date_time,
                     value)
            for index, value in self._xref
        ]

    @property
    def filenames(self):
        # type: (...) -> list[str]
        """List of deciphered cross referenced file names (`list[str]`, read-only).
        """
        return [self._files[index].name for index, _ in self._xref]

    @property
    def filepaths(self):
        # type: (...) -> list[str]
        """List of deciphered cross referenced file paths (`list[str]`, read-only).
        """
        return [self._files[index].filepath for index, _ in self._xref]

    @property
    def indexes(self):
        # type: (...) -> list[int]
        """List of undeciphered cross referenced file index (`list[int]`, read-only).
        """
        return [index for index, _ in self._xref]

    @property
    def values(self):
        # type: (...) -> list[Any]
        """List of values that was used for cross referencing (`list[Any]`, read-only).
        """
        return [value for _, value in self._xref]

    def append(self, index, data):
        # type: (int, Any) -> None
        """Add a cross reference link mapping file to data.

        Args:
            index (int): Index of mapped file.
            data (any): Value of mapped data corresponding to file.

        Raises:
            IndexError: Index is out of range of parsed files.
        """
        if index >= len(self._files):
            raise IndexError
        self._xref.append(MappingRecord(index, data))

    def reset(self):
        # type: (...) -> None
        """Resets all mapped cross reference links."""
        del self._xref[:]


class FileCorrelator():
    """Represents a file correlation and metadata parsing manager.

    Attributes:
        mapped (list): Reference to list of file map records.
    """

    def __init__(self, path, format_=None):
        # type: (str, str|None) -> None
        """Initialize a FileCorrelator object.

        Args:
            path (str): Directory path containing files to parse.
            format_ (str, optional): Format of filename containing datetime string like
                `time.strptime()` and `datetime.datetime.strptime()`.
                Format exclude file extension. .i.e "2023-05-03_1030_filename.jpg"
                is "%Y-%m-%d_%H%M_filename".  Defaults to None.

        Raises:
            FileNotFoundError: Directory path does not exist.
        """
        self.path = path  # Use property
        self._format = format_
        """Format for filename parsing (`str`)."""
        self._ext = None  # Reference file extension included for parsing
        """Reference to file extension filter for parsing (`str | tuple[str]`)."""
        self._files = []  # Reference to list of parsed files
        """Reference to list of parsed files (`list[FileInfo]`)."""
        self.mapped = FileMapping(self._files)  # Mapped File Cross Reference
        """Reference to list of crossed referenced files. See :class:`FileMapping`"""

    @property
    def path(self):
        # type: (...) -> str
        """Reference to path of directory used for file parsing (`str`).

        Raises:
            FileNotFoundError: Directory path does not exist.
        """
        return self._path

    @path.setter
    def path(self, value):
        # type: (str) -> None
        if _os.path.isdir(value):
            self._path = _os.path.normpath(value)
        else:
            raise FileNotFoundError("Directory does not exist!")

    @property
    def files(self):
        # type: (...) -> list[FileInfo]
        """List of currently parsed files (`list[FileInfo]`, read-only)."""
        return self._files

    @property
    def filenames(self):
        # type: (...) -> list[str]
        """List of currently parsed filenames (`list[str]`, read-only)."""
        return [file.name for file in self._files]

    @property
    def filepaths(self):
        # type: (...) -> list[str]
        """List of currently parsed full file paths (`list[str]`, read-only)."""
        return [file.filepath for file in self._files]

    @property
    def date_times(self):
        # type: (...) -> list[_datetime | None]
        """List of datetime as matched from currently parsed filenames
            (`list[datetime | None]`, read-only)."""
        return [file.date_time for file in self._files]

    @property
    def matched(self):
        # type: (...) -> list[FileInfo]
        """List of parsed files that currently have matched values (`list[FileInfo]`, read-only)."""
        return [file for file in self._files if file.value]

    # @property
    # def values_mapped(self):
    #     # type: (...) -> list[any]
    #     """Getter for list of mapped files to values."""
    #     result = []
    #     for file in self.matched:
    #         try:
    #             for _ in range(len(file.value)):
    #                 result.append(file)
    #         except TypeError:
    #             result.append(file)
    #     return result

    def values(self, flat=False):
        # type: (bool|None) -> list[Any]
        """Getter for list for all values for parsed files.

        Args:
            flat (bool, optional): Flatten output. Defaults to False.

        Returns:
            list: List of values matched to file.
        """
        if flat:
            return [value
                    for file in self._files
                    for value in (file.value if isinstance(file.value, list)
                                  else [file.value])]
        return [file.value for file in self._files]

    def parse_files(self, format_=None, ext=".jpg"):
        # type: (str|None, str|tuple|None) -> None
        """Parses date time string from filenames in directory for correlation.

        Args:
            format_ (str, optional): Format of filename containing datetime string like
                ``time.strptime()`` or ``datetime.datetime.strptime()``.  
                Required if not declared during initialization. Defaults to None.  
                Format excludes file extension.
                e.g., ``"2023-05-03_1030_filename.jpg"`` uses ``"%Y-%m-%d_%H%M_filename"``.
            ext (tuple | str, optional): File extension to include
                i.e (".jpg", ".png") or ".jpg" . Defaults to ".jpg".

        Raises:
            RuntimeError: No filename datetime string format provided during
                initialization and calling this method.
            RuntimeError: No file extension provided during method call.
        """
        if format_ and self._format != format_:
            self._format = format_
        elif not self._format:
            raise RuntimeError("No filename datetime string format provided "
                               "during method call or initialization.")

        if ext and self._ext != ext:
            self._ext = ext
        elif not self._ext:
            raise RuntimeError(
                "No file extension provided during method call.")

        self.reset()

        files = _os.listdir(self.path)
        for file in files:
            filepath = _os.path.join(self.path, file)
            # Make sure file is an image
            if not _os.path.isfile(filepath):
                continue

            name, file_ext = _os.path.splitext(file)
            if file_ext not in self._ext:
                continue

            file_datetime = _datetime.strptime(name, self._format)
            self._files.append(FileInfo(file, filepath, file_datetime))

    def map_by_datetime(self, map_values, ref_date_time, data, direction=0):
        # type: (Iterable, Iterable, Iterable, int|None) -> None
        """Correlate external values and reference timestamps with parsed file timestamps.

        Links datasets through a shared timestamp chain:
        ``map_values`` <-> ``ref_date_time`` <-> ``Parsed File Timestamps``

        Args:
            map_values (Iterable): External values to map (e.g., sensor readings).
            ref_date_time (Iterable): Timestamps corresponding to ``map_values`` 
                used to bridge the dataset to the files.
            data (Iterable): Data values to correlate with ``map_values``.
            direction (int, optional): Search direction preference for closest datetime.
                Future: 1, Past: -1, No preference: 0. Defaults to 0.
        """
        self.mapped.reset()
        files_date_times = self.date_times

        def get_index(f, direction):
            if direction > 0:
                return _np.argmin(_np.ma.masked_less(f, 0))
            if direction < 0:
                return _np.argmax(_np.ma.masked_greater(f, 0))
            return _np.argmin(f)

        for value in map_values:
            # Get Index of reference data which is closest to map_value in question
            mapped_index = _np.argmin(
                _transformation.calculate_delta(
                    values=data,
                    ref=value,
                    abs_=True
                )
            )
            # Get Index of parsed files which is closest to datetime matching
            # map_value datetime.
            file_index = get_index(
                _transformation.calculate_delta(
                    values=files_date_times,
                    ref=ref_date_time[mapped_index],
                    abs_=(not direction)
                ),
                direction=direction
            )
            mapped_pair = MatchPair(value, data[mapped_index])
            self.mapped.append(file_index, mapped_pair)
            if self._files[file_index].value:
                if isinstance(self._files[file_index].value, list):
                    self._files[file_index].value.append(mapped_pair)
                else:
                    old_value = self._files[file_index].value
                    self._files[file_index].value = [old_value, mapped_pair]
            else:
                self._files[file_index].value = mapped_pair

    def reset(self, reload=False):
        # type: (bool|None) -> None
        """Reset list of parsed files.

        Args:
            reload (bool, optional): Forces reparsing of files from directory.
                Defaults to False.

        Warns:
            UserWarning: Unable to reload files. Need to call :meth:`parse_files` first.
        """
        if reload:
            try:
                self.parse_files()
            except RuntimeError:
                _warnings.warn(
                    "Unable to reload files. Need to call `parse_files()` first.",
                    UserWarning
                )
        else:
            del self._files[:]
            self.mapped.reset()
