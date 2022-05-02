import csv
import math
import statistics


class ReportCreator:
    def __init__(self, file_name):
        self.all_population_statistics = {}
        self.file_name = file_name

    def save_statistics(self, population_id, statistics_to_save):
        """
        population_id - name of configuration. For example tournament_with_return_p_0_6
        """
        if population_id in self.all_population_statistics:
            self.all_population_statistics[population_id].append(statistics_to_save.copy())
        else:
            self.all_population_statistics[population_id] = [statistics_to_save.copy()]

    def create_csv(self):
        with open(self.file_name, 'w', newline='') as file:
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

            # total result table
            second_table_column_set = ["Suc", "Min", "Max", "Avg", "Min_I_min", "NI_I_min", "Max_I_max", "NI_I_max",
                                       "Sigma_NI", "Avg_I_min", "Avg_I_max", "Avg_I_avg", "Sigma_I_max", "Sigma_I_min",
                                       "Sigma_I_avg", "AvgGR_early", "MinGR_early",
                                       "MaxGR_early", "AvgGR_late", "MinGR_late", "MaxGR_late", "AvgGR_avg",
                                       "MinGR_avg", "MaxGR_avg", "Min_RR_min", "NI_RR_min", "Max_RR_max", "NI_RR_max",
                                       "Avg_RR_min", "Avg_RR_max", "Avg_RR_avg", "Min_Teta_min", "NI_Teta_min",
                                       "Max_Teta_max", "NI_Teta_max", "Avg_Teta_min", "Avg_Teta_max", "Avg_Teta_avg",
                                       "Sigma_RR_max_", "Sigma_RR_min_", "Sigma_RR_avg_",
                                       "Sigma_Teta_max_", "Sigma_Teta_min_", "Sigma_Teta_avg_",
                                       "Min_s_min", "NI_s_min", "Max_s_max", "NI_s_max", "Avg_s_min", "Avg_s_max",
                                       "Avg_s_avg"
                                       ]

            total_stat = self.calc_total_stat()
            # create rounds header
            for i in range(num_of_rounds):
                round_num.append(f"Прогін {i + 1}")
                for col in first_table_column_set:
                    headers.append(col)
                    round_num.append(" ")
                headers.append("     ")
            round_num.append("TOTAL")
            headers += second_table_column_set

            writer.writerow(round_num)
            writer.writerow(headers)

            for key, value in self.all_population_statistics.items():
                row = [key]
                for i in range(num_of_rounds):
                    round_data = value[i]
                    for col in first_table_column_set:
                        row.append(round_data.get(col, ""))
                    row.append(" ")

                total_item_val = total_stat[key]
                for col in second_table_column_set:
                    row.append(total_item_val.get(col, ""))
                writer.writerow(row)



    def calc_total_stat(self):
        res = {}
        for key, value in self.all_population_statistics.items():
            method_total_res = self.calc_method_total_stat(key)
            res[key] = method_total_res
        return res

    @staticmethod
    def calc_sigma(arr):
        n = len(arr)
        avg_x = 1/n * sum(arr)
        res = math.sqrt(1/(n-1) * sum([(i - avg_x)**2 for i in arr]))
        return res

    def calc_method_total_stat(self, method_name):
        data = self.all_population_statistics[method_name]
        res = {}

        def is_round_success(round):
            return round["Suc"]

        successful_rounds = list(filter(is_round_success, data))

        res["Suc"] = len(successful_rounds)

        if len(successful_rounds) > 0:
            res["Min"] = min([i["NI"] for i in successful_rounds])
            res["Max"] = max([i["NI"] for i in successful_rounds])
            res["Avg"] = statistics.mean([i["NI"] for i in successful_rounds])

            # intensity
            min_intensity = sorted(successful_rounds, key=lambda i: i["I_min"])[0]
            res["Min_I_min"] = min_intensity["I_min"]
            res["NI_I_min"] = min_intensity["NI_I_min"]
            max_intensity = sorted(successful_rounds, key=lambda i: i["I_max"], reverse=True)[0]
            res["Max_I_max"] = max_intensity["I_max"]
            res["NI_I_max"] = max_intensity["NI_I_max"]

            res["Sigma_NI"] = self.calc_sigma([i["NI"] for i in successful_rounds])

            res["Avg_I_min"] = statistics.mean([i["I_min"] for i in successful_rounds])
            res["Avg_I_max"] = statistics.mean([i["I_max"] for i in successful_rounds])
            res["Avg_I_avg"] = statistics.mean([i["I_avg"] for i in successful_rounds])

            res["Sigma_I_max"] = self.calc_sigma([i["I_max"] for i in successful_rounds])
            res["Sigma_I_min"] = self.calc_sigma([i["I_min"] for i in successful_rounds])
            res["Sigma_I_avg"] = self.calc_sigma([i["I_avg"] for i in successful_rounds])

            res["AvgGR_early"] = statistics.mean([i["GR_early"] for i in successful_rounds])
            res["MinGR_early"] = min([i["GR_early"] for i in successful_rounds])
            res["MaxGR_early"] = max([i["GR_early"] for i in successful_rounds])

            res["AvgGR_late"] = statistics.mean([i["GR_late"] for i in successful_rounds])
            res["MinGR_late"] = min([i["GR_late"] for i in successful_rounds])
            res["MaxGR_late"] = max([i["GR_late"] for i in successful_rounds])

            res["AvgGR_avg"] = statistics.mean([i["GR_avg"] for i in successful_rounds])
            res["MinGR_avg"] = min([i["GR_avg"] for i in successful_rounds])
            res["MaxGR_avg"] = max([i["GR_avg"] for i in successful_rounds])

            min_rr_min = sorted(successful_rounds, key=lambda i: i["RR_min"])[0]
            res["Min_RR_min"] = min_rr_min["RR_min"]
            res["NI_RR_min"] = min_rr_min["NI_RR_min"]
            max_rr_max = sorted(successful_rounds, key=lambda i: i["RR_max"], reverse=True)[0]
            res["Max_RR_max"] = max_rr_max["RR_max"]
            res["NI_RR_max"] = max_rr_max["NI_RR_max"]

            res["Avg_RR_min"] = statistics.mean([i["RR_min"] for i in successful_rounds])
            res["Avg_RR_max"] = statistics.mean([i["RR_max"] for i in successful_rounds])
            res["Avg_RR_avg"] = statistics.mean([i["RR_avg"] for i in successful_rounds])

            min_teta_min = sorted(successful_rounds, key=lambda i: i["Teta_min"])[0]
            res["Min_Teta_min"] = min_teta_min["Teta_min"]
            res["NI_Teta_min"] = min_teta_min["NI_Teta_min"]
            max_teta_max = sorted(successful_rounds, key=lambda i: i["Teta_max"], reverse=True)[0]
            res["Max_Teta_max"] = max_teta_max["Teta_max"]
            res["NI_Teta_max"] = max_teta_max["NI_Teta_max"]

            res["Avg_Teta_min"] = statistics.mean([i["Teta_min"] for i in successful_rounds])
            res["Avg_Teta_max"] = statistics.mean([i["Teta_max"] for i in successful_rounds])
            res["Avg_Teta_avg"] = statistics.mean([i["Teta_avg"] for i in successful_rounds])

            res["Sigma_RR_max_"] = self.calc_sigma([i["RR_max"] for i in successful_rounds])
            res["Sigma_RR_min_"] = self.calc_sigma([i["RR_min"] for i in successful_rounds])
            res["Sigma_RR_avg_"] = self.calc_sigma([i["RR_avg"] for i in successful_rounds])
            res["Sigma_Teta_max_"] = self.calc_sigma([i["Teta_max"] for i in successful_rounds])
            res["Sigma_Teta_min_"] = self.calc_sigma([i["Teta_min"] for i in successful_rounds])
            res["Sigma_Teta_avg_"] = self.calc_sigma([i["Teta_avg"] for i in successful_rounds])

            min_s_min = sorted(successful_rounds, key=lambda i: i["s_min"])[0]
            res["Min_s_min"] = min_s_min["s_min"]
            res["NI_s_min"] = min_s_min["NI_s_min"]

            max_s_max = sorted(successful_rounds, key=lambda i: i["s_max"], reverse=True)[0]
            res["Max_s_max"] = max_s_max["s_max"]
            res["NI_s_max"] = max_s_max["NI_s_max"]

            res["Avg_s_min"] = statistics.mean([i["s_min"] for i in successful_rounds])
            res["Avg_s_max"] = statistics.mean([i["s_max"] for i in successful_rounds])
            res["Avg_s_avg"] = statistics.mean([i["s_avg"] for i in successful_rounds])

        return res
