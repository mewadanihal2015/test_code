// Avatar list (Replace with your actual image URLs)
const avatars = ["avatar1.png", "avatar2.png", "avatar3.png"];
let currentIndex = 0;

// Select DOM elements
const avatarImg = document.getElementById("avatar");
const selectedAvatarText = document.getElementById("selected-avatar");

// Function to update avatar
function updateAvatar() {
    avatarImg.src = avatars[currentIndex];
}

// Handle key press events
document.addEventListener("keydown", (event) => {
    if (event.key === "ArrowRight") {
        currentIndex = (currentIndex + 1) % avatars.length;
        updateAvatar();
    } else if (event.key === "ArrowLeft") {
        currentIndex = (currentIndex - 1 + avatars.length) % avatars.length;
        updateAvatar();
    } else if (event.key === "Enter") {
        selectedAvatarText.textContent = `Selected Avatar: ${avatars[currentIndex]}`;
    }
});

// Initialize first avatar
updateAvatar();
