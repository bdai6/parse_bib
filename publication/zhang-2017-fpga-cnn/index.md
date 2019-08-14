---
title: "Improving the Performance of OpenCL-based FPGA Accelerator for Convolutional Neural Network"
authors: ["Jialiang Zhang","Jing Li"]
date: 2017-01-01
doi: "10.1145/3020078.3021698"
publication_types: ["1"]
publication: "_Proceedings of the 2017 ACM/SIGDA International Symposium on Field-Programmable Gate Arrays_"
publication_short: ""
abstract: "OpenCL FPGA has recently gained great popularity with emerging needs for workload acceleration such as Convolutional Neural Network (CNN), which is the most popular deep learning architecture in the domain of computer vision. While OpenCL enhances the code portability and programmability of FPGA, it comes at the expense of performance. The key challenge is to optimize the OpenCL kernels to efficiently utilize the flexible hardware resources in FPGA. Simply optimizing the OpenCL kernel code through various compiler options turns out insufficient to achieve desirable performance for both compute-intensive and data-intensive workloads such as convolutional neural networks.  In this paper, we first propose an analytical performance model and apply it to perform an in-depth analysis on the resource requirement of CNN classifier kernels and available resources on modern FPGAs. We identify that the key performance bottleneck is the on-chip memory bandwidth. We propose a new kernel design to effectively address such bandwidth limitation and to provide an optimal balance between computation, on-chip, and off-chip memory access. As a case study, we further apply these techniques to design a CNN accelerator based on the VGG model. Finally, we evaluate the performance of our CNN accelerator using an Altera Arria 10 GX1150 board. We achieve 866 Gop/s floating point performance at 370MHz working frequency and 1.79 Top/s 16-bit fixed-point performance at 385MHz. To the best of our knowledge, our implementation achieves the best power efficiency and performance density compared to existing work."
summary: ""
tags: ["conference"," convolutional neural networks"," fpga"," hardware accelerator"," opencl"]
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

(Acceptance Rate: underline25%, 25 out of 101)
