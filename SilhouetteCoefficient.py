import math


class SilhouetteCoefficient:

    clusters = [[]]
    centers = []

    def __init__(self, _clusters=None, _centers=None):
        self.clusters = _clusters
        self.centers = _centers


    def euclidean_distance(self, p1, p2):
        dist = 0

        for i in range(len(p1)):
            dist += (p1[i] - p2[i])**2

        return math.sqrt(dist)

    def intra_distance(self, cluster, center):
        intra_dist = 0

        for point in cluster:
            intra_dist += self.euclidean_distance(point, center)

        return intra_dist/len(cluster)

    def min_inter_distance(self, clusters, center):
        min_distance = float("inf")

        for cluster in clusters:
            cluster_distance_avarage = 0
            cluster_distance = 0
            for point in cluster:
                dist = self.euclidean_distance(point, center)
                cluster_distance += dist

            cluster_distance_avarage = cluster_distance/len(cluster)

            if cluster_distance_avarage < min_distance:
                min_distance = cluster_distance_avarage

        return min_distance

    '''
        intra_dist = küme elemanlarının küme merkezine olan uzaklıklarının ortalaması
        inter_dist = küme merkezinden, diğer kümedeki elemanlara olan uzaklığın minumum olanı
    '''
    def compute(self):

        SC = []

        cluster_list = [[] for i in range(len(self.centers))]

        for c in self.clusters:
            cluster_num = c['C']
            cluster_list[cluster_num].append(c['V'])

        for i in range(len(self.centers)):

            center = self.centers[i]

            c_inter_dist = self.min_inter_distance(cluster_list, center)
            c_intra_dist = self.intra_distance(cluster_list[i], center)
            SC.append((c_inter_dist - c_intra_dist) / ( 0.001 + max([c_inter_dist, c_intra_dist])) )

        return SC
