#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import itertools
import os.path


def cartesian_product(dicts):
    return (dict(zip(dicts, x)) for x in itertools.product(*dicts.values()))


def summary(configuration):
    kvs = sorted([(k, v) for k, v in configuration.items()], key=lambda e: e[0])
    return '_'.join([('%s=%s' % (k, v)) for (k, v) in kvs])


def to_command(c):
    command = "PYTHONPATH=. ./bin/hyper-cli.py" \
              " --train data/yago3/yago3-train.txt" \
              " --valid data/yago3/yago3-valid.txt" \
              " --test data/yago3/yago3-test.txt" \
              " --epochs %s" \
              " --optimizer %s" \
              " --lr %s" \
              " --batches %s" \
              " --model %s" \
              " --similarity %s" \
              " --margin %s" \
              " --entity-embedding-size %s --predicate-embedding-size %s"\
              % (c['epochs'], c['optimizer'], c['lr'], c['batches'],
                 c['model'], c['similarity'], c['margin'],
                 c['embedding_size'], c['embedding_size'])
    return command


def to_logfile(c):
    outfile = "logs/exp_yago3_v1/exp_yago3_v1." + summary(c) + ".log"
    return outfile


hyperparameters_space = dict(
    epochs=[500],
    optimizer=['adagrad'],
    lr=[.01, .1],
    batches=[10],
    model=['TransE', 'ScalE'],
    similarity=['l1', 'l2', 'dot'],
    margin=[0, 1, 2, 5, 10],
    embedding_size=[20, 50, 100, 200, 300, 400])

configurations = cartesian_product(hyperparameters_space)

for c in configurations:
    logfile = to_logfile(c)

    completed = False
    if os.path.isfile(logfile):
        with open(logfile, 'r') as f:
            content = f.read()
            completed = '### MICRO (test filtered)' in content

    if not completed:
        line = '%s >> %s 2>&1' % (to_command(c), logfile)
        print(line)
