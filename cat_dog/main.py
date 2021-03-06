#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

File Name : main.py
File Description : This is the file where we do the training, testing, validating job
Author : Liangwei Li

"""
import torch as t

from util.Trainer import Trainer
from models.ResNet34 import ResNet34
from data_related.load_data import training_all, dev_all
from config import Configuration
cf = Configuration()
from util.tools import check_previous_models


def train(model, train_data):
    """
    Train method: train the model
    :param model: which model to use
    :param train_data: define the training data
    :return:
    """
    criterion = t.nn.CrossEntropyLoss()
    optimizer = t.optim.Adam(model.parameters(), lr=cf.learning_rate, weight_decay=cf.weight_decay)
    trainer = Trainer(model=model, criterion=criterion, optimizer=optimizer, dataset=dataset, val_dataset=dev_all)
    trainer.run()


def evaluate(model, eval_data):
    """
    Evaluate the model, this method will be called during the training processing at every epoch.
    :param model:  define which model to be evaluated.
    :param eval_data:  define the evaluating data to be used.
    :return:
    """
    model.eval()
    cnt = 0
    total = len(eval_data)
    for idx, data in enumerate(eval_data):
        input, label = data
        input = t.autograd.Variable(input)
        label = t.autograd.Variable(label)
        output = t.argmax(model(input), dim=1)
        if output == label:
            cnt += 1
            accuracy = cnt / (idx + 1)
            print('{cnt} pictures were correctly classified(Total number of pictures is {total})!\nCurrent accuracy is '
                  '{acc}'.format(cnt=cnt, total=total, acc=accuracy))
    print('Final accuracy is {acc}'.format(acc=accuracy))
    model.train()
    return accuracy


if __name__ == '__main__':
    model = ResNet34(in_channels=3, out_classes=cf.num_classes)
    model_flag = check_previous_models()                       # check if there exist previous models
    if model_flag != None:
        model.load(model_flag)                                 # if true, it will let the the user to choose whether to use previous model
    # train(model, training_all)
    evaluate(model, dev_all)