import copy
import random

import math


class KMeans:

    k = 2
    clusters = []
    centroids = []
    max_iteration = 100

    def __init__(self, k=2, max_iteration=100):
        self.max_iteration = max_iteration
        self.k = k
        print("kmeans clustering...")

    def cosine_similarity(self, v1, v2):
        sum_v1 = 0
        sum_v2 = 0
        product_multiplation = 0

        for index in range(len(v1)):
            _v1 = v1[index]
            _v2 = v2[index]
            sum_v1 += _v1 * _v1
            sum_v2 += _v2 * _v2
            product_multiplation += _v1 * _v2

        return 1 - (product_multiplation / math.sqrt(sum_v1*sum_v2))

    def set_random_centroids(self):
        random_centers = random.sample(self.clusters, self.k)

        for rand in random_centers:
            self.centroids.append(rand['V'])

    def average_data_points(self, data_points):

        len_data = len(data_points)
        average_point = []

        sum_data = data_points[0]

        for data in data_points[1:]:
                sum_data = list(map(sum, zip(data, sum_data)))                # [1,2,3] + [3,4,5] = [4,6,8]

        average_point = list(map(lambda x: x/len_data, sum_data))              # [2,4,6] / 2 = [1,2,3]

        return average_point

    def set_new_centroids(self):
        self.centroids = []
        for center_x in range(self.k):
            data_points_x = [d['V'] for d in list(filter(lambda x: x['C'] == center_x, self.clusters))]   #kümeye ait noktaları al
            centroid_x = self.average_data_points(data_points_x)                                          # noktaların ortalamalarını al
            self.centroids.append(centroid_x)                                                             # yeni merkez olarak ekle

    def fit(self, vector=None):
        cluster = []

        point_count = 0
        for v in vector:
            tfidf_list = []
            for term in vector[v]:
                tfidf_list.append(vector[v][term]['tfidf'])

            point_dict = {'D': point_count, 'C': 0, 'V': tfidf_list}

            point_count += 1
            cluster.append(point_dict)
        self.clusters = cluster

        self.set_random_centroids()         # ilk merkezleri rastgele seç

        temp_clusters = copy.deepcopy(self.clusters)

        count = 0

        while count < self.max_iteration:
            cluster_changed = False

            while temp_clusters:                         # tüm elemanları dolaş
                data_point = temp_clusters.pop()         # listedeki elemanı al ve listeden sil

                min_distance = self.cosine_similarity(data_point['V'], self.centroids[0])   # ilk kümeye uzaklığı hesapla
                min_distance_center = 0
                center_count = 0

                for center in self.centroids[1:]:
                    center_count += 1
                    distance = self.cosine_similarity(data_point['V'], center)       # elemanın en yakın olduğu kümeyi bul
                    if distance < min_distance:
                        min_distance = distance
                        min_distance_center = center_count

                if data_point['C'] != min_distance_center:                           # noktanın min distance lı kümesi değiştiyse
                    self.clusters.remove(data_point)
                    data_point['C'] = min_distance_center
                    self.clusters.append(data_point)
                    cluster_changed = True

            # set new centroids
            self.set_new_centroids()

            temp_clusters = copy.deepcopy(self.clusters)
            count += 1

            # eğer kümeler değişmediyse bitir
            if not cluster_changed:
                break

        for centroid in self.centroids:
            print(centroid)

        return self.clusters, self.centroids