#!/usr/bin/python
#
# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import urllib2
import os.path
import numpy as np
import tensorflow as tf
from node_lookup import NodeLookup
from errors import error_result

snapshot_file = 'tmp/tmp.jpg'
model_dir = 'tmp/imagenet'
num_top_predictions = 5

def classify_remote_image(image_url):
    # Attempt to Download
    try:
        image = download_image(image_url)
    except IOError:
        return error_result("Camera's Snapshot URL could not be downloaded")

    # Attempt to Classify
    try:
        results = run_inference_on_image(image)
    except:
        return error_result("Could not classify the image")

    return {
        "image_url": image_url,
        "results": results
    }


def create_graph():
    with tf.gfile.FastGFile(os.path.join(
            model_dir, 'classify_image_graph_def.pb'
    ), 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')


def run_inference_on_image(image):
    """Runs inference on an image.

    Args:
      image: Image file name.

    Returns:
      Nothing
    """
    if not tf.gfile.Exists(image):
        tf.logging.fatal('File does not exist %s', image)
    image_data = tf.gfile.FastGFile(image, 'rb').read()

    # Creates graph from saved GraphDef.
    create_graph()

    with tf.Session() as sess:
        # Some useful tensors:
        # 'softmax:0': A tensor containing the normalized prediction across
        #   1000 labels.
        # 'pool_3:0': A tensor containing the next-to-last layer containing 2048
        #   float description of the image.
        # 'DecodeJpeg/contents:0': A tensor containing a string providing JPEG
        #   encoding of the image.
        # Runs the softmax tensor by feeding the image_data as input to the graph.
        softmax_tensor = sess.graph.get_tensor_by_name('softmax:0')
        predictions = sess.run(softmax_tensor,
                               {'DecodeJpeg/contents:0': image_data})
        predictions = np.squeeze(predictions)

        # Creates node ID --> English string lookup.
        node_lookup = NodeLookup()

        top_k = predictions.argsort()[-num_top_predictions:][::-1]
        results = {}
        for node_id in top_k:
            human_string = node_lookup.id_to_string(node_id)
            score = predictions[node_id]
            results[human_string] = float(score)
        return results

def download_image(url):
    # Downloads the image from the specified URL to the filesystem
    response = urllib2.urlopen(url)
    body = response.read()
    if body == '':
        raise IOError('The Snapshot URL did not contain any HTTP body when fetched')

    with open(snapshot_file, 'w') as f:
        f.write(body)

    return snapshot_file
