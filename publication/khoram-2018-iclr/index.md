---
title: "Adaptive Quantization of Neural Networks"
authors: ["Soroosh Khoram","Jing Li"]
date: 2018-04-01
publication_types: ["1"]
publication: "_International Conference on Learning Representations (textbfICLR)_"
publication_short: ""
abstract: "Despite the state-of-the-art accuracy of Deep Neural Networks (DNN) in various classification problems, their deployment onto resource constrained edge computing devices remains challenging due to their large size and complexity. Several recent studies have reported remarkable results in reducing this complexity through quantization of DNN models. However, these studies usually do not consider the changes in the loss function when performing quantization, nor do they take the different importances of DNN model parameters to the accuracy into account. We address these issues in this paper by proposing a new method, called adaptive quantization, which simplifies a trained DNN model by finding a unique, optimal precision for each network parameter such that the increase in loss is minimized. The optimization problem at the core of this method iteratively uses the loss function gradient to determine an error margin for each parameter and assigns it a precision accordingly. Since this problem uses linear functions, it is computationally cheap and, as we will show, has a closed-form approximate solution. Experiments on MNIST, CIFAR, and SVHN datasets showed that the proposed method can achieve near or better than state-of-the-art reduction in model size with similar error rates. Furthermore, it can achieve compressions close to floating-point model compression methods without loss of accuracy."
summary: ""
tags: ["conference"]
categories: []
featured: false

url_pdf:
url_code:
url_dataset:
url_poster:
url_project:
url_slides:
url_source:
url_video:

image:
  caption: ""
  focal_point: ""
  preview_only: false

projects: []

slides: ""
---

(Acceptance Rate: underline34%, 314 out of 935)
