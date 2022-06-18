// Invoke Functions Call on Document Loaded
// document.addEventListener("DOMContentLoaded", function () {
//   hljs.highlightAll();
// });

const alertWrapper = document.querySelector(".alert");
const alertClose = document.querySelector(".alert__close");

if (alertWrapper) {
  alertClose.addEventListener("click", () => {
    alertWrapper.style.display = "none";
  });
}
