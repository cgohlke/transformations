Homogeneous Transformation Matrices and Quaternions
===================================================

Transformations is a Python library for calculating 4x4 matrices for
translating, rotating, reflecting, scaling, shearing, projecting,
orthogonalizing, and superimposing arrays of 3D homogeneous coordinates
as well as for converting between rotation matrices, Euler angles,
and quaternions. Also includes an Arcball control object and
functions to decompose transformation matrices.

:Author: `Christoph Gohlke <https://www.cgohlke.com>`_
:License: BSD 3-Clause
:Version: 2022.9.26

Requirements
------------

This release has been tested with the following requirements and dependencies
(other versions may work):

- `CPython 3.8.10, 3.9.13, 3.10.7, 3.11.0rc2 <https://www.python.org>`_
- `NumPy 1.22.4 <https://pypi.org/project/numpy/>`_

Revisions
---------

2022.9.26

- Add dimension check on superimposition_matrix (#2).

2022.8.26

- Update metadata
- Remove support for Python 3.7 (NEP 29).

2021.6.6

- Remove support for Python 3.6 (NEP 29).

2020.1.1

- Remove support for Python 2.7 and 3.5.

2019.4.22

- Fix setup requirements.

Notes
-----

Transformations.py is no longer actively developed and has a few known issues
and numerical instabilities. The module is mostly superseded by other modules
for 3D transformations and quaternions:

- `Scipy.spatial.transform <https://github.com/scipy/scipy/tree/master/
  scipy/spatial/transform>`_
- `Transforms3d <https://github.com/matthew-brett/transforms3d>`_
  (includes most code of this module)
- `Pytransform3d <https://github.com/rock-learning/pytransform3d>`_
- `Numpy-quaternion <https://github.com/moble/quaternion>`_
- `Blender.mathutils <https://docs.blender.org/api/master/mathutils.html>`_

The API is not stable yet and is expected to change between revisions.

This Python code is not optimized for speed. Refer to the transformations.c
module for a faster implementation of some functions.

Documentation in HTML format can be generated with epydoc.

Matrices (M) can be inverted using numpy.linalg.inv(M), be concatenated using
numpy.dot(M0, M1), or transform homogeneous coordinate arrays (v) using
numpy.dot(M, v) for shape (4, -1) column vectors, respectively
numpy.dot(v, M.T) for shape (-1, 4) row vectors ("array of points").

This module follows the "column vectors on the right" and "row major storage"
(C contiguous) conventions. The translation components are in the right column
of the transformation matrix, i.e. M[:3, 3].
The transpose of the transformation matrices may have to be used to interface
with other graphics systems, e.g. OpenGL's glMultMatrixd(). See also [16].

Calculations are carried out with numpy.float64 precision.

Vector, point, quaternion, and matrix function arguments are expected to be
"array like", i.e. tuple, list, or numpy arrays.

Return types are numpy arrays unless specified otherwise.

Angles are in radians unless specified otherwise.

Quaternions w+ix+jy+kz are represented as [w, x, y, z].

A triple of Euler angles can be applied/interpreted in 24 ways, which can
be specified using a 4 character string or encoded 4-tuple:

  *Axes 4-string*: e.g. 'sxyz' or 'ryxy'

  - first character : rotations are applied to 's'tatic or 'r'otating frame
  - remaining characters : successive rotation axis 'x', 'y', or 'z'

  *Axes 4-tuple*: e.g. (0, 0, 0, 0) or (1, 1, 1, 1)

  - inner axis: code of axis ('x':0, 'y':1, 'z':2) of rightmost matrix.
  - parity : even (0) if inner axis 'x' is followed by 'y', 'y' is followed
    by 'z', or 'z' is followed by 'x'. Otherwise odd (1).
  - repetition : first and last axis are same (1) or different (0).
  - frame : rotations are applied to static (0) or rotating (1) frame.

References
----------

1.  Matrices and transformations. Ronald Goldman.
    In "Graphics Gems I", pp 472-475. Morgan Kaufmann, 1990.
2.  More matrices and transformations: shear and pseudo-perspective.
    Ronald Goldman. In "Graphics Gems II", pp 320-323. Morgan Kaufmann, 1991.
3.  Decomposing a matrix into simple transformations. Spencer Thomas.
    In "Graphics Gems II", pp 320-323. Morgan Kaufmann, 1991.
4.  Recovering the data from the transformation matrix. Ronald Goldman.
    In "Graphics Gems II", pp 324-331. Morgan Kaufmann, 1991.
5.  Euler angle conversion. Ken Shoemake.
    In "Graphics Gems IV", pp 222-229. Morgan Kaufmann, 1994.
6.  Arcball rotation control. Ken Shoemake.
    In "Graphics Gems IV", pp 175-192. Morgan Kaufmann, 1994.
7.  Representing attitude: Euler angles, unit quaternions, and rotation
    vectors. James Diebel. 2006.
8.  A discussion of the solution for the best rotation to relate two sets
    of vectors. W Kabsch. Acta Cryst. 1978. A34, 827-828.
9.  Closed-form solution of absolute orientation using unit quaternions.
    BKP Horn. J Opt Soc Am A. 1987. 4(4):629-642.
10. Quaternions. Ken Shoemake.
    http://www.sfu.ca/~jwa3/cmpt461/files/quatut.pdf
11. From quaternion to matrix and back. JMP van Waveren. 2005.
    http://www.intel.com/cd/ids/developer/asmo-na/eng/293748.htm
12. Uniform random rotations. Ken Shoemake.
    In "Graphics Gems III", pp 124-132. Morgan Kaufmann, 1992.
13. Quaternion in molecular modeling. CFF Karney.
    J Mol Graph Mod, 25(5):595-604
14. New method for extracting the quaternion from a rotation matrix.
    Itzhack Y Bar-Itzhack, J Guid Contr Dynam. 2000. 23(6): 1085-1087.
15. Multiple View Geometry in Computer Vision. Hartley and Zissermann.
    Cambridge University Press; 2nd Ed. 2004. Chapter 4, Algorithm 4.7, p 130.
16. Column Vectors vs. Row Vectors.
    http://steve.hollasch.net/cgindex/math/matrix/column-vec.html

Examples
--------

>>> alpha, beta, gamma = 0.123, -1.234, 2.345
>>> origin, xaxis, yaxis, zaxis = [0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]
>>> I = identity_matrix()
>>> Rx = rotation_matrix(alpha, xaxis)
>>> Ry = rotation_matrix(beta, yaxis)
>>> Rz = rotation_matrix(gamma, zaxis)
>>> R = concatenate_matrices(Rx, Ry, Rz)
>>> euler = euler_from_matrix(R, 'rxyz')
>>> numpy.allclose([alpha, beta, gamma], euler)
True
>>> Re = euler_matrix(alpha, beta, gamma, 'rxyz')
>>> is_same_transform(R, Re)
True
>>> al, be, ga = euler_from_matrix(Re, 'rxyz')
>>> is_same_transform(Re, euler_matrix(al, be, ga, 'rxyz'))
True
>>> qx = quaternion_about_axis(alpha, xaxis)
>>> qy = quaternion_about_axis(beta, yaxis)
>>> qz = quaternion_about_axis(gamma, zaxis)
>>> q = quaternion_multiply(qx, qy)
>>> q = quaternion_multiply(q, qz)
>>> Rq = quaternion_matrix(q)
>>> is_same_transform(R, Rq)
True
>>> S = scale_matrix(1.23, origin)
>>> T = translation_matrix([1, 2, 3])
>>> Z = shear_matrix(beta, xaxis, origin, zaxis)
>>> R = random_rotation_matrix(numpy.random.rand(3))
>>> M = concatenate_matrices(T, R, Z, S)
>>> scale, shear, angles, trans, persp = decompose_matrix(M)
>>> numpy.allclose(scale, 1.23)
True
>>> numpy.allclose(trans, [1, 2, 3])
True
>>> numpy.allclose(shear, [0, math.tan(beta), 0])
True
>>> is_same_transform(R, euler_matrix(axes='sxyz', *angles))
True
>>> M1 = compose_matrix(scale, shear, angles, trans, persp)
>>> is_same_transform(M, M1)
True
>>> v0, v1 = random_vector(3), random_vector(3)
>>> M = rotation_matrix(angle_between_vectors(v0, v1), vector_product(v0, v1))
>>> v2 = numpy.dot(v0, M[:3,:3].T)
>>> numpy.allclose(unit_vector(v1), unit_vector(v2))
True
