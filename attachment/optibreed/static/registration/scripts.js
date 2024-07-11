document.addEventListener("DOMContentLoaded", function() {
    document.addEventListener("click", function(event) {
        var isClickInsideCard = document.querySelector(".card").contains(event.target);

        if (!isClickInsideCard) {
            window.location.href = "/";
        }
    });

    const closeButton = document.getElementById("close-card");
    closeButton.addEventListener("click", function() {
        const card = document.querySelector(".card");
        card.style.display = "none";
        window.location.href = "/";
    });
});




// signup
document.addEventListener("DOMContentLoaded", function () {
    document.addEventListener("click", function (event) {
      var isClickInsideCard = document
        .querySelector(".card")
        .contains(event.target);
  
      if (!isClickInsideCard) {
        window.location.href = "/";
      }
    });
  
    const closeButton = document.getElementById("close-card");
  
    closeButton.addEventListener("click", function () {
      const card = document.querySelector(".card");
      card.style.display = "none";
      window.location.href = "/";
    });
  });
  