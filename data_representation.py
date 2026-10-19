import csv


class DataTable:
    def __init__(self, csv_path: str,reference=None):
        """
        Load CSV data into memory.
        Convert all values to float.
        """
        self.data = []
        self.column_names = [] #the header values

        with open(csv_path, 'r') as file: #csv_path is a placeholder
            reader = csv.reader(file) #reader that can go through the file line by line
            #it comes from the csv import thingy
            self.column_names = next(reader) #skiping the header
            for row in reader:
                numbers = []
                for value in row:
                    if value == '?':
                        numbers.append(None)
                    else:
                        numbers.append(float(value))
                self.data.append(numbers)
         # Replace missing values (None) with a column mean
        for column_index in range(len(self.column_names)):
            if reference is None:
                # historical data: mean of this column's valid values
                valid = [row[column_index] for row in self.data if row[column_index] is not None]
                mean = sum(valid) / len(valid)
            else:
                # new cases: mean from the historical table
                mean = reference.get_column_average(self.column_names[column_index])

            for row in self.data:
                if row[column_index] is None:
                    row[column_index] = mean




    def get(self, row_idx: int, col_name: str):
        """
        Return a single value from a row and column.
        """
        column_index = self.column_names.index(col_name) #finds the position index number of the column

        return self.data[row_idx][column_index] #the row_idex gets the whole row
        #column_index gets the value of the index at that specific row


    def get_column(self, col_name: str) -> list:
        """
        Return all values in a column.
        """
        column_index = self.column_names.index(col_name) #find the index in the column like before
        values = []
        for row in self.data: #looking through all the rows
            values.append(row[column_index]) #grabbin the value from that column

        return values

    def get_row(self, row_idx: int) -> dict:
        """
        Return a row as {column_name: value}
        """

        row = self.data[row_idx]
        result = {} #empty dictionary to fill up

        for i in range(len(self.column_names)):
            col_name = self.column_names[i]
            result[col_name] = row[i] #adds a key-value pair to the dictionary
        return result



    def get_column_names(self) -> list:
        """
        Return list of column names.
        """
        return self.column_names # we are using the list from the innit functiion here


    def get_column_average(self, col_name: str) -> float:
        """
        Return average of a column.
        """
        values = self.get_column(col_name)
        if values:
            return sum(values) / len(values)
        else:
            return 0 #taking the average sum diviide by the length

    def get_column_min(self, col_name: str) -> float:
        """
        Return minimum value of a column.
        """
        values = self.get_column(col_name)
        if values:
            return min(values)
        else:
            return 0

    def get_column_max(self, col_name: str) -> float:
        """
        Return maximum value of a column.
        """
        values = self.get_column(col_name)
        if values:
            return max(values)
        else:
            return 0