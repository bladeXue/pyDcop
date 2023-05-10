#!/usr/bin/python3
# BSD-3-Clause License
#
# Copyright 2017 Orange
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import numpy as np

def branin(x1: float, x2: float) -> float:
    """Returns the value of the Branin-Hoo function

    Implementation of the Branin-Hoo function
    https://www.sfu.ca/~ssurjano/branin.html

    Three global minima
    f(x*) = 0.397887
    x* = (-pi, 12.275), (pi, 2.275), (9.42478, 2.475)

    x1 = [-5, 10]
    x2 = [0, 15]
    """
    # Set the parameters
    # a = 1.
    # b = 5.1 / (4. * np.pi**2)
    # c = 5. / np.pi
    # r = 6.
    # s = 10.
    # t = 1. / (8. * np.pi)

   

    # Calculate the value
    # f = a*(x2 - b*x1**2 + c*x1 - r)**2 + s*(1. - t)*np.cos(x1) + s
    f = 5*x1**2+ 2*x1+ -4*x1*x2+ -5*x2+ -5*x2**2

    return f
