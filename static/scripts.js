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
            // Show the toast notification
            var toastEl = document.getElementById("liveToast");
            var toast = new bootstrap.Toast(toastEl);
            toast.show();

            // Optionally, reload the page after a short delay if you want updated content
            setTimeout(() => window.location.reload(), 300);
          } else if (data.errors) {
            // Format error messages
            let errorMessage = "";
            Object.keys(data.errors).forEach((field) => {
              errorMessage += `${field}: ${data.errors[field].join(", ")}<br>`;
            });
            // Insert the error message into the error toast body
            document.querySelector("#errorToast .toast-body").innerHTML =
              errorMessage;
            // Show the error toast
            const errorToastEl = document.getElementById("errorToast");
            const errorToast = new bootstrap.Toast(errorToastEl);
            errorToast.show();
          }
        })
        .catch((error) => console.error("Error:", error));
    });
  });
});
