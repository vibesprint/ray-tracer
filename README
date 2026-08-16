# A Simple Ray Tracing Renderer in Python

## Introduction

This project I made following the book *The Ray Tracer Challenge* from the
*Pragmatic Programmer*. It's been some time since I stopped working on this
and now I am putting it on github. All the generated images are in
the `gallery` folder. The author also provided the scene data for
generating book cover using the renderer, which I generated and
can also be found in the `gallery` directory. It can be seen there's
some blackish dots in the generated image. That is due to floating
point calculation precision. Rather than doing a hard comparison
with 0 like `myvar == 0`, we will have to allow for some tolerance,
like if `math.abs(myvar - 0) < 0.001` then `myvar` is zero. That
is as far as I remember. I think I implemented this, but I am
not sure if it's there or not. If it's there, then those blackish
dots might be due to another reason.

## Performance

Initially I had written it in plain Python. Then when it was completed, I tried
to do some performance improvements. I looked into numpy for implementing
the linear algebra functions. But didn't do it because then I would have
had to change the base representation of vectors and that could have had
cascading changes throughout the codebase. I didn't write all the code again
so I didn't go this route. Then I looked jython and cython and maybe some
other runtimes also. I chose cython. But I just couldn't get it to work.
There were some problems occuring, I don't remember what. Ultimately
I gave up on it.

Anyways, finally I tried to improve performance by parallelizing the calculations
using Python multiprocessing library which spins up additional python
processes for parallelization. It wasn't a major improvement. Previously
it was taking around 13 minutes for a scene, then maybe after optimizing
it came to around 10 minutes.
