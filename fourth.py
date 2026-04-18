def simple_linear_regression(x, y):
    """
    Performs simple linear regression on a given dataset (x, y).
    Args:
        x (list): A list of independent variable values.
        y (list): A list of dependent variable values.
    Returns:
        tuple: A tuple containing the calculated slope (m) and y-intercept (b).
    """
    if not x or not y:
        raise ValueError("Input lists must not be empty.")
    n = len(x)
    if n != len(y):
        raise ValueError("Input lists for x and y must have the same length.")
    # Calculate the mean of x and y
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    # Numerator and denominator for slope (m)
    numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
    denominator = sum((x[i] - mean_x) ** 2 for i in range(n))

    # Handle the case where the denominator is zero to avoid division by zero error.
    if denominator == 0:
        return 0.0, mean_y  # Return a horizontal line through mean_y
    # Calculate the slope and y-intercept
    m = numerator / denominator
    b = mean_y - m * mean_x
    return m, b

def predict(x_new, m, b):
    """
    Predicts the value for a new data point using the linear regression model.
    Args:
        x_new (float or list): The new independent variable value(s).
        m (float): The slope of the regression line.
        b (float): The y-intercept of the regression line.
    Returns:
        float or list: The predicted y-value(s).
    """
    if isinstance(x_new, (int, float)):
        return m * x_new + b
    elif isinstance(x_new, list) or isinstance(x_new, tuple):
        return [m * float(val) + b for val in x_new]
    else:
        raise TypeError("Input 'x_new' must be a number or a list/tuple of numbers.")

def r_squared(x, y, m, b):
    """
    Calculates the R-squared value, which measures how well the model fits the data.
    R^2 = 1 - (SS_res / SS_tot)
    Args:
        x (list): Original x-values.
        y (list): Original y-values.
        m (float): The slope of the regression line.
        b (float): The y-intercept of the regression line.
    Returns:
        float: The R-squared value.
    """
    if not x or not y:
        raise ValueError("Input lists must not be empty.")
    n = len(x)
    if n != len(y):
        raise ValueError("Input lists for x and y must have the same length.")
    mean_y = sum(y) / n
    # Total sum of squares (SS_tot)
    ss_tot = sum((yi - mean_y) ** 2 for yi in y)
    # Residual sum of squares (SS_res)
    ss_res = sum((y[i] - predict(x[i], m, b)) ** 2 for i in range(n))
    # Handle division by zero
    if ss_tot == 0:
        return 1.0  # Perfect fit if all y values are the same
    r2 = 1 - (ss_res / ss_tot)
    return r2

# --- Example Usage ---
if __name__ == '__main__':
    # Sample dataset: years of experience (x) vs. salary (y) in thousands of dollars
    experience = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    salary = [30, 35, 45, 50, 60, 65, 75, 80, 90, 95]

    print("--- Simple Linear Regression Example ---")
    print(f"Original data points: \n\tExperience: {experience}\n\tSalary: {salary}\n")

    # Train the model
    slope, intercept = simple_linear_regression(experience, salary)

    print("Model trained successfully!")
    print(f"Calculated slope (m): {slope:.2f}")
    print(f"Calculated y-intercept (b): {intercept:.2f}")

    # Calculate and display the R-squared value
    r2_value = r_squared(experience, salary, slope, intercept)
    print(f"R-squared value: {r2_value:.4f} (A value close to 1 indicates a good fit)")

    # Make predictions for new data points
    new_experience = 11
    predicted_salary = predict(new_experience, slope, intercept)
    print(f"\nPrediction for {new_experience} years of experience: ${predicted_salary:.2f} thousand")

    new_experience_list = [12, 13, 14]
    predicted_salaries = predict(new_experience_list, slope, intercept)
    print(f"Predictions for multiple years ({new_experience_list}):")
    for exp, sal in zip(new_experience_list, predicted_salaries):
        print(f"\tExperience: {exp} years -> Predicted Salary: ${sal:.2f} thousand")