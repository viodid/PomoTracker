// navbar expand in mobile

document.addEventListener('DOMContentLoaded', () => {
  const open = document.querySelector('#open-sidebar');
  let hamburger = false;
  open.addEventListener('click', () => {
      if (!hamburger) {
        document.querySelector("#sidebar")
          .classList
          .toggle("hidden");
        document.querySelector("#sidebar").style.height = "300px";
        document.querySelector("#sidebar").style.width = "100%";
        open.style.transform = "rotate(-90deg)";
        hamburger = true;
      } else {
        document.querySelector("#sidebar")
          .classList
          .toggle("hidden");
        document.querySelector("#sidebar").style.height = "0";
        document.querySelector("#sidebar").style.width = "0";
        open.style.transform = "rotate(0deg)";
        hamburger = false;
      }
    }
  );
});
