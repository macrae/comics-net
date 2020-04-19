## Title
`comicsnet` pre-processing of covers

## Abstract
In a previous experiment (link), it was discovered that the comic book cover classifier
was overly reliant on non-pencil rendered features like the series title and the barcode.
In this experiment we will test the feasibility of applying a machine learner to remove
the barcode from an image in such a way that retains the style of the image.

## Introduction

## Materials and Methods
We will use synthetic training data, by first taking a collection of a couple thousand
comic book covers without barcodes, and copying and pasting a barcode in random places.
The augmented images containing the barcodes we copied and pasted will be used as X in our
training data set; the un-altered images will be used as y. The task is to predict the pixels
within the bounding box of the barcode.

## Results

## Discussion

## References