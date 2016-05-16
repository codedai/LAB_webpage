import mxnet as mx
import numpy as np
import sys,os
from mxnet.io import DataIter
from PIL import Image

class NpyIter(DataIter):
    """NpyIter object in the fcn-xs example. Taking a file list file to get DataIter
    in this example, we use the whole image training for fcn-xs, that is to say
    we do not need resize/crop the image to the same size, so the batch_size is
    set to 1 here
    Parameters
    ----------
    root_dir : string
        the root dir of image/label lie in
    flist_name : string
        the list file of image and label, every line owns the form:
        index \t image_label_path \t image_data_path
    cut_off_size : int
        if the maximal size of one image is larger than cut_off_size, then it will
        crop the image with the minimal size of that iamge
    data_name : string
        the data name used in symbol data(default data name)
    label_name : string
        the label name used in symbol softmax_label(default label name)
    """
    def __init__(self, root_dir, flist_name,
                 batch_size = 1,
                 rgb_mean=(0,0,0),
                 data_name = "data",
                 label_name = "softmax_label"):
        super(NpyIter, self).__init__()
        self.root_dir = root_dir
        self.flist_name = os.path.join(self.root_dir, flist_name)
        self.mean = np.array(rgb_mean)
        self.data_name = data_name
        self.label_name = label_name
        self.batch_size = batch_size

        self.num_data = len(open(self.flist_name,'r').readlines())
        self.f = open(self.flist_name,'r')
        # self.data =  np.zeros((self.batch_size,361))
        # self.label =  np.zeros((self.batch_size,361))
        # self.data, self.label = self._read()
        self.cursor = 0

    def _read(self):
        """get two list, each list contains two elements: name and nd.array value"""
        _, data_img_name, label_img_name = self.f.readline().strip('\n').split("\t")
        data = {}
        label = {}
        data[self.data_name], label[self.label_name] = self._read_img(data_img_name, label_img_name)
        return list(data.items()), list(label.items())

    def _read_img(self, img_name, label_name):
        img = np.load(os.path.join(self.root_dir, img_name))
        label = np.load(os.path.join(self.root_dir, label_name))
        img = img.reshape((361,))
        label = label.reshape((361,))
        # assert img.size = label.size
        # img = np.array(img, dtype=np.float32)
        # label = np.array(label)
        #
        # reshaped_mean = self.mean.reshape(1,1,3)
        # img = img - reshaped_mean
        # img = np.swapaxes(img, 0, 2)
        # img = np.swapaxes(img, 1, 2)
        # img = np.expand_dims(img, axis=0)
        # label = np.array(label)
        # label = np.expand_dims(label, axis=0)
        return (img, label)

    @property
    def provide_data(self):
        """The name and shape of data provided by this iterator"""
        # import pdb; pdb.set_trace()
        # for k, v in self.data:
        #     print k,v
        return [(k, tuple([1] + list(v.shape[1:]))) for k, v in self.data]

    @property
    def provide_label(self):
        """The name and shape of label provided by this iterator"""
        return [(k, tuple([1] + list(v.shape[1:]))) for k, v in self.label]

    def get_batch_size(self):
        return 1

    def reset(self):
        self.cursor = -1
        self.f.close()
        self.f = open(self.flist_name, 'r')

    def iter_next(self):
        if(self.cursor < self.num_data):
            # print self.cursor,self.num_data
            # print "not in true"
            return True
        else:
            # print "end of file"
            return False

    def next(self):
        """return one dict which contains "data" and "label" """
        # print(self.cursor)
        # print(self.num_data)
        if self.iter_next():
            if (self.cursor + self.batch_size) <= self.num_data:
                # print ('---------小于-----------')
                self.data = np.zeros((self.batch_size, 361))
                self.label = np.zeros((self.batch_size, 361))
                self.dataBatch = np.zeros((self.batch_size, 361))
                self.labelBatch = np.zeros((self.batch_size, 361))
                # self.data, self.label = self._read()
                for i in range(self.batch_size):
                    self.dataBatch, self.labelBatch = self._read()
                    self.cursor += 1
                    # print self.cursor, self.num_data
                    self.data[i,:] = self.dataBatch[0][1]
                    self.label[i,:] = self.labelBatch[0][1]
                    # print (self.data)
                return {self.data_name  : self.data,
                        self.label_name : self.label}
            else:
                # print('-----------不小于-----------')
                sizex = self.num_data - self.cursor
                self.data = np.zeros((sizex,361))
                self.label = np.zeros((sizex,361))
                self.dataBatch = np.zeros((sizex,361))
                self.labelBatch = np.zeros((sizex,361))
                # print(sizex)
                # print(self.cursor)
                for i in range(sizex):
                    # print(self.cursor)
                    self.dataBatch,self.labelBatch = self._read()
                    self.cursor += 1
                    self.data[i,:] = self.dataBatch[0][1]
                    self.label[i,:] = self.labelBatch[0][1]
                return {self.data_name  : self.data,
                        self.label_name : self.label}
        else:
            return StopIteration
