"""Formula One."""
import re
import csv
import copy


class Driver:
    """Driver class."""

    def __init__(self, name: str, team: str):
        """
        Driver constructor.

        Here you should save driver's results as dictionary,
        where key is race number and value is points from that race.
        You must also save driver's points into a variable "points".

        :param name: Driver name
        :param team: Driver team
        """
        self.name = name
        self.team = team
        self.points = 0
        self.results = {}

    def get_results(self) -> dict:
        """
        Get all driver's results.

        :return: Results as dictionary
        """
        results = self.results
        return results

    def get_points(self) -> int:
        """
        Return calculated driver points.

        :return: Calculated points
        """
        self.points = 0
        for point in self.results.values():
            self.points += point
        return self.points

    def add_result(self, race_number: int, points: int):
        """
        Add new result to dictionary of results.

        Dictionary is located in the constructor.

        :param race_number: Race number
        :param points: Number of points from the race
        """
        self.results.update({race_number: points})


class Race:
    """Race class."""

    def __init__(self, file):
        """
        Race constructor.

        Here you should keep data collected from file.
        You must read file rows to list.

        :param file: File with race data
        """
        self.file = file
        self.lines = self.read_file_to_list()

    def read_file_to_list(self):
        """
        Read file data to list in constructor.

        First line shows number of races in data file.
        Rest of the data follows same rules. Each line consists of 'Driver Team Time Race'.
        There are 2 or more spaces between each 'category'.
        E.g. "Mika Häkkinen  McLaren-Mercedes      42069   3"

        If file does NOT exist, throw FileNotFoundError with message "No file found!".
        """
        try:
            self.lines = []
            with open(self.file) as f:
                for line in f:
                    if len(line) > 2:
                        data = Race.extract_info(line)
                        self.lines.append(data)
                    # else:
                        # pass
            return self.lines
        except FileNotFoundError:
            raise FileNotFoundError('No file found!')

    @staticmethod
    def extract_info(line: str) -> dict:
        """
        Helper method for read_file_to_list.

        Here you should convert one data line to dictionary.
        Dictionary must contain following key-value pairs:
            'Name': driver's name as string
            'Team': driver's team as string
            'Time': driver's time as integer (time is always in milliseconds)
            'Diff': empty string
            'Race': race number as integer

        :param line: Data string
        :return: Converted dictionary
        """
        token = re.split(r'\s{2,}', line)
        token_dict = {'Name': token[0], 'Team': token[1], 'Time': int(token[2]), 'Diff': '', 'Race': int(token[3])}
        return token_dict

    def filter_data_by_race(self, race_number: int) -> list:
        """
        Filter data by race number.

        :param race_number: Race number
        :return: Filtered race data
        """
        race = []
        for line in self.lines:
            if line['Race'] == race_number:
                race.append(line)
            # else:
                # pass
        return race

    @staticmethod
    def format_time(time: str) -> str:
        """
        Format time from milliseconds to M:SS.SSS.

        format_time('12') -> 0:00.012
        format_time('1234') -> 0:01.234
        format_time('123456') -> 2:03.456

        :param time: Time in milliseconds
        :return: Time as M:SS.SSS string
        """
        old_time = int(time)
        minutes = old_time % 60000
        seconds = minutes % 1000
        x = int((old_time - minutes) / 60000)
        y = int((minutes - seconds) / 1000)
        z = int(seconds % 1000)
        new_time = f"{x}:{y :02}.{z :03}"
        return new_time

    @staticmethod
    def calculate_time_difference(first_time: int, second_time: int) -> str:
        """
        Calculate difference between two times.

        First time is always smaller than second time. Both times are in milliseconds.
        You have to return difference in format +M:SS.SSS

        calculate_time_difference(4201, 57411) -> +0:53.210

        :param first_time: First time in milliseconds
        :param second_time: Second time in milliseconds
        :return: Time difference as +M:SS.SSS string
        """
        difference = '+' + str(Race.format_time(str(second_time - first_time)))
        return difference

    @staticmethod
    def sort_data_by_time(results: list) -> list:
        """
        Sort results data list of dictionaries by 'Time'.

        :param results: List of dictionaries
        :return: Sorted list of dictionaries
        """
        sorted_time = sorted(results, key=lambda k: int(k['Time']))
        return sorted_time

    def get_results_by_race(self, race_number: int) -> list:
        """
        Final results by race number.

        This method combines the rest of the methods.
        You have to filter data by race number and sort them by time.
        You must also fill 'Diff' as time difference with first position.
        You must add 'Place' and 'Points' key-value pairs for each dictionary.

        :param race_number: Race number for filtering
        :return: Final dictionary with complete data
        """
        points = [25, 18, 15, 12, 10, 8, 6, 4, 2, 1]
        race_result = self.filter_data_by_race(race_number)
        old_result = Race.sort_data_by_time(race_result)
        result = copy.deepcopy(old_result)
        for line in result:
            line['Diff'] = self.calculate_time_difference(result[0]['Time'], line['Time'])
            if line['Diff'] == '+0:00.000':
                line['Diff'] = ''
        i = 1
        for line in result:
            line['Time'] = self.format_time(line['Time'])
            line['Place'] = i
            i += 1
        for line in result:
            if line['Place'] <= 10:
                line['Points'] = points[line['Place'] - 1]
            else:
                line['Points'] = 0
        return result

    def get_results(self):
        """Get results from all races."""
        total_list = []
        with open(self.file) as f:
            total_races = int(f.readline())
        for i in range(1, total_races + 1, 1):
            for line in self.get_results_by_race(i):
                total_list.append(line)
        return total_list


class FormulaOne:
    """FormulaOne class."""

    def __init__(self, file):
        """
        FormulaOne constructor.

        It is reasonable to create Race instance here to collect all data from file.

        :param file: File with race data
        """
        self.file = file
        self.race = Race(file)

    def write_race_results_to_file(self, race_number: int):
        """
        Write one race results to a file.

        File name is 'results_for_race_{race_number}.txt'.
        Exact specifications are described in the text.

        :param race_number: Race to write to file
        """
        with open(f'results_for_race_{race_number}.txt', 'w') as f:
            f.write(f'{"PLACE":10}{"NAME":25}{"TEAM":25}{"TIME":15}{"DIFF":15}{"POINTS":6}\n')
            for i in range(0, 96, 1):
                f.write('-')
            f.write('\n')
            for line in self.race.get_results_by_race(race_number):
                f.write(f'{line["Place"]:<10}{line["Name"]:25}{line["Team"]:25}{line["Time"]:15}{line["Diff"]:15}'
                        f'{line["Points"]:<6}\n')

    def write_race_results_to_csv(self, race_number: int):
        """
        Write one race results to a csv file.

        File name is 'race_{race_number}_results.csv'.
        Exact specifications are described in the text.

        :param race_number: Race to write to file
        """
        with open(f'race_{race_number}_results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(['Place', 'Name', 'Team', 'Time', 'Diff', 'Points', 'Race'])
            for line in self.race.get_results_by_race(race_number):
                writer.writerow([line['Place'], line['Name'], line['Team'], line['Time'], line['Diff'], line['Points'],
                                 line['Race']])

    def write_championship_to_file(self):
        """
        Write championship results to file.

        It is reasonable to create Driver class instance for each unique driver name and collect their points
        using methods from Driver class.
        Exact specifications are described in the text.
        """
        results = self.race.get_results()
        drivers = {}
        for result in results:
            name = result['Name']
            if name in drivers:
                driver = drivers[name]
                driver.add_result(result['Race'], result['Points'])
            else:
                driver = Driver(result['Name'], result['Team'])
                drivers[result['Name']] = driver
                driver.add_result(result['Race'], result['Points'])
            driver.get_points()
        sorted_drivers = sorted(drivers.values(), key=lambda k: k.points, reverse=True)

        with open('championship_results.txt', 'w') as f:
            f.write(f'{"PLACE":10}{"NAME":25}{"TEAM":25}{"POINTS":6}\n')
            for i in range(0, 66, 1):
                f.write('-')
            f.write('\n')
            i = 1
            for driver in sorted_drivers:
                f.write(f'{i:<10}{driver.name:25}{driver.team:25}{driver.points:<6}\n')
                i += 1
