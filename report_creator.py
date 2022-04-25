import csv
import statistics


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
        with open('report1.csv', 'w', newline='') as file:
            writer = csv.writer(file)

            # rounds' results
            headers = [""]
            round_num = [""]
            num_of_rounds = len(list(self.all_population_statistics.values())[0])

            # column_set = list(list(self.all_population_statistics.values())[0])[0].keys()

            first_table_column_set = ["NI", "F_found", "F_avg", "I_min", "NI_I_min", "I_max", "NI_I_max", "I_avg",
                                      "GR_early", "GR_avg", "GR_late", "NI_GR_late", "RR_min", "NI_RR_min", "RR_max",
                                      "NI_RR_max", "RR_avg", "Teta_min", "NI_Teta_min", "Teta_max", "NI_Teta_max",
                                      "Teta_avg", "s_min", "NI_s_min", "s_max", "NI_s_max", "s_avg"]

            # create rounds header
            for i in range(num_of_rounds):
                round_num.append(f"Прогін {i + 1}")
                for col in first_table_column_set:
                    headers.append(col)
                    round_num.append(" ")
                headers.append("     ")

            writer.writerow(round_num)
            writer.writerow(headers)

            for key, value in self.all_population_statistics.items():
                row = [key]
                for i in range(num_of_rounds):
                    round_data = value[i]
                    for col in first_table_column_set:
                        row.append(round_data[col])
                    row.append(" ")
                writer.writerow(row)

            writer.writerow([""])

            # total result table
            second_table_column_set = ["Suc", "Min", "Max", "Avg", "Min_I_min", "NI_I_min", "Max_I_max", "NI_I_max",
                                       "Avg_I_min", "Avg_I_max", "Avg_I_avg"]
            writer.writerow([""]+second_table_column_set)

            for key, value in self.calc_total_stat().items():
                row = [key]
                for col in second_table_column_set:
                    row.append(value[col])
                writer.writerow(row)

    def calc_total_stat(self):
        res = {}
        for key, value in self.all_population_statistics.items():
            method_total_res = self.calc_method_total_stat(key)
            res[key] = method_total_res
        return res

    def calc_method_total_stat(self, method_name):
        data = self.all_population_statistics[method_name]
        res = {}

        def is_round_success(round):
            return round["Suc"]

        successful_rounds = list(filter(is_round_success, data))

        res["Suc"] = len(successful_rounds)
        res["Min"] = min([i["NI"] for i in successful_rounds])
        res["Max"] = max([i["NI"] for i in successful_rounds])
        res["Avg"] = statistics.mean([i["NI"] for i in successful_rounds])

        # intensity
        min_intensity = sorted(successful_rounds, key=lambda i: i["I_min"])[0]
        res["Min_I_min"] = min_intensity["I_min"]
        res["NI_I_min"] = min_intensity["NI_I_min"]
        max_intensity = sorted(successful_rounds, key=lambda i: i["I_max"], reverse=True)[0]
        res["Max_I_max"] = min_intensity["I_max"]
        res["NI_I_max"] = min_intensity["NI_I_max"]

        # res["Sigma_NI"]

        res["Avg_I_min"] = statistics.mean([i["I_min"] for i in successful_rounds])
        res["Avg_I_max"] = statistics.mean([i["I_max"] for i in successful_rounds])
        res["Avg_I_avg"] = statistics.mean([i["I_avg"] for i in successful_rounds])

        # res["Sigma_I_max"]
        # res["Sigma_I_min"]
        # res["Sigma_I_avg"]

        # res["AvgGR_early"]
        # res["MinGR_early"]
        # res["AvgGR_early"]

        return res
