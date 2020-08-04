# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 18:13:32 2020

@author: wegia
"""


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
    forest_run(dimensionality, patterns_data, pattern_labels, simulations=1, k_down=8, k_up=9)
    # forest_run(dimensionality, patterns_data, metric='si')