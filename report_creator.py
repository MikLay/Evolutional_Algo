import csv


class ReportCreator:
    def __init__(self):
        self.all_population_statistics = {}

    def save_statistics(self, population_id, statistics_to_save):
        """
        population_id - name of configuration. For example tournament_with_return_p_0_6
        """
        if population_id in self.all_population_statistics:
            self.all_population_statistics[population_id].append(statistics_to_save.copy())
        else:
            self.all_population_statistics[population_id] = [statistics_to_save.copy()]

    def create_csv(self):
        with open('report.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            headers = [""]
            round_num = [""]
            num_of_rounds = len(list(self.all_population_statistics.values())[0])

            column_set = list(list(self.all_population_statistics.values())[0])[0].keys()
            # create rounds header
            for i in range(num_of_rounds):
                round_num.append(f"Прогін {i + 1}")
                for col in column_set:
                    headers.append(col)
                    round_num.append(" ")
                headers.append("     ")

            writer.writerow(round_num)
            writer.writerow(headers)
            for key, value in self.all_population_statistics.items():
                row = [key]
                for i in range(num_of_rounds):
                    round_data = value[i]
                    for col in column_set:
                        row.append(round_data[col])
                    row.append(" ")
                writer.writerow(row)
