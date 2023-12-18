"""This module assist with working with files/images for post processing."""

__all__ = ["FileDetail", "FileCorrelation"]

import os
import datetime
from dataclasses import dataclass
from typing import Iterable
import numpy

# Package imports
from . import common

@dataclass
class FileDetail():
    """Represents a file detail used in storing file/image correlation info."""
    def __init__(self, name, filepath, date_time=None, value=None):
        # type: (str, str, datetime.datetime, any) -> None
        """Generator for FileDetail object.

        Args:
            name (str): Name of file including extension.
            filepath (str): Full file path, includes filename and extension.
            date_time (datetime, optional): Timestamp. Defaults to None.
            value (any, optional): Value that file is matched on. Defaults to None.
        """
        self.name = name
        self.filepath = filepath
        self.date_time = date_time
        self.value = value

    def __lt__(self, other):
        return self.date_time < other.date_time

    def __le__(self, other):
        return self.date_time <= other.date_time

    def __eq__(self, other):
        return (self.name == other.name) and (self.date_time == other.date_time)

    def __str__(self):
        return self.name

    def __repr__(self):
        # pylint: disable-next=consider-using-f-string
        return "FileDetail(%s, %s, %s, %s)" % (
                repr(self.name),
                repr(self.filepath),
                repr(self.date_time),
                repr(self.value)
                )

    def reset(self):
        """Resets value associated with file."""
        self.value = None


class FileCorrelation():
    """Represents an image correlation object."""
    def __init__(self, format_, path):
        # type: (str, str) -> None
        """Generator for FileCorrelation object.

        Args:
            format_ (str): Format of filename containing datetime string like \
                `time.strptime()` and `datetime.datetime.strptime()`.
                Format exclude file extension. .i.e "2023-05-03_1030_filename.jpg" \
                is "%Y-%m-%d_%H%M_filename".
            path (str): Directory path containing files to parse.
        """
        self._format = format_
        self.path = path
        self._ext = None # Object to store file extension
        self.files = [] # Object to store matched files info

    @property
    def filenames(self):
        # type: (...) -> list[str]
        """Getter for list of filenames currently parsed files."""
        return [file.name for file in self.files]

    @property
    def filepaths(self):
        # type: (...) -> list[str]
        """Getter for list for the full file paths for currently parsed files."""
        return [file.filepath for file in self.files]

    @property
    def date_times(self):
        # type: (...) -> list[datetime.datetime]
        """Getter for list of datetime as matched from currently parsed filenames."""
        return [file.date_time for file in self.files]

    @property
    def values(self):
        # type: (...) -> list[any]
        """Getter for list for all values for parsed files.

        Will return same results as `matched` property if \
            `map_to_files_datetime(..., finish=True)` or \
            `FileCorrelation.finish()` has been called.
        """
        return [file.value for file in self.files]

    @property
    def matched(self):
        # type: (...) -> list[any]
        """Getter for list for values currently parsed files has matched on only."""
        return [ file for file in self.files if file.value]

    def parse_files(self, format_=None, ext=".jpg"):
        # type: (str|None, tuple|str) -> None
        """
        Parses date time string from filenames in directory for correlation.

        Args:
            format_ (str, optional): Format of filename containing datetime \
                string like `time.strptime()` and \
                `datetime.datetime.strptime()`if not declared during \
                initialization. Defaults to None.
                Format exclude file extension. \
                .i.e "2023-05-03_1030_filename.jpg" is "%Y-%m-%d_%H%M_filename".
            ext (tuple | str, optional): File extension to include \
                i.e (".jpg", ".png") or ".jpg" . Defaults to ".jpg".

        Raises:
            RuntimeError: No filename datetime string format provided during \
                initialization and calling this method.
            RuntimeError: No file extension provided during method call.
        """
        if format_ and self._format != format_:
            self._format = format_
        elif not self._format:
            raise RuntimeError("No filename datetime string format provided " \
                    "during method call or initialization.")

        if ext and self._ext != ext:
            self._ext = ext
        elif not self._ext:
            raise RuntimeError("No file extension provided during method call.")

        if self.files:
            del self.files[:]
        try:
            files = os.listdir(self.path)
            for file in files:
                filepath = os.path.join(self.path, file)
                # Make sure file is an image
                if not os.path.isfile(filepath):
                    continue
                name, file_ext = os.path.splitext(file)
                if file_ext not in self._ext:
                    continue
                file_datetime = datetime.datetime.strptime(name, self._format)
                self.files.append(FileDetail(file, filepath, file_datetime))
        except Exception as err:
            raise err

    def map_to_files_datetime(self, map_values, ref_date_time, data, finish=True):
        # type: (Iterable, Iterable, Iterable, bool) -> None
        """Process mapping of values and date time to parsed date time in filenames.

        map_values <-> ref_date_time <-> data

        Args:
            map_values (Iterable): Values to map on.
            ref_date_time (Iterable): Common reference between values to be mapped \
                and dataset. Allow correlation between map_values and data.
            data (Iterable): Data or Values to corellate map_values with.
            finish (bool, optional): Immediately clears list of files not \
                matched with anything. Defaults to True.
        """
        self.reset()
        files_date_times = self.date_times
        for value in map_values:
            mapped_index = numpy.argmin(
                    common.calculate_delta(
                            values = data,
                            ref = value,
                            abs_ = True)
            )
            file_index = numpy.argmin(
                    common.calculate_delta(
                            values = files_date_times,
                            ref = ref_date_time[mapped_index],
                            abs_ = True)
            )
            self.files[file_index].value = value
        if finish:
            self.finish()

    def reset(self, reload=False):
        # type: (bool) -> None
        """Reset list of files matched values.

        Args:
            reload (bool, optional): Forces reparsing of files from directory. \
                Defaults to False.

        Raises:
            RuntimeWarning: Unable to reload. Need to call parse_files() first.
        """
        if reload:
            try:
                self.parse_files()
            except RuntimeError as err:
                raise RuntimeWarning("Unable to reload files. " \
                        "Need to call parse_files() first.") from err
        else:
            for file in self.files:
                file.reset()

    def finish(self):
        """Clears list of files with no matches."""
        self.files = self.matched
