// Function to store employee_id in local storage
function storeEmployeeId(employeeId) {
    localStorage.setItem('employee_id', employeeId);
}

// Function to retrieve employee_id from local storage
function getEmployeeId() {
    return localStorage.getItem('employee_id');
}

// Function to clear employee_id from local storage
function clearEmployeeId() {
    localStorage.removeItem('employee_id');
}

// Example of clearing employee_id on logout
function logout() {
    clearEmployeeId();
    // Redirecting to employee login page
    window.location.href = '/employee-login/'; // Change the URL to your employee login page
}


// Example of clearing employee_id after a certain time (e.g., few hours)
function clearAfterFewHours() {
    const logoutTime = new Date().getTime() + (3 * 60 * 60 * 1000); // 3 hours
    setTimeout(() => {
        clearEmployeeId();
    }, logoutTime - new Date().getTime());
}
