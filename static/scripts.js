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
              errorMessage += `${field}: ${data.errors[field].join(', ')}`;
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
  // Add Option Button Functionality
  const addOptionBtn = document.getElementById('add-option-btn');
  if (addOptionBtn) { // Check if the button exists on the page
    addOptionBtn.addEventListener('click', function () {
      const optionsContainer = document.getElementById('options-container');
      const optionGroups = optionsContainer.querySelectorAll('.option-group');
      const lastOptionGroup = optionGroups[optionGroups.length - 1];

      if (!lastOptionGroup) {
        console.error("No option group to clone.");
        return; // Exit if no option group exists
      }

      const newOptionGroup = lastOptionGroup.cloneNode(true); // Deep clone

      // Clear input values in the new option group
      newOptionGroup.querySelectorAll('input[type="text"], textarea').forEach(input => {
        input.value = '';
      });
      newOptionGroup.querySelector('input[type="checkbox"]').checked = false; // Uncheck checkbox

      // Update option group heading number
      const heading = newOptionGroup.querySelector('h6');
      const nextOptionIndex = optionGroups.length + 1;
      if (heading) {
        heading.textContent = `Option ${nextOptionIndex}`;
      }

      // **Important: Update input names for FieldList indexing**
      newOptionGroup.querySelectorAll('input, textarea, select').forEach(input => {
        const name = input.getAttribute('name');
        if (name && name.startsWith('options-')) { // Assuming default FieldList prefix
          const parts = name.split('-');
          const fieldName = parts[2]; // text or is_correct
          input.setAttribute('name', `options-${nextOptionIndex - 1}-${fieldName}`); // Adjust index
          input.setAttribute('id', `options-${nextOptionIndex - 1}-${fieldName}`); // Update ID if needed for labels

          // Update label 'for' attribute if applicable
          const label = newOptionGroup.querySelector(`label[for="${parts.join('-')}"]`);
          if (label) {
            label.setAttribute('for', `options-${nextOptionIndex - 1}-${fieldName}`);
          }
        }
      });


      optionsContainer.appendChild(newOptionGroup);
    });
  }
});

function searchContentUser() {
  let input = document.getElementById("searchInput").value.toLowerCase();
  let quizCards = document.getElementsByClassName("quiz-card");

  for (let card of quizCards) {
    let title = card.querySelector(".fw-semibold").innerText.toLowerCase();
    if (title.includes(input)) {
      card.style.display = "";
    } else {
      card.style.display = "none";
    }
  }
}

