'''
this script detects face roi, and can merge the processed face back to the original frame.
'''

import dlib
import cv2
import numpy as np
import torch


class faceROI(object):
    def __init__(self):
        super(faceROI, self).__init__()
        self.detector = dlib.get_frontal_face_detector()

    def _resize_rectangle(self, d, ratio):
        center = d.center()
        width = d.width()
        height = d.height()
        width2 = int(width*ratio)
        height2 = int(height*ratio)
        left = int(center.x - width2/2)
        right = int(center.x + width2/2)
        top = int(center.y-height2/2)
        bottom = int(center.y+height2/2)
        d2 = dlib.rectangle(left, top, right, bottom)
        return d2

    def detect(self, image, face_size=448):
        '''
        extract face ROI of a image
        :param image: a RGB numpy array, which is a 8-bit image
        :return:
        '''
        roi = self.detector(image)
        faces = []
        roi_ = []
        for i, d in enumerate(roi):
            d = self._resize_rectangle(d, 2)
            roi_ += [d]
            face_now = image[d.top():d.bottom(), d.left():d.right(), :]
            face_now = cv2.resize(face_now, (face_size, face_size))
            faces += [face_now]
        return faces, roi_

    def fuse(self, image, roi, faces, if_face_residual=False):
        '''
        fuse the processed faces back to the image
        :param image:
        :param roi: the roi generated by self.detector()
        :param faces: the processed face image. they might have been processed.
        :pram if_face_residual: indicate whether the processed face is a residual one. if true, then the "faces"
        added to corresponding roi region of the the image; otherwise, then we cover it rather than replace it
        :return: the fused image
        '''
        for d, f in zip(roi, faces):
            shape = (d.bottom() - d.top(), d.right() - d.left())
            print(shape)
            f_now = cv2.resize(f, shape)
            if if_face_residual:
                face_now = image[d.top():d.bottom(), d.left():d.right(), :]
                face_now += f_now
            else:
                face_now = f_now
            image[d.top():d.bottom(), d.left():d.right(), :] = face_now
        return image