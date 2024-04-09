import numpy as np

def knee_pt(y, x=None, just_return=False):
    """
    Returns the x-location of a (single) knee of curve y=f(x).

    Parameters:
        y (array_like): Vector (>=3 elements).
        x (array_like, optional): Vector of the same size as y.
        just_return (bool, optional): If True, the function will not error out and simply return NaN on detected error conditions.

    Returns:
        res_x (float): x-location of the knee.
        idx_of_result (int): Index of the x-coordinate at the knee.

    Important:
        - The x and y don't need to be sorted, they just have to correspond.
        - Because of the way the function operates, y must be at least 3 elements long,
          and the function will never return either the first or the last point as the answer.

    Defaults:
        - If x is not specified or is empty, it's assumed to be 1:length(y), in this case, both returned values are the same.
        - If just_return is not specified or is empty, it's assumed to be False (i.e., the function will error out).
    """

    # Set internal operation flags
    use_absolute_dev_p = False  # or quadratic

    # Deal with issuing or not issuing errors
    issue_errors_p = True
    if just_return:
        issue_errors_p = False

    # Default answers
    res_x = np.nan
    idx_of_result = np.nan

    # Check y
    if y.size == 0:
        if issue_errors_p:
            raise ValueError('knee_pt: y cannot be an empty vector')
        return res_x, idx_of_result

    y = np.array(y).flatten()

    # Make or read x
    if x is None or x.size == 0:
        x = np.arange(1, len(y) + 1)
    else:
        x = np.array(x).flatten()

    # More checking
    if x.shape != y.shape:
        if issue_errors_p:
            raise ValueError('knee_pt: y and x must have the same dimensions')
        return res_x, idx_of_result

    # Check length of y
    if len(y) < 3:
        if issue_errors_p:
            raise ValueError('knee_pt: y must be at least 3 elements long')
        return res_x, idx_of_result

    # Sort x and y
    if not np.all(np.diff(x) >= 0):
        idx = np.argsort(x)
        y = y[idx]
        x = x[idx]
    else:
        idx = np.arange(len(x))

    # Calculate parameters for left-of-knee fit
    sigma_xy_fwd = np.cumsum(x * y)
    sigma_x_fwd = np.cumsum(x)
    sigma_y_fwd = np.cumsum(y)
    sigma_xx_fwd = np.cumsum(x * x)
    n = np.arange(1, len(y) + 1)
    det_fwd = n * sigma_xx_fwd - sigma_x_fwd * sigma_x_fwd
    mfwd = (n * sigma_xy_fwd - sigma_x_fwd * sigma_y_fwd) / det_fwd
    bfwd = -(sigma_x_fwd * sigma_xy_fwd - sigma_xx_fwd * sigma_y_fwd) / det_fwd

    # Calculate parameters for right-of-knee fit
    sigma_xy_bck = np.cumsum(x[::-1] * y[::-1])
    sigma_x_bck = np.cumsum(x[::-1])
    sigma_y_bck = np.cumsum(y[::-1])
    sigma_xx_bck = np.cumsum(x[::-1] * x[::-1])
    det_bck = n * sigma_xx_bck - sigma_x_bck * sigma_x_bck
    mbck = (n * sigma_xy_bck - sigma_x_bck * sigma_y_bck) / det_bck
    bbck = -(sigma_x_bck * sigma_xy_bck - sigma_xx_bck * sigma_y_bck) / det_bck

    # Calculate sum of per-point errors for left and right fits
    error_curve = np.full_like(y, np.nan)
    for breakpt in range(1, len(y) - 1):
        delsfwd = (mfwd[breakpt] * x[:breakpt] + bfwd[breakpt]) - y[:breakpt]
        delsbck = (mbck[breakpt] * x[breakpt:] + bbck[breakpt]) - y[breakpt:]
        if use_absolute_dev_p:
            error_curve[breakpt] = np.sum(np.abs(delsfwd)) + np.sum(np.abs(delsbck))
        else:
            error_curve[breakpt] = np.sqrt(np.sum(delsfwd ** 2)) + np.sqrt(np.sum(delsbck ** 2))

    # Find location of the min of the error curve
    loc = np.argmin(error_curve)
    res_x = x[loc]
    idx_of_result = idx[loc]

    return res_x, idx_of_result

# Test cases
if __name__ == "__main__":
    y_test = np.array([30, 27, 24, 21, 18, 15, 12, 10, 8, 6, 4, 2, 0])
    x_test = np.arange(1, len(y_test) + 1)

    res_x, idx_of_result = knee_pt(y_test)
    print("Expected Result: x = 7, idx = 6")
    print(f"Computed Result: x = {res_x}, idx = {idx_of_result}")

    res_x, idx_of_result = knee_pt(y_test[::-1])
    print("Expected Result: x = 7, idx = 6")
    print(f"Computed Result: x = {res_x}, idx = {idx_of_result}")

    res_x, idx_of_result = knee_pt(np.random.rand(3, 3))
    print("Expected Error: ValueError (y must be at least 3 elements long)")

    res_x, idx_of_result = knee_pt(np.random.rand(3, 3), just_return=False)
    print("Expected Error: ValueError (y must be at least 3 elements long)")

    res_x, idx_of_result = knee_pt(np.random.rand(3, 3), just_return=True)
    print("Expected Result: NaN")
    print(f"Computed Result: x = {res_x}, idx = {idx_of_result}")

    res_x, idx_of_result = knee_pt(y_test, np.arange(1, 14))
    print("Expected Result: x = 7, idx = 6")
    print(f"Computed Result: x = {res_x}, idx = {idx_of_result}")

    res_x, idx_of_result = knee_pt(y_test, np.arange(1, 14) * 20)
    print("Expected Result: x = 140, idx = 6")
    print(f"Computed Result: x = {res_x}, idx = {idx_of_result}")

    res_x, idx_of_result = knee_pt(y_test + np.random.rand(13) / 10, np.arange(1, 14) * 20)
    print("Expected Result: x = 140, idx = 6")
    print(f"Computed Result: x = {res_x}, idx = {idx_of_result}")

    res_x, idx_of_result = knee_pt(y_test + np.random.rand(13) / 10, np.arange(1, 14) * 20 + np.random.rand(13))
    print("Expected Result: Close to x = 140, idx = 6")
    print(f"Computed Result: x = {res_x}, idx = {idx_of_result}")

    x = np.arange(0, np.pi / 2, 0.01)
    y = np.sin(x)
    res_x, idx_of_result = knee_pt(y, x)
    print("Expected Result: Around x = 0.9, idx = Around 90")
    print(f"Computed Result: x = {res_x}, idx = {idx_of_result}")

    reorder = np.argsort(np.random.rand(len(x)))
    xr = x[reorder]
    yr = y[reorder]
    res_x, idx_of_result = knee_pt(yr, xr)
    print("Expected Result: Around x = 0.9, idx = Around 90")
    print(f"Computed Result: x = {res_x}, idx = {idx_of_result}")

    res_x, idx_of_result = knee_pt(np.arange(10, 0, -1))
    print("Expected Result: x = 2, idx = 1")
    print(f"Computed Result: x = {res_x}, idx = {idx_of_result}")
