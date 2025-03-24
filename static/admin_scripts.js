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

// admin search
function searchContent() {
  let input = document.getElementById("searchInput").value.toLowerCase();
  let subjects = document.querySelectorAll(".col");

  subjects.forEach((subject) => {
    let subjectName = subject.querySelector("h4").innerText.toLowerCase();
    let chapters = subject.querySelectorAll(".accordion-item");
    let subjectMatch = subjectName.includes(input);
    let chapterMatch = false;

    chapters.forEach((chapter) => {
      let chapterName = chapter.querySelector(".accordion-button strong").innerText.toLowerCase();
      let quizzes = chapter.querySelectorAll(".list-group-item");
      let chapterHasMatch = chapterName.includes(input);
      let quizMatch = false;

      quizzes.forEach((quiz) => {
        let quizName = quiz.querySelector("a").innerText.toLowerCase();
        if (quizName.includes(input)) {
          quiz.style.display = "";
          quizMatch = true;
        } else {
          quiz.style.display = "none";
        }
      });

      if (quizMatch || chapterHasMatch) {
        chapter.style.display = "";
        chapterMatch = true;
      } else {
        chapter.style.display = "none";
      }
    });

    if (subjectMatch || chapterMatch) {
      subject.style.display = "";
    } else {
      subject.style.display = "none";
    }
  });
}
