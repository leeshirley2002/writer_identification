import os
import numpy
import random
##kmeans in python
def get_distance_matrix(file_name):
    s = open(file_name).readlines()
    data_matrix = []
    for i in s:
        line_s = numpy.zeros(67)
        line = i.rstrip().split()[1:]
        for m in line:
            line_s[int(m.split(':')[0])-1] = float(m.split(':')[1])
        data_matrix.append(line_s)
    #print data_matrix[:2]
    data_matrix = numpy.array(data_matrix,dtype = numpy.float32)
    data_size = len(data_matrix[:,0])
    distance_matrix = numpy.zeros([data_size,data_size],dtype = numpy.float32)
    for x in range(0,data_size):
        for y in range(0,x+1):
            a1 = (data_matrix[x]-data_matrix[y])**2
            distance = a1.sum()**0.5
            distance_matrix[x][y] = distance
            distance_matrix[y][x] = distance
    return distance_matrix

def kmeans(distance_matrix,num_cluster):
    d = distance_matrix
    data_size = len(d[0])
    data_index = numpy.arange(data_size)
    #initialize cluster center
    cluster_center = random.sample(data_index,num_cluster)
    for i in range(1,10):
        cluster_dict = {}
        for cluster in range(num_cluster):
            cluster_dict[cluster] = []
        for point in data_index:
            dist_between_centers = [d[center][point] for center in cluster_center]
            min_dist = min(dist_between_centers)
            min_dist_index = dist_between_centers.index(min_dist)
            cluster_dict[min_dist_index].append(point)
        #calc new cluster center
        cluster_center = []
        aver_dist_all = []
        for key in cluster_dict:
            dist_sum_aver = []
            for point in cluster_dict[key]:
                point_dist_list = [d[point][i] for i in cluster_dict[key]]
                point_dist_sum = sum(point_dist_list)
                dist_sum_aver.append(point_dist_sum/len(cluster_dict[key]))
            new_min_dist = min(dist_sum_aver)
            new_min_dist_index = dist_sum_aver.index(new_min_dist)
            new_center = cluster_dict[key][new_min_dist_index]
            cluster_center.append(new_center)
            aver_dist_all.append(new_min_dist)
        print sum(aver_dist_all)
def main():
    dist_matrix = get_distance_matrix('D:\\xiaobai\\b.scale')
    kmeans(dist_matrix,5)
if __name__ == '__main__':
    main()
