from datetime import datetime


class saving_csv:
    def __init__(self):
        self.title = self.__get_file_title()
        with open(self.title, "w") as myfile:
            myfile.write("DISTANCE, REF\n")

    def save_measure(self, d, r, s):
        with open(self.title, "a") as myfile:
            myfile.write(f"{d}, {r}, {s}\n")

    @staticmethod
    def __get_file_title():
        now = datetime.now()
        formatted_datetime = now.strftime("%Y-%m-%d_%H:%M")
        return f"Info_{formatted_datetime}.csv"


