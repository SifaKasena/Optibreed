document.addEventListener("DOMContentLoaded", function() {
    const roomSelector = document.getElementById("roomSelector");
    roomSelector.addEventListener("change", function() {
      const selectedRoomId = roomSelector.value;
      window.location.href = `{% url 'optibreed:dashboard' %}?room=${selectedRoomId}`;
    });
  });
