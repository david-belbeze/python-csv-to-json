# Python CSV to JSON

This script can be used to convert csv to json.

The syntax describe below provide information to the script to help to 
convert the csv data set into json sequence.

## Prerequistes

Python 3.

## Usage 

To see the documentation you can use the following command.

`python __main__.py --help`

```text
usage: __main__.py [-h] [-d DELIMITER] [-q QUOTE] [-s SMART] infile outfile

positional arguments:
  infile                The input file path parameter
  outfile               The output file path parameter

optional arguments:
  -h, --help            show this help message and exit
  -d DELIMITER, --delimiter DELIMITER
                        The delimiter of the csv file. Default value is ";"
  -q QUOTE, --quote QUOTE
                        The quote char tu use to parse the csv file. Default
                        value is '"'
  -s SMART, --smart SMART
                        The smart option allows to indent json file(SMART as
                        number of spaces for indentation). Default value is 0
```

## CSV header syntax

Each column can define a json object field. It is only necessary to define the type 
of the column.

> If the type is not defined, the column is ignored in json output sequence.

Field types are:
 - i: integer
 - f: float
 - b: boolean
 - s: string
 - a.[type]: array of [type]. Use the code of field type above (`i`, `f`, `b` 
   or `s`).
 
For example the column `id (i)` indicate "add the `id` field as an integer".

For arrays, use the syntax `serices (a.s)` to indicate "add `services` field 
as array of string". 

> the header column is trimmed and convert as lower case.  
So `" userCount (i) "` will be converted as "usercount" in json object.

See the example to understand the process.

## Example

Consider the next csv file "input.csv"

|id (i)|name (s)|premium (b)|services (a.s)|disabled
| - | - | - | - | - |
|0|David|0|read,write,admin|0|
|1|Robert|1|read,write|1|
|2|Alice|0|read|1|

Format is:

```csv
id (i);name (s);premium (b);services (a.s);disabled
0;David;0;read,write,admin;0
1;Robert;1;read,write;1
2;Alice;0;read;1
```

Run the following command

`python __main__.py input.csv output.json -d ";" -s 4`

The content of the output.json will be

```json
[
    {
        "premium": false,
        "services": [
            "read",
            "write",
            "admin"
        ],
        "id": 0,
        "name": "David"
    },
    {
        "premium": true,
        "services": [
            "read",
            "write"
        ],
        "id": 1,
        "name": "Robert"
    },
    {
        "premium": false,
        "services": [
            "read"
        ],
        "id": 2,
        "name": "Alice"
    }
]
```

## License MIT

Copyright 2019 David BELBEZE

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated 
documentation files (the "Software"), to deal in the Software without restriction, including without limitation the 
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit 
persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the 
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE 
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR 
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR 
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

