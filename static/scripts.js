// notification function
function showToast(message, type = 'success') {
  // Get the correct toast element based on type
  const toastEl = type === 'success' ? document.getElementById('liveToast') : document.getElementById('errorToast');
  const toastBody = toastEl.querySelector('.toast-body');
  toastBody.textContent = message;

  // Optionally, add different classes based on the type (success/error)
  if (type === 'success') {
    toastEl.classList.remove('bg-danger');
    toastEl.classList.add('bg-success');
  } else {
    toastEl.classList.remove('bg-success');
    toastEl.classList.add('bg-danger');
  }

  // Show the toast
  const toast = new bootstrap.Toast(toastEl);
  toast.show();
}

// script for whenever someone submits a form
document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".modal form").forEach((form) => {
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      const formData = new FormData(form);
      const modalId = form.closest(".modal").id; // Get the modal ID dynamically

      fetch(form.action, {
        method: "POST",
        body: formData,
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.message) {
            // Show the success toast
            showToast(data.message, 'success');

            setTimeout(() => window.location.reload(), 300);
          } else if (data.errors) {
            // Format error messages
            let errorMessage = '';
            Object.keys(data.errors).forEach((field) => {
              errorMessage += `${field}: ${data.errors[field].join(', ')}<br>`;
            });

            // Show the error toast
            showToast(errorMessage, 'error');
          }
        })
        .catch((error) => {
          // Show the error toast for fetch failure
          showToast(`Error processing request. ${error}`, 'error');
        });
    });
  });
});
