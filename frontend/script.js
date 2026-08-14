// ===== CONFIG =====
// Change this to your deployed backend URL when you go live.
// Local testing (Flask running on your machine): keep as is.
const API_URL = "http://localhost:5000/api/inquiry";

// ===== CONTACT FORM =====
const form = document.getElementById("inquiry-form");
const status = document.getElementById("form-status");

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const payload = {
    name: form.name.value.trim(),
    phone: form.phone.value.trim(),
    message: form.message.value.trim(),
  };

  const submitBtn = form.querySelector("button[type=submit]");
  submitBtn.disabled = true;
  status.textContent = "Sending...";

  try {
    const res = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (!res.ok) throw new Error("Server error");

    status.textContent = "Sent! We'll reply on WhatsApp shortly.";
    form.reset();
  } catch (err) {
    // Backend down / asleep / network issue — give them a working fallback
    // instead of a dead end.
    const whatsappNumber = "919876543210";
    const fallbackText = encodeURIComponent(
      `Hi, I'm ${payload.name} (${payload.phone}). ${payload.message}`
    );
    status.innerHTML =
      `Couldn't send right now. ` +
      `<a href="https://wa.me/${whatsappNumber}?text=${fallbackText}" target="_blank" rel="noopener">Tap here to send on WhatsApp instead</a>.`;
  } finally {
    submitBtn.disabled = false;
  }
});

// ===== NAV: shrink on scroll (subtle) =====
const nav = document.getElementById("nav");
window.addEventListener("scroll", () => {
  if (window.scrollY > 40) {
    nav.style.boxShadow = "0 4px 14px rgba(36,21,18,0.06)";
  } else {
    nav.style.boxShadow = "none";
  }
});
