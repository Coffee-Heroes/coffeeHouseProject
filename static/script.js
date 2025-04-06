const modal = document.getElementById("auth-modal");
const authLinks = document.querySelectorAll(".auth-btn");
const closeBtn = document.querySelector(".close-btn");

authLinks.forEach((link) => {
  link.addEventListener("click", (e) => {
    e.preventDefault();
    modal.classList.remove("hidden");
  });
});

closeBtn.addEventListener("click", () => {
  modal.classList.add("hidden");
});

window.addEventListener("click", (e) => {
  if (e.target === modal) {
    modal.classList.add("hidden");
  }
});
