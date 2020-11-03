# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 18:07:11 2020

@author: wegia
"""


import math
import random
import csv
import numpy as np
import cProfile
import hashlib

memoization = {}


class Clustering:
    """
    An instance of the Clustering is a solution i.e. a particular partitioning of the (heterogeneous) data set into
    homogeneous subsets. For Centroid based clustering algorithms this involves looking at each pattern and assigning
    it to it's nearest centroid. This is done by calculating the distance between each pattern and every centroid and
    selecting the one with the smallest distance. Here we use are using fractional distance with the default parameters.

    :param d: dimensionality of the input patterns
    :param k: the pre-specified number of clusters & centroids
    :param z: the patterns in the data set
    :param min: the minimum distance (required to prevent division by zero)
    """

    def __init__(self, d, k, z, min):
        # print("Initializing solution ...")
        """
        Initializes a Clustering object with the specified parameters
        :param d: dimensionality of the input patterns
        :param k: the pre-specified number of clusters & centroids
        :param z: the patterns in the data set
        :param min: the minimum distance (required to prevent division by zero)
        """
        self.dimensionality = d
        self.num_clusters = k
        self.patterns = z
        self.solution = []
        for i in range(len(z)):
            self.solution.append(0)
        self.centroids = np.random.rand(k, d)
        self.e = min

    def re_init(self):
        """
        A method for reinitializing the solution
        """
        self.centroids = None
        self.centroids = np.random.rand(self.num_clusters, self.dimensionality)

    def assign_patterns(self):
        """
        This method iterates over all patterns and calculates the distances between that pattern and every centroid.
        These value are stored in [distances]. The assign_pattern method is then used to find the centroid with the
        smallest distance and update the 'label' i.e. centroid which the pattern is associated.
        """
        s = Similarity(self.e)
        # for each pattern
        for i in range(len(self.patterns)):
            # for each centroid
            distances = []
            for j in range(self.num_clusters):
                # calculate the distances
                distances.append(s.fractional_distance(self.centroids[j], self.patterns[i]))
            # assign the pattern to a cluster
            self.assign_pattern(distances, i)

    def assign_pattern(self, distances, index):
        """
        This method updates the label i.e. centroid index \in (0, k-1) to which pattern z(index) belongs
        :param distances: distances to each centroid
        :param index: the index of the pattern we are assigning in z
        """
        self.solution[index] = 0
        smallest = distances[self.solution[index]]
        for i in range(len(distances)):
            if distances[i] < smallest:
                smallest = distances[i]
                self.solution[index] = i

    def update_centroids(self, s=1.0):
        """
        This method implements the mean-shift heuristic used by the K-means clustering algorithm. This heuristic
        updates the value of each centroid with the average value at each dimension of the patterns assigned to it.
        :param s: this is the scaling factor i.e. how much we want to diminish the movement of the centroids by
        """
        # Step 1 - initialize a variable to store the sum at each dimension of the patterns assigned to each centroid
        centroids_sum = []
        for i in range(self.num_clusters):
            centroids_sum.append([])
            for j in range(self.dimensionality):
                centroids_sum[i].append(0.0)
        # Step 2 - initialize a variable to store the count of patterns assigned to each centroid
        centroids_count = []
        for i in range(self.num_clusters):
            centroids_count.append(0.0)
        # Step 3 - Update the value of centroids_sum and centroids_count for step 4
        for i in range(len(self.solution)):
            for j in range(self.dimensionality):
                centroids_sum[self.solution[i]][j] += self.patterns[i][j]
            centroids_count[self.solution[i]] += 1
        # Step 4 - compute the averages (total / count) for each dimension for each centroid
        centroids_average = []
        for i in range(self.num_clusters):
            centroids_average.append([])
            for j in range(self.dimensionality):
                if centroids_count[i] > 0:
                    centroids_average[i].append(centroids_sum[i][j] / max(1.0, centroids_count[i]))
                else:
                    centroids_average[i].append(random.random())
        # Step 5 - set  each dimension of each centroid to the average of it's clusters values at that dimension
        for i in range(self.num_clusters):
            if s == 1.0:
                self.centroids[i] = None
                self.centroids[i] = centroids_average[i]
            else:
                for j in range(len(self.centroids[i])):
                    self.centroids[i][j] += (centroids_average[i][j] - self.centroids[i][j]) * s

    def k_means_clustering(self, n, s=1.0):
        """
        This method performs the K-means clustering algorithm on the data for n iterations. This involves updating the
        centroids using the mean-shift heuristic n-times and reassigning the patterns to their closest centroids.
        :param n: number of iterations to complete
        :param s: the scaling factor to use when updating the centroids
        pick on which has a better solution (according to some measure of cluster quality)
        """

        for i in range(n):
            self.assign_patterns()
            self.update_centroids(s)

    def print_solution(self, labels):
        """
        Prints out the clustering i.e. which patterns are assigned to which centroids. This can be cross-referenced
        with the label on each pattern to determine which countries are clustered together in space.
        :param labels: pattern labels
        """
        for i in range(len(self.solution)):
            print(labels[i], ",", self.solution[i])


class ClusteringQuality:
    """
    Instances of this class implement the two measures of clustering quality discussed in the article, namely the davies
    bouldin index and the silhouette index. It also implements a number of useful helper methods.
    :param solution: the clustering solution of type Clustering
    :param minimum: the minimum distance allowable
    """

    def __init__(self, solution, minimum):
        """
        Initializes a ClusteringQuality object with a given Clustering solution and a minimum distance
        :param solution: this is an object of type Clustering
        :param minimum: this is the minimum distance allowed between two points
        """
        assert isinstance(solution, Clustering)
        self.solution = solution
        self.e = minimum

    def cluster_totals(self):
        """
        This method calculates the total distance from every centroid to every pattern assigned to it. It also records
        the number of patterns in each cluster which are used to compute average distances in cluster_averages()
        :return: a two dimensional list of [total cluster distance, total patterns in cluster] for each centroid
        """
        s = Similarity(self.e)
        # create array (will be 2d) to store total internal cluster distances and cluster counts for each centroid
        cluster_distances_counts = []
        for i in range(self.solution.num_clusters):
            ith_cluster_count = 0.0
            ith_cluster_distance = 0.0
            for z in range(len(self.solution.solution)):
                # update the count and the total distance for the centroid z[i] belongs to (whichever one that is)
                if self.solution.solution[z] == i:
                    ith_cluster_count += 1
                    ith_cluster_distance += s.fractional_distance(self.solution.patterns[z], self.solution.centroids[i])
            # add the result to the 2d list
            cluster_distances_counts.append([ith_cluster_distance, max(ith_cluster_count, 1.0)])
        return np.array(cluster_distances_counts)

    def cluster_averages(self):
        """
        Receives output from cluster_totals() and computes the average distance per centroid
        :return: average distance from each centroid to the patterns assigned to it
        """
        # create list to store averages in
        cluster_averages = []
        # get the total internal cluster distances plus the counts for each centroid / cluster
        cluster_distances_counts = self.cluster_totals()
        for i in range(len(cluster_distances_counts)):
            # calculate the averages and add it to the list
            cluster_averages.append(cluster_distances_counts[i][0] / cluster_distances_counts[i][1])
        return np.array(cluster_averages)

    def davies_bouldin(self):
        """
        This method computes the davies-bouldin (db) of a given clustering.
        :return: the davies bouldin value of the clustering
        """
        # get the average internal cluster distances
        cluster_averages = self.cluster_averages()
        # create variable for db
        davies_bouldin = 0.0
        s = Similarity(self.e)
        # for each cluster / centroid i
        for i in range(self.solution.num_clusters):
            # for each cluster / centroid j
            for j in range(self.solution.num_clusters):
                # when i and j are not the same cluster / centroid
                if j != i:
                    # calculate the distance between the two centroids of i and j
                    d_ij = s.fractional_distance(self.solution.centroids[i], self.solution.centroids[j])
                    # update the variable to equal to sum of internal cluster distances of clusters i and j divided by
                    # the previously computer value i.e. the distance between centroid i and centroid j
                    d_ij = (cluster_averages[i] + cluster_averages[j]) / d_ij
                    # update db is this is larger than any db seen before
                    davies_bouldin = max(d_ij, davies_bouldin)
        return davies_bouldin

    def silhouette_index(self, index):
        """
        This method computes the silhouette index (si) for any given pattern between -1 and 1
        :param index: the pattern we are looking at now
        :return: the silhouette index for that pattern
        """
        # store the total distance to each cluster
        silhouette_totals = []
        # store the number of patterns in each cluster
        silhouette_counts = []
        # initialize the variables
        for i in range(self.solution.num_clusters):
            silhouette_totals.append(0.0)
            silhouette_counts.append(0.0)
        s = Similarity(self.e)
        for i in range(len(self.solution.patterns)):
            # for every pattern other than the one we are calculating now
            if i != index:
                # get the distance between pattern[index] and that pattern
                distance = s.fractional_distance(self.solution.patterns[i], self.solution.patterns[index])
                # add that distance to the silhouette totals for the correct cluster
                silhouette_totals[self.solution.solution[i]] += distance
                # update the number of patterns in that cluster
                silhouette_counts[self.solution.solution[i]] += 1
        # setup variable to find the cluster (not equal to the pattern[index]'s cluster) with the smallest distance
        smallest_silhouette = silhouette_totals[0] / max(1.0, silhouette_counts[0])
        for i in range(len(silhouette_totals)):
            # calculate the average distance of each pattern in that cluster from pattern[index]
            silhouette = silhouette_totals[i] / max(1.0, silhouette_counts[i])
            # if the average distance is lower and it isn't pattern[index] cluster update the value
            if silhouette < smallest_silhouette and i != self.solution.solution[index]:
                smallest_silhouette = silhouette
        # calculate the internal cluster distances for pattern[index]
        index_cluster = self.solution.solution[index]
        index_silhouette = self.e + silhouette_totals[index_cluster] / max(1.0, silhouette_counts[index_cluster])
        # return the ratio between the smallest distance from pattern[index] to another cluster's patterns and
        # the patterns belong to the same cluster as pattern[index]
        return (smallest_silhouette - index_silhouette) / max(smallest_silhouette, index_silhouette)

    def silhouette_index_zero_one(self, index):
        """
        Returns the silhouette index between 0 and 1 and makes it a minimization objective (easier)
        :param index: the pattern we are looking at now
        :return: the silhouette index for that pattern
        """
        return 1 - ((1 + self.silhouette_index(index)) / 2.0)

    def average_silhouette_index(self, scaled_zero_one=True):
        """
        This method computes the average silhouette index value every pattern in the data set.
        :param scaled_zero_one: allows you to scale the result between 0 and 1 and reverse the order
        :return: the silhouette index of the given clustering
        """
        silhouette_sum = 0.0
        for i in range(len(self.solution.patterns)):
            if scaled_zero_one:
                silhouette_sum += self.silhouette_index_zero_one(i)
            else:
                silhouette_sum += self.silhouette_index(i)
        return silhouette_sum / len(self.solution.patterns)

    def quantization_error(self):
        """
        This method calculates the quantization error of the given clustering
        :return: the quantization error
        """
        total_distance = 0.0
        s = Similarity(self.e)
        for i in range(len(self.solution.patterns)):
            total_distance += math.pow(s.fractional_distance(self.solution.patterns[i],
                                                             self.solution.centroids[self.solution.solution[i]]), 2.0)
        return total_distance / len(self.solution.patterns)


class Similarity:
    """
    This class contains instances of similarity / distance metrics. These are used in centroid based clustering
    algorithms to identify similar patterns and put them into the same homogeneous sub sets
    :param minimum: the minimum distance between two patterns (so you don't divide by 0)
    """

    def __init__(self, minimum):
        self.e = minimum
        self.vector_operators = VectorOperations()

    def manhattan_distance(self, p_vec, q_vec):
        """
        This method implements the manhattan distance metric
        :param p_vec: vector one
        :param q_vec: vector two
        :return: the manhattan distance between vector one and two
        """
        return max(np.sum(np.fabs(p_vec - q_vec)), self.e)

    def square_euclidean_distance(self, p_vec, q_vec):
        """
        This method implements the squared euclidean distance metric
        :param p_vec: vector one
        :param q_vec: vector two
        :return: the squared euclidean distance between vector one and two
        """
        diff = p_vec - q_vec
        return max(np.sum(diff ** 2), self.e)

    def euclidean_distance(self, p_vec, q_vec):
        """
        This method implements the euclidean distance metric
        :param p_vec: vector one
        :param q_vec: vector two
        :return: the euclidean distance between vector one and two
        """
        return max(math.sqrt(self.square_euclidean_distance(p_vec, q_vec)), self.e)

    def half_square_euclidean_distance(self, p_vec, q_vec):
        """
        This method implements the half squared euclidean distance metric
        :param p_vec: vector one
        :param q_vec: vector two
        :return: the half squared euclidean distance between vector one and two
        """
        return max(0.5 * self.square_euclidean_distance(p_vec, q_vec), self.e)

    def cosine_similarity(self, p_vec, q_vec):
        """
        This method implements the cosine similarity metric
        :param p_vec: vector one
        :param q_vec: vector two
        :return: the cosine similarity between vector one and two
        """
        pq = self.vector_operators.product(p_vec, q_vec)
        p_norm = self.vector_operators.norm(p_vec)
        q_norm = self.vector_operators.norm(q_vec)
        return max(pq / (p_norm * q_norm), self.e)

    def tanimoto_coefficient(self, p_vec, q_vec):
        """
        This method implements the cosine tanimoto coefficient metric
        :param p_vec: vector one
        :param q_vec: vector two
        :return: the tanimoto coefficient between vector one and two
        """
        pq = self.vector_operators.product(p_vec, q_vec)
        p_square = self.vector_operators.square(p_vec)
        q_square = self.vector_operators.square(q_vec)
        return max(pq / (p_square + q_square - pq), self.e)

    def fractional_distance(self, p_vec, q_vec, fraction=2.0):
        """
        This method implements the fractional distance metric. I have implemented memoization for this method to reduce
        the number of function calls required. The net effect is that the algorithm runs 400% faster. A similar approach
        can be used with any of the above distance metrics as well.
        :param p_vec: vector one
        :param q_vec: vector two
        :param fraction: the fractional distance value (power)
        :return: the fractional distance between vector one and two
        """
        # memoization is used to reduce unnecessary calculations ... makes a BIG difference
        memoize = True
        if memoize:
            key = self.get_key(p_vec, q_vec)
            x = memoization.get(key)
            if x is None:
                diff = p_vec - q_vec
                diff_fraction = diff ** fraction
                return max(math.pow(np.sum(diff_fraction), 1 / fraction), self.e)
            else:
                return x
        else:
            diff = p_vec - q_vec
            diff_fraction = diff ** fraction
            return max(math.pow(np.sum(diff_fraction), 1 / fraction), self.e)

    @staticmethod
    def get_key(p_vec, q_vec):
        """
        This method returns a unique hash value for two vectors. The hash value is equal to the concatenated string of
        the hash value for vector one and vector two. E.g. is hash(p_vec) = 1234 and hash(q_vec) = 5678 then get_key(
        p_vec, q_vec) = 12345678. Memoization improved the speed of this algorithm 400%.
        :param p_vec: vector one
        :param q_vec: vector two
        :return: a unique hash
        """
        # return str(hash(tuple(p_vec))) + str(hash(tuple(q_vec)))
        return str(hashlib.sha1(p_vec)) + str(hashlib.sha1(q_vec))


class VectorOperations():
    """
    This class contains useful implementations of methods which can be performed on vectors
    """

    @staticmethod
    def product(p_vec, q_vec):
        """
        This method returns the product of two lists / vectors
        :param p_vec: vector one
        :param q_vec: vector two
        :return: the product of p_vec and q_vec
        """
        return p_vec * q_vec

    @staticmethod
    def square(p_vec):
        """
        This method returns the square of a vector
        :param p_vec: the vector to be squared
        :return: the squared value of the vector
        """
        return p_vec ** 2

    @staticmethod
    def norm(p_vec):
        """
        This method returns the norm value of a vector
        :param p_vec: the vector to be normed
        :return: the norm value of the vector
        """
        return np.sqrt(p_vec)


class Data():
    """
    A class for downloading data from a CSV file
    :param file_name: the file name
    :return: the data
    """

    def __init__(self, file_name):
        self.file_name = file_name
        return

    def load_data(self):
        """
        This method opens the file and reads it in
        :return:
        """
        loaded_patterns = []
        file = open(self.file_name)
        row_number = 0
        labels = []
        for row in csv.reader(file):
            if row_number != 0:
                floats = []
                for j in range(len(row)):
                    if j != 0:
                        floats.append(float(row[j]))
                    else:
                        labels.append(row[j])
                loaded_patterns.append(floats)
            row_number += 1
        return np.array(loaded_patterns), labels


def forest_run(dimensions, patterns, pattern_labels, metric='qe', k_up=20, k_down=2, simulations=55, iterations=50):
    """
    A method for watching Forest Gump run
    :param dimensions: the dimensionality of the data
    :param patterns: the data itself
    :param metric: the quality metric
    :param k_up: the maximum number of clusters
    :param k_down: the minimum number of clusters
    :param simulations: the number of simulations for each k
    :param iterations: the number of iterations for each k-means pass
    """
    # variable to store the best result
    best_clustering = None
    # the quality of that result
    best_quality = 1000.00
    # write results out to file while simulating
    file_out = 'E:\Monte Carlo Final Results' + '_' + metric + '.csv'
    with open(file_out, 'w', newline='') as f:
        # different k values to test on
        for i in range(k_down, k_up):
            num_clusters = i
            # number of retries / simulations
            for j in range(simulations):
                # create a clustering solution and apply k-means
                clustering = Clustering(dimensions, num_clusters, patterns, 0.0001)
                clustering.k_means_clustering(iterations)
                # used to compute quality of the solution
                quality = ClusteringQuality(clustering, 0.0001)
                this_quality = 0.0
                if metric == 'qe':
                    this_quality = quality.quantization_error()
                if metric == 'si':
                    this_quality = quality.average_silhouette_index()
                if metric == 'db':
                    this_quality = quality.davies_bouldin()
                # update the best clustering
                if this_quality < best_quality:
                    best_quality = this_quality
                    best_clustering = clustering
                    print("Updated best clustering")
                # write result to the file
                result = [num_clusters, this_quality]
                for x in result:
                    f.write(str(x))
                    f.write(",")
                f.write("\n")
                f.flush()
                print(j, result)
        # print the actual clustering out to console
        best_clustering.print_solution(pattern_labels)


if __name__ == "__main__":
    # cProfile.run('forest_run()')
    # set the number of dimensions in the data
    dimensionality = 19
    # load the data into an object
    data = Data("D:\AirNode\Collaborations\PublicAuthority\Inter-Governmental\ECMWF\ESoWC\Challenge24_OutlierDetection_AirQuality\TechnicalStack\Implementations\Milestone_2\Example_Dataset\Final-Data-Set.csv")
    # get the patterns from the object (list of lists)
    pattern_labels = []
    patterns_data, pattern_labels = data.load_data()
    # specify the metric
    # qe = quantization error
    # si = silhouette index
    # db = davies-bouldin
    # forest_run(dimensionality, patterns_data)
    forest_run(dimensionality, patterns_data, pattern_labels, simulations=1000, k_down=6, k_up=9)
    # forest_run(dimensionality, patterns_data, metric='si')