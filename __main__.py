#!/usr/bin/env python3
# -*- coding: UTF_8 -*-

import argparse
import csv
import json
import os
import re
import sys


class TypeDescriptor:
    """
    Abstract type descriptor used to parse data
    """

    def parse(self, value):
        """
        Parse the value into the right type as the type descriptor

        :param value: The string value
        :type value: str
        :return: The value parsed
        """
        NotImplementedError()


class IntegerDescriptor(TypeDescriptor):
    """
    Integer descriptor used to parse data as int type
    """

    def parse(self, value):
        return int(value)


class FloatDescriptor(TypeDescriptor):
    """
    Float descriptor used to parse data as float type
    """

    def parse(self, value):
        return float(value)


class StringDescriptor(TypeDescriptor):
    """
    String descriptor used to parse data as str type
    """

    def parse(self, value):
        return str(value).strip(" ")


class BooleanDescriptor(TypeDescriptor):
    """
    Boolean descriptor used to parse data as bool type
    """

    def parse(self, value):
        try:
            value = int(value.strip())
        except ValueError:
            raise ValueError('The value for boolean must be an integer where 0 means False and any others True')
        return bool(value)


class ArrayDescriptor(TypeDescriptor):
    """
    Array descriptor used to parse data as list type of given type
    """

    def __init__(self, type):
        """
        :param type: the type descriptor contained in the list
        :type type: TypeDescriptor
        """
        self.type = type

    def parse(self, value):
        values = value.split(",")

        # the list to return after values are parsed
        r_list = []

        # foreach piece parse into the right value
        for piece in values:
            if piece:
                r_list.append(self.type.parse(piece))

        return r_list


class CSVHeaderColumn:

    def __init__(self, name, type):
        self.name = name.lower()
        self.type = type

    @staticmethod
    def parse_type(type):
        """
        Parse the column type in a a type descriptor

        :param type: The type to decode
        :type type: str
        :return: the type descriptor
        :rtype: TypeDescriptor
        """
        if "." in type:
            pieces = type.split(".", 1)
            if pieces[0] == "a":
                return ArrayDescriptor(
                    CSVHeaderColumn.parse_type(pieces[1])
                )
        elif type == "i":
            return IntegerDescriptor()
        elif type == "f":
            return FloatDescriptor()
        elif type == "s":
            return StringDescriptor()
        elif type == "b":
            return BooleanDescriptor()

        # if not returned before the value is bad
        raise ValueError("The type \"{}\" is not accepted".format(type))


class Translator:

    def __init__(self, in_file, out_file, delimiter, quote, smart):
        self.in_file = in_file
        self.out_file = out_file

        self.delimiter = ";" if delimiter is None else delimiter
        self.quote = "\"" if quote is None else quote

        self.smart = smart

        self.header = None
        self.data_set = None

    def check(self):
        """
        Check if the precondition are validate or not

        :raises FileNotFoundError: Error raised when the input file is bad
        """
        if not os.path.exists(self.in_file) or not os.path.isfile(self.in_file):
            raise FileNotFoundError(
                "The file {} is not found".format(os.path.join(os.getcwd(), self.in_file))
            )

    def load(self):
        """
        Parse the csv file into data set
        """
        with open(self.in_file, "r") as f:
            spam_reader = csv.reader(f, delimiter=self.delimiter, quotechar=self.quote)

            # load the header line to extract each columns
            self.header = Translator.decode_header(next(spam_reader))

            # load each lines of data
            self.data_set = [r for r in spam_reader]

    def build(self):
        r_set = []

        for row in self.data_set:
            item = {}

            for key in self.header:
                # the key is the index of the row
                column_header = self.header[key]
                try:
                    item[column_header.name] = column_header.type.parse(row[key])
                except ValueError as e:
                    print(e)
                    sys.exit(1)

            r_set.append(item)

        return r_set

    def dump(self):
        """
        Create the json content before dump in the out file
        """
        with open(self.out_file, "w") as f:
            if self.smart:
                json.dump(self.build(), f, indent=self.smart)
            else:
                json.dump(self.build(), f, separators=(',', ':'))

    @staticmethod
    def decode_header(row):
        """
        Decode the header row by storing data

        :param row: The row header extracted from the csv file
        :type row: list
        :return: The header file descriptor
        :rtype: dict
        """
        header = {}

        for index, column in enumerate(row):
            match = re.match(r"^([a-z_\-]+)\s*\(([a-z.]+)\)$", column.strip(), re.IGNORECASE)
            if match is not None:
                header[index] = CSVHeaderColumn(match.group(1), CSVHeaderColumn.parse_type(match.group(2)))

        return header


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("infile", type=str, help="The input file path parameter")
    parser.add_argument("outfile", type=str, help="The output file path parameter")
    parser.add_argument("-d", "--delimiter", type=str, help="The delimiter of the csv file. Default "
                                                            "value is \";\"")
    parser.add_argument("-q", "--quote", type=str, help="The quote char tu use to parse the csv "
                                                        "file. Default value is '\"'")
    parser.add_argument("-s", "--smart", type=int, help="The smart option allows to indent json file"
                                                        "(SMART as number of spaces for indentation). "
                                                        "Default value is 0", default=0)

    args = parser.parse_args()

    translator = Translator(
        args.infile,
        args.outfile,
        args.delimiter,
        args.quote,
        args.smart
    )
    
    # verify precondition
    translator.check()
    # parse data in RAM
    translator.load()
    # convert data and put the result in output file as JSON format
    translator.dump()


if __name__ == '__main__':
    main()
