from __future__ import print_function
import numpy as np


# Mask col. Get col vector. Roll by amount.
# Reapply.
def rot_col(rect, x, v):
    vec = np.copy(rect[:, x])
    new_rect = np.copy(rect)
    new_rect[:, x] = 0.
    vec = np.roll(vec, v)
    new_rect[:, x] = vec
    return new_rect


# Copy array. Roll in rows.
# Mask back original row.
# Add in new rect.
def rot_row(rect, y, v):
    row_mask = np.ones(rect.shape[0], dtype=np.bool)
    row_mask[y] = 0

    shift = np.copy(rect)
    preserve = np.copy(rect)

    preserve[~row_mask, :] = 0
    shift[row_mask, :] = 0

    shifted = np.roll(shift, v)

    return np.logical_or(shifted, preserve)


def make_rect(r=6, c=50):
    return np.zeros((r, c))


def mask_ab(rect, a, b):
    mask = np.ones((b, a))

    new_rect = np.copy(rect)
    new_rect[0:b, 0:a] = mask

    return new_rect


def print_rect(rect):
    for row in rect:
        for entry in row:
            if entry == 1:
                print('#', end='')
            else:
                print('.', end='')
        print()


if __name__ == '__main__':
    rect = make_rect(3, 7)
    rect = mask_ab(rect, 3, 2)
    rect = rot_col(rect, 1, 1)
    rect = rot_row(rect, 0, 4)
    rect = rot_col(rect, 1, 1)
    print_rect(rect)
    print(np.sum(rect))
