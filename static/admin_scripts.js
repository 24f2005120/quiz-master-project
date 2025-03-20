function updateModalFormAction(newAction, modalId, data = {}) {

  // Update form action
  const form = document.getElementById(modalId + "Form");
  if (!form) {
    console.error("Form not found!");
    return;
  }

  form.action = newAction;

  // Populate form fields
  Object.keys(data).forEach((key) => {
    let inputField = form.querySelector(`[name="${key}"]`); // Select field by name
    console.log("Updating Field:", key, "with Value:", data[key]);

    if (inputField) {
      if (data[key]) {
        inputField.value = data[key] || "";
      }
    } else {
      console.warn("Field not found:", key);
    }
  });
}

// Get the delete URLs dynamically

function handleDelete(url) {
  if (!confirm("Are you sure you want to delete this?")) return;

  fetch(url, { method: "DELETE" })
    .then((response) => response.json())
    .then((data) => {
      if (data.message) {
        showToast(data.message, "success");
        setTimeout(() => window.location.reload(), 300);
      } else if (data.errors) {
        showToast(data.errors, "error");
      }
    })
    .catch(() => showToast("Error deleting item", "danger"));
}
