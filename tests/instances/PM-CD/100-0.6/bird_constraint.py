
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

def bird(x, y):
    """
    Function description in the following paper:
        @article{Mishra2006,
        author = {Mishra, Sudhanshu K},
        doi = {10.2139/ssrn.926132},
        issn = {1556-5068},
        journal = {SSRN Electronic Journal},
        title = {{Some New Test Functions for Global Optimization and Performance of Repulsive Particle Swarm Method}},
        url = {http://www.ssrn.com/abstract=926132},
        year = {2006}
        }

    Domain for x and y [-2pi, 2pi]
    Approximate optimum f(x*) = 106.764537

    Returns negative (normalized) value for maximization

    Property:
        Lipschitz_constant: 1326.5
    """
    value = np.sin(y) * np.exp((1.-np.cos(x))**2) + np.cos(x) * np.exp((1. - np.sin(y))**2) + (x - y)**2
    return -value

def bird_normalized_inputs(x, y):
    """Return the value of the bird function for normalized inputs"""
    x_normalized = (x * 4.0 * np.pi) - 2.0 * np.pi
    y_normalized = (y * 4.0 * np.pi) - 2.0 * np.pi
    return bird(x_normalized, y_normalized)