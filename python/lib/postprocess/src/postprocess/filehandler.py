"""This module assist with working with files/images for post processing.

Dependencies:
- numpy
"""

__all__ = ["MapValue", "FileInfo", "FileCorrelation"]

import os as _os
from dataclasses import dataclass as _dataclass  # Decorator
from datetime import datetime as _datetime
from typing import Any as _Any
from typing import Iterable as _Iterable  # Type hinting

import numpy as _np

# Package imports
from . import common as _common

# Pylint, disable for python 2 compatibility
# pylint: disable=consider-using-f-string


@_dataclass
class MapValue():
    """Represents a pair of matched/mapped value.

    Attributes:
        left (any): Value of left orientated matched/mapped pair.
        right (any): Value of right orientated matched/mapped pair.
    """

    def __init__(self, left, right):
        # type: (_Any, _Any) -> None
        """Generator for MatchInfo object.

        Args:
            left (any): Left value.
            right (any): Right value.

        Raises:
            TypeError: Left and Right not of same type.
        """
        if not isinstance(left, type(right)):
            raise TypeError("Left and Right not of same type")
        self._left = left
        """Private reference to 'left' value (`any`)."""
        self._right = right
        """Private reference to 'right' value (`any`)"""

    def __lt__(self, other):
        # type: (MapValue) -> bool
        return self._left < other._left and self._right < other._right

    def __le__(self, other):
        # type: (MapValue) -> bool
        return self._left <= other._left and self._right <= other._right

    def __eq__(self, other):
        # type: (MapValue) -> bool
        return (self._left == other._left) and (self._right == other._right)

    def __reversed__(self):
        temp = self._left
        self._left = self._right
        self._right = temp

    def __iter__(self):
        return iter((self._left, self._right))

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
        # type: (...) -> _Any
        """Getter for left match value (`any`, read-only)."""
        return self._left

    @property
    def right(self):
        # type: (...) -> _Any
        """Getter for right match value (`any`, read-only)."""
        return self._right

    def delta(self, reverse=False):
        # type: (bool) -> _Any
        """Calculates the difference between left and right value.

        Args:
            reverse (bool, optional): Subtract Left from Right.
                Defaults to False (Right from Left).

        Returns:
            any: Difference between matched/mapped value
        """
        if reverse:
            return _common.calculate_delta(self._right, self._left, abs_=False)
        return _common.calculate_delta(self._left, self._right, abs_=False)


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
        # type: (str, str, _datetime|None, _Any|None) -> None
        """Generator for FileInfo object.

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
class XRefRecord():
    """Cross Reference Record Object.

    Attributes:
        index (int): Index info of mapped object crossed reference value
            maps to.
        value (any): Value that is linked by cross referenced index.
    """

    def __init__(self, index, value):
        # type: (int, _Any) -> None
        """Generator for Cross Reference Record.

        Args:
            index (int): Index info of mapped object crossed reference value
                maps to.
            value (any): Value that is linked by cross referenced index.
        """
        self.index = index
        """Index info of mapped object crossed reference value maps to (`int`)."""
        self.value = value
        """Value that is linked by cross referenced index (`any`)."""

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
class FileMapXRef():
    """Cross Reference Object between files and mapped values."""

    def __init__(self, files):
        # type: (list) -> None
        self._files = files
        """Reference to list of files used for mapping (`list[str]`)."""
        self._xref = []  # List of Cross reference between files and mapped values
        """Reference to list of cross reference records of files (`list[XRefRecord[int, any]]`)."""

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
        # type: (...) -> list[XRefRecord]
        """List of undeciphered file index mapped value cross references
            (`list[XRefRecord[int,any]]`, read-only).
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
        # type: (...) -> list[_Any]
        """List of values that was used for cross referencing (`list[any]`, read-only).
        """
        return [value for _, value in self._xref]

    def append(self, index, data):
        # type: (int, _Any) -> None
        """Add a cross reference link mapping file to data.

        Args:
            index (int): Index of mapped file.
            data (any): Value of mapped data corresponding to file.

        Raises:
            IndexError: Index is out of range of parsed files.
        """
        if index >= len(self._files):
            raise IndexError
        self._xref.append(XRefRecord(index, data))

    def reset(self):
        # type: (...) -> None
        """Resets all mapped cross reference links."""
        del self._xref[:]


class FileCorrelation():
    """Represents an image correlation object.

    Attributes:
        mapped (list): Reference to list of file map records.
    """

    def __init__(self, path, format_=None):
        # type: (str, str|None) -> None
        """Generator for FileCorrelation object.

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
        """Reference to file extension filter for parsing (`str | tuple[str]`)"""
        self._files = []  # Reference to list of parsed files
        """Reference to list of parsed files (`list[str]`)"""
        self.mapped = FileMapXRef(self._files)  # Mapped File Cross Reference
        """Reference to list of crossed referenced files. (`FileMapXref`)"""

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
        # type: (...) -> list[_datetime]
        """List of datetime as matched from currently parsed filenames
            (`list[datetime, None]`, read-only)."""
        return [file.date_time for file in self._files]

    @property
    def matched(self):
        # type: (...) -> list[_Any]
        """List for values currently parsed files has matched on only (`list[any`], read-only)."""
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
        # type: (bool|None) -> list[_Any]
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
            format_ (str, optional): Format of filename containing datetime
                string like `time.strptime()` or `datetime.datetime.strptime()`.  
                Required if not declared during initialization. Defaults to None.  
                Format exclude file extension.
                i.e "2023-05-03_1030_filename.jpg" is "%Y-%m-%d_%H%M_filename".
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
        try:
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
        except Exception as err:
            raise err

    def map_to_filename_datetime(self, map_values, ref_date_time, data, dir_=0):
        # type: (_Iterable, _Iterable, _Iterable, int|None) -> None
        """Process mapping of values and date time to parsed date time in filenames.

        map_values <-> ref_date_time <-> data

        Args:
            map_values (Iterable): Values to map on.
            ref_date_time (Iterable): Common reference between values to be mapped
                and dataset. Allow correlation between map_values and data.
            data (Iterable): Data or Values to corellate map_values with.
            dir_ (int, optional): Direction preference for closest date_time.
                Future: 1, Past: -1, No preference: 0. Defaults to 0.
        """
        self.mapped.reset()
        files_date_times = self.date_times

        def get_index(f, dir_):
            if dir_ > 0:
                return _np.argmin(_np.ma.masked_less(f, 0))
            if dir_ < 0:
                return _np.argmax(_np.ma.masked_greater(f, 0))
            return _np.argmin(f)

        for value in map_values:
            # Get Index of reference data which is closest to map_value in question
            mapped_index = _np.argmin(
                _common.calculate_delta(
                    values=data,
                    ref=value,
                    abs_=True
                )
            )
            # Get Index of parsed files which is closest to datetime matching
            # map_value datetime.
            file_index = get_index(
                _common.calculate_delta(
                    values=files_date_times,
                    ref=ref_date_time[mapped_index],
                    abs_=(not dir_)
                ),
                dir_=dir_
            )
            value = MapValue(value, data[mapped_index])
            self.mapped.append(file_index, value)
            if self._files[file_index].value:
                if isinstance(self._files[file_index].value, list):
                    self._files[file_index].value.append(value)
                else:
                    old_value = self._files[file_index].value
                    self._files[file_index].value = [old_value, value]
            else:
                self._files[file_index].value = value

    def reset(self, reload=False):
        # type: (bool|None) -> None
        """Reset list of parsed files.

        Args:
            reload (bool, optional): Forces reparsing of files from directory.
                Defaults to False.

        Raises:
            RuntimeWarning: Unable to reload. Need to call parse_files() first.
        """
        if reload:
            try:
                self.parse_files()
            except RuntimeError as err:
                raise RuntimeWarning("Unable to reload files. "
                                     "Need to call parse_files() first.") from err
        else:
            del self._files[:]
            self.mapped.reset()
