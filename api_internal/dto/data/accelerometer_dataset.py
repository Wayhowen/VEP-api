# # import numpy as np
# from matplotlib import pyplot
#
# from dto.data.accelerometer_reading import Reading as AccelerometerReading
#
#
# class Dataset:
#     def __init__(self, data):
#         self.dataset = [AccelerometerReading(data_entry) for data_entry in data]
#         # self.speed = self._calculate_speed()
#
#     @property
#     def dataset_times(self):
#         return list([entry.time.timestamp() for entry in self.dataset])
#
#     @property
#     def dataset_x(self):
#         return list([entry.x for entry in self.dataset])
#
#     @property
#     def dataset_y(self):
#         return list([entry.y for entry in self.dataset])
#
#     @property
#     def dataset_z(self):
#         return list([entry.z for entry in self.dataset])
#
#     @property
#     def print_raw(self):
#         for item in self.dataset:
#             print(item)
#
#     # delta V = acc * delta T
#     # we can approximate speed if we know what way the phone is facing
#
#     def _calculate_speed(self):
#         speed_dict = {
#             "x": [0],
#             "y": [0],
#             "z": [0]
#         }
#         initial_speed = 0
#
#         timesteps = []
#         for index, entry in enumerate(self.dataset[1:]):
#             timesteps.append(entry.time - self.dataset[index].time)
#
#         for index, entry in enumerate(self.dataset):
#             if index == 0:
#                 print(0)
#             else:
#                 initial_speed += (entry.z * timesteps[index-1].total_seconds())
#                 print(initial_speed)
#
#         return []
#
#     def create_graph(self, title):
#         data = [-1, 0, 1, -1, -1, 0, 2, 1]
#         data1 = list(reversed(data))
#         time = [index for index, _ in enumerate(data)]
#
#         fig, ax = pyplot.subplots()
#         ax.plot(self.dataset_times, self.dataset_z, label=None)
#         ax.plot(self.dataset_times, self.dataset_x, label=None)
#         ax.plot(self.dataset_times, self.dataset_y, label=None)
#         ax.grid(True)
#         # ax.plot(time, data1, label="second data")
#         ax.set_title(title)
#         ax.legend(loc='upper left')
#         ax.set_ylabel('Accelerometer Reading')
#         ax.set_xlabel('Time of reading')
#         # ax.set_xlim(xmin=min(time), xmax=max(time))
#         fig.tight_layout()
#         fig.show()
