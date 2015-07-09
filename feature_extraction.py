import os
import numpy
import math

class FeatureExaction:
    def __init__(self, file_name, calc_statical_feature = True, calc_direct_feature = True):
        self.file_name = file_name
        if '\\' in file_name:
            self.name = file_name.split('\\')[-1].split('.')[0]
        else:
            self.name = file_name.split('.')[0]
        self.origin_data = self.parse_file()
        self.calc_statical_feature = calc_statical_feature
        self.calc_direct_feature = calc_direct_feature
        if calc_statical_feature == True:
            self.statical_feature = self.calcStatFeature()
        if calc_direct_feature == True:
            self.direct_feature = self.calcDirectFeature()
            
    def parse_file(self):
        try:
            f = open(self.file_name)
        except:
            print ('FILE NOT FOUND')
        data_array = []
        while 1:
            s = f.readline()
            if not s:break
            line = s.rstrip().split()
            data_array.append([int(line[0]),int(line[2]),int(line[1])])
        return data_array
    
    def calcStatFeature(self):
        data = self._convertToMatrix()
        c = data[0:8,:]
        new_matrix = numpy.zeros([7,7])
        lenx = len(data[:,0])
        leny = len(data[0,:])
        lenx_part = lenx/7.0
        leny_part = leny/7.0
        for x in range(0,7):
            for y in range(0,7):
                
                new_matrix[x][y] = data[int(lenx_part*x):int(lenx_part*(x+1)),int(leny_part*y):int(leny_part*(y+1))].sum()
        return list(new_matrix.reshape([1,49])[0])
     
    def _convertToMatrix(self):
        data_array = numpy.array(self.origin_data)[:,1:]
        minx = data_array[:,0].min()
        maxx = data_array[:,0].max()
        miny = data_array[:,1].min()
        maxy = data_array[:,1].max()
        rangex = maxx - minx
        rangey = maxy - miny
        norm_data = numpy.zeros([rangex+3,rangey+3])
        for i in data_array:
            norm_data[i[0]-minx+1,i[1]-miny+1] = 1
        return norm_data
    
    def calcDirectFeature(self):
        line_cor = []
        angles_all = []
        for i in self.origin_data:
            if i[0] == 2:
                line_cor = []
                line_cor.append([i[1],i[2]])
            if i[0] == 0:
                line_cor.append([i[1],i[2]])
            if i[0] == 4:
                line_cor.append([i[1],i[2]])
                angles = self._calcAngle(line_cor)
                angles_all.extend(angles)
        an = 10
        angle_desc = numpy.zeros(18)    
        for i in angles_all:
            if i != 180:
                angle_desc[int(i/an)] += 1
            else:
                angle_desc[17] += 1
        return list(angle_desc)
             
    def _calcAngle(self,data):
        len_data = len(data)
        angle_list = []
        for i in range(0,len_data-2):
            point1 = data[i]
            point2 = data[i+1]
            point3 = data[i+2]
            v1 = [point1[0]-point2[0],point1[1]-point2[1]]
            v2 = [point3[0]-point2[0],point3[1]-point2[1]]
            try:
                angle = self._getAngle(v1,v2)
                angle_list.append(angle)
            except:
                print 1
        return angle_list
    
    def _getAngle(self,x,y):
        xy = x[0]*y[0]+x[1]*y[1]
        x2 = (x[0]**2+x[1]**2)**0.5
        y2 = (y[0]**2+y[1]**2)**0.5
        cosV = xy/(x2*y2)
        if cosV < -1.0:
            cosV = -1.0
        if cosV > 1.0:
            cosV = 1.0
        if cosV ==1.0:
            angle = 0
        else:
            angle = 180/(math.pi/math.acos(cosV))
        return angle
    
    def getDescLine(self):
        line = self.name + ' '
        out = []
        if self.calc_statical_feature == True:
            out.extend(self.statical_feature) 
        if self.calc_direct_feature == True:
            out.extend(self.direct_feature)
        out = [str(i) for i in out]
        line += ' '.join(out)
        return line
    
    def getLibsvmDescLine(self):
        line = self.name + ' '
        out = []
        if self.calc_statical_feature == True:
            out.extend(self.statical_feature) 
        if self.calc_direct_feature == True:
            out.extend(self.direct_feature)
        desc_list = ['%s:%s'%(i+1,str(out[i])) for i in range(len(out))]
        line += ' '.join(desc_list)
        return line
    
            
def main():
    a =FeatureExaction(r'D:\xiaobai\smooth_5_char_old\characterAtoZ\a\5_AARquery_06_96a.txt')
    a1 = os.listdir(r'D:\xiaobai\smooth_5_char_old\characterAtoZ_random\D1')
    fout = open('D1.desc','wb')
    for i in a1:
        f = FeatureExaction(r'D:\xiaobai\smooth_5_char_old\characterAtoZ_random\D1'+'\\'+i)
        fout.write('-1 '+' '.join(f.getLibsvmDescLine().split()[1:])+'\n')
    fout.close()
    
if __name__ == '__main__':
    main()
