import logging
import csv


class Column(object):
    """
    Column leverages: csv.DictReader(f, delimiter=",") by default
    as a result of that default design, column headers MUST be unique otherwise the last duplicate column header
    will overwrite previous entries
    """

    # constructor
    def __init__(self, file, encoding):
        self.__log = logging.getLogger(__name__)
        self.__file = file
        self.__encoding = encoding

    """
    columns [Array] (Required): 
        Array of string objects that are to be retrieved from the file i.e.,
        ['targetName', 'roles'] will only return identified headers
        ["*"] will return all columns
    
    select [Set or Dict] (Optional): This is a single SELECT statement
        Pass either a set() i.e. {"targetName"}
        or Pass a dict() i.e. {"targetName": "Application Developers"}
        This will be default only accept the first value passed in either the set or dict
        
    distinct [Boolean] Optional: This field will return duplicate rows for a key if false, if true will
        return every occurrence for a key
        
    delimiter_to_array [String](Optional): delimiter to be used to split a field value to an array, i.e. 
        if ";" provided: ldavid;jseinfeld --> ['ldavid', 'jseinfeld']
    """

    def get_rows(self, columns, select=None, distinct=None, delimiter_to_array=None):

        headers = self.has_columns(columns)
        rows = []
        select_list = []
        key = None
        key_value = None

        if type(select) is set:
            for item in select:
                key = item
                break
        elif type(select) is dict:
            for item in select:
                key = item
                key_value = select[item]
                break

        with open(self.__file, encoding=self.__encoding) as f:
            reader = csv.DictReader(f, delimiter=",")

            for row in reader:
                if key and not distinct and len(select_list) == 0 and (not key_value or row[key] == key_value):
                    select_list.append(row[key])

                # this is going to only return on instance of the key, i.e. the first occurrence
                if key and distinct and row[key] not in select_list and (not key_value or row[key] == key_value):
                    rows.append(self.get_row(headers, row, delimiter_to_array))
                    select_list.append(row[key])  # used for select_list purposes

                # this one is going to return all occurrences of the key
                elif key and not distinct and (not key_value or row[key] == key_value and row[key] in select_list):
                    rows.append(self.get_row(headers, row, delimiter_to_array))

                # this is just going to get everything
                elif not key:
                    rows.append(self.get_row(headers, row, delimiter_to_array))

        return rows

    def get_row(self, headers, row, delimiter_to_array=None):

        obj = {}
        for header in headers:
            if delimiter_to_array and delimiter_to_array in row[header]:
                obj[header] = row[header].split(delimiter_to_array)
            else:
                obj[header] = row[header]

        return obj

    # return valid headers only, so if non valid headers are provided they will not return
    def has_columns(self, columns):
        headers = []

        # require the first line of the file for validation
        with open(self.__file, encoding=self.__encoding) as f:
            reader = csv.DictReader(f, delimiter=",")
            row = next(reader)

            if columns[0] == "*":
                headers = row.keys()
            else:
                for column in columns:
                    header = self.has_column(column, row)
                    if header:
                        headers.append(header)
        return headers

    def has_column(self, column, row):
        has = column
        try:
            # an exception will throw if this column header doesn't exist
            row[column]
        except:
            # when exception is thrown we"ll set this to an empty string
            has = None
        return has

