#**Finding Lane Lines on the Road**

##Writeup

---

**Finding Lane Lines on the Road**

The goals / steps of this project are the following:
* Make a pipeline that finds lane lines on the road
* Reflect on your work in a written report


[//]: # (Image References)

[image1]: ./examples/grayscale.jpg "Grayscale"

---

### Reflection

###1. Describe your pipeline

First I copied the code from P1.ipynb to a new file P1.py to get a familiar python environment.

Then I added a new function `find_lane_lines(original_image)` that should contain all the pipeline code. I added code
step by step and checked the results against the single test images.

####1. Convert to grayscale & blur

It's not gray, but it has only one color value per pixel:

![grayscale](writeup/figure_1.png)

####2. Apply Canny

![canny](writeup/figure_2.png)

####3. Only use region of interest

Here I made a mistake which I only figured out later: I didn't reuse the last result:

![region](writeup/figure_3.png)

####4. Enlarge region of interest

I enlarged the region a little bit on the bottom right side:

![region larger](writeup/figure_4.png)

####5. Get Hough lines & get weighted image

Now I began to wonder: Why is Hough detecting my whole region as lines?

![hough lines](writeup/figure_5.png)

I printed the weighted image, but so far no improvement:

![hough lines weighted](writeup/figure_6.png)

####6. Fix mistake: variable unused

Then I used my unused variable and things started to look good!

![fix issue](writeup/figure_7.png)

####7. Smaller region of interest

I noticed that the horizon contains lines, which would be detected by the algorithm. So I fixed it by using a smaller
region of interest:

![horizon](writeup/figure_8.png)

Now I could backport the code to Jupyter Notebook and create the videos!

###2. Potential shortcomings of my current pipeline

TODO


###3. Possible improvements for my pipeline

TODO
