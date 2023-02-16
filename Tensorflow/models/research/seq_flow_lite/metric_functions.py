# Copyright 2020 The TensorFlow Authors All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
# Lint as: python3
"""Metric functions."""
import tensorflow.compat.v1 as tf


def classification_metric(per_example_loss, label_ids, logits):
  """Compute eval metrics."""
  return {
      "accuracy":
          tf.metrics.accuracy(label_ids, tf.math.argmax(logits, axis=-1)),
      "eval_loss":
          tf.metrics.mean(per_example_loss)
  }


THRESHOLDS = [0.5]


def labeling_metric(per_example_loss, label_ids, logits):
  """Compute eval metrics."""
  scores = tf.math.sigmoid(logits)
  num_classes = label_ids.get_shape().as_list()[-1]
  return_dict = {"eval_loss": tf.metrics.mean(per_example_loss)}
  for idx in range(num_classes):
    return_dict["auc/" + str(idx)] = tf.metrics.auc(label_ids[:, idx],
                                                    scores[:, idx])
    return_dict["precision@" + str(THRESHOLDS) + "/" +
                str(idx)] = tf.metrics.precision_at_thresholds(
                    label_ids[:, idx], scores[:, idx], thresholds=THRESHOLDS)
    return_dict["recall@" + str(THRESHOLDS) + "/" +
                str(idx)] = tf.metrics.recall_at_thresholds(
                    label_ids[:, idx], scores[:, idx], thresholds=THRESHOLDS)
  return return_dict
