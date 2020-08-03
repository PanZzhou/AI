import cv2
import time
import logging
#ID3算法和C4.5算法来进行特征选择
import numpy as np
import pandas as pd
import random

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

total_class = 10
cho_met='ID3'

def log(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        logging.debug('start %s()' % func.__name__)
        ret = func(*args, **kwargs)

        end_time = time.time()
        logging.debug('end %s(), cost %s seconds' % (func.__name__, end_time - start_time))

        return ret

    return wrapper


# 二值化
def binaryzation(img):
    cv_img = img.astype(np.uint8)
    cv2.threshold(cv_img, 50, 1, cv2.THRESH_BINARY, cv_img)
    return cv_img


@log
def binaryzation_features(trainset):
    features = []

    for img in trainset:
        img = np.reshape(img, (10, 10))
        cv_img = img.astype(np.uint8)

        img_b = binaryzation(cv_img)
        # hog_feature = np.transpose(hog_feature)
        features.append(img_b)

    features = np.array(features)
    features = np.reshape(features, (-1, 100))

    return features


class Tree(object):
    def __init__(self, node_type, Class=None, feature=None):
        self.node_type = node_type
        self.dict = {}
        self.Class = Class
        self.feature = feature

    def add_tree(self, val, tree):
        self.dict[val] = tree

    def predict(self, features):
        if self.node_type == 'leaf':
            return self.Class
        if (features[self.feature] in self.dict.keys()):
            tree = self.dict[features[self.feature]]
        else:
            if (self.Class is None):
                return random.randint(0, 1)
            else:
                return self.Class
        return tree.predict(features)


def calc_ent(x):
    """
        calculate empirical entropy of x
    """

    x_value_list = set([x[i] for i in range(x.shape[0])])#x.shape[0]得出矩阵x有多少行
    ent = 0.0
    for x_value in x_value_list:
        p = float(x[x == x_value].shape[0]) / x.shape[0]
        logp = np.log2(p)
        ent -= p * logp

    return ent


def calc_condition_ent(train_feature, train_label):
    """
        calculate empirical entropy H(y|x)
    """

    # calc ent(y|x)

    ent = 0
    train_feature_set = set(train_feature)
    # print("train_feature_set", train_feature_set)
    for train_feature_value in train_feature_set:
        Di = train_feature[train_feature == train_feature_value]
        label_i = train_label[train_feature == train_feature_value]
        # print("Di", Di)
        train_label_set = set(train_label)
        temp = 0
        # print("train_label_set", train_label_set)
        for train_label_value in train_label_set:
            Dik = Di[label_i == train_label_value]
            # print(Dik)
            if (len(Dik) != 0):
                p = float(len(Dik)) / len(Di)
                logp = np.log2(p)
                temp -= p * logp
        ent += float(len(Di)) / len(train_feature) * temp
    return ent


def recurse_train(train_set, train_label, features, epsilon):
    global total_class

    LEAF = 'leaf'
    INTERNAL = 'internal'

    # 步骤1——如果train_set中的所有实例都属于同一类Ck
    label_set = set(train_label)
    # print(label_set)
    if len(label_set) == 1:
        return Tree(LEAF, Class=label_set.pop())

    # 步骤2——如果features为空

    class_count0 = 0
    class_count1 = 0

    for i in range(len(train_label)):
        if (train_label[i] == 1):
            class_count1 += 1
        else:
            class_count0 += 1

    if (class_count0 >= class_count1):
        max_class = 0
    else:
        max_class = 1

    if features is None:
        return Tree(LEAF, Class=max_class)

    if len(features) == 0:
        return Tree(LEAF, Class=max_class)

    # 步骤3——计算信息增益
    max_feature = 0
    max_gda = 0

    D = train_label
    HD = calc_ent(D)
    for feature in features:
        A = np.array(train_set[:, feature].flat)
        gda = HD - calc_condition_ent(A, D)

        max_gda,max_feature=feature_choose(gda,feature,max_gda,max_feature,HD)

    # 步骤4——小于阈值
    if max_gda < epsilon:
        return Tree(LEAF, Class=max_class)

    # 步骤5——构建非空子集
    sub_features = features.remove(max_feature)
    tree = Tree(INTERNAL, feature=max_feature)

    feature_col = np.array(train_set[:, max_feature].flat)
    feature_value_list = set([feature_col[i] for i in range(feature_col.shape[0])])
    for feature_value in feature_value_list:

        index = []
        for i in range(len(train_label)):
            if train_set[i][max_feature] == feature_value:
                index.append(i)

        sub_train_set = train_set[index]
        sub_train_label = train_label[index]

        sub_tree = recurse_train(sub_train_set, sub_train_label, sub_features, epsilon)
        tree.add_tree(feature_value, sub_tree)

    return tree

def feature_choose(new_gda,new_feature,chosen_grda,chosen_feature,HD):
    if cho_met=='ID3':
        return ID3_choose(new_gda,new_feature,chosen_grda,chosen_feature)
    else:
        return C45_choose(new_gda,new_feature,chosen_grda,chosen_feature,HD)

#使用ID3算法标准来进行特征选择（选择信息增益最大的特征）
def ID3_choose(new_gda,new_feature,chosen_gda,chosen_feature):
    if new_gda > chosen_gda:
        return new_gda, new_feature
    else:
        return chosen_gda,chosen_feature

#使用C4.5算法来进行特征选择（选择信息增益率最大的特征）
def C45_choose(new_gda,new_feature,chosen_grda,chosen_feature,HD):
    #HA=calc_ent(A)
    #if HA==0:
        #return chosen_grda,chosen_feature
    #grda=new_gda/HA
    grda=new_gda/HD
    if grda>chosen_grda:
        return grda,new_feature
    else:
        return chosen_grda,chosen_feature


@log
def train(train_set, train_label, features, epsilon):
    # print(features)
    return recurse_train(train_set, train_label, features, epsilon)


@log
def predict(test_set, tree):
    result = []
    for features in test_set:
        tmp_predict = tree.predict(features)
        result.append(tmp_predict)
    return np.array(result)


if __name__ == '__main__':
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    raw_data = pd.read_csv('./data/train_binary1.csv', header=0)
    data = raw_data.values

    images = data[0:, 1:]
    labels = data[:, 0]
    # 图片二值化
    features = binaryzation_features(images)

    # 选取 2/3 数据作为训练集， 1/3 数据作为测试集
    train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size=0.33,random_state=1)

    logging.debug("############特征选择算法是{0}算法#############".format(cho_met))
    # print(train_features.shape)
    print(train_features.shape)
    print(train_labels.shape)
    tree = train(train_features, train_labels, [i for i in range(100)], 0.1)
    test_predict = predict(test_features, tree)
    # print(test_predict)
    score = accuracy_score(test_labels, test_predict)

    print("The accuracy score is ", score)

    cho_met="C4.5"
    logging.debug("###########特征选择算法是{0}算法############".format(cho_met))
    tree = train(train_features, train_labels, [i for i in range(100)], 0.1)
    test_predict = predict(test_features, tree)
    score = accuracy_score(test_labels, test_predict)

    print("The accuracy score is ", score)