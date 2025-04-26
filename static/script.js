const authButtons = document.querySelectorAll(".auth-btn");
const modals = document.querySelectorAll(".modal");
const closeBtns = document.querySelectorAll(".close-btn");
const switchLinks = document.querySelectorAll(".switch-modal");


authButtons.forEach(button => {
  button.addEventListener("click", e => {
    const targetModal = button.dataset.modal;
    if (targetModal) {
      e.preventDefault();
      openModal(targetModal);
    }
  });
});


switchLinks.forEach(link => {
  link.addEventListener("click", e => {
    e.preventDefault();
    closeAllModals();
    const targetModal = link.dataset.modal;
    openModal(targetModal);
  });
});


closeBtns.forEach(btn => {
  btn.addEventListener("click", () => {
    closeAllModals();
  });
});


window.addEventListener("click", e => {
  modals.forEach(modal => {
    if (e.target === modal) {
      closeAllModals();
    }
  });
});


function openModal(id) {
  document.getElementById(`${id}-modal`).classList.remove("hidden");
}


function closeAllModals() {
  modals.forEach(modal => modal.classList.add("hidden"));
}

setTimeout(() => {
  document.querySelectorAll('.flash-message').forEach(el => el.remove());
}, 4000);