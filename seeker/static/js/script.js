const carousal = document.querySelector(".section_7_reviews_carousel");
const leftBtn = document.querySelector(".section_7_reviews_list_controls_left");
const rightBtn = document.querySelector(
  ".section_7_reviews_list_controls_right"
);
const list = document.querySelector(".section_7_reviews_list");

const onClickRight = () => {
  carousal.scrollTo(list.scrollWidth, 0);
  rightBtn.style.opacity = 0;
  leftBtn.style.opacity = 1;
};

const onClickLeft = () => {
  carousal.scrollTo(-list.scrollWidth, 0);
  rightBtn.style.opacity = 1;
  leftBtn.style.opacity = 0;
};


// for navigating to login and register page

function navigateToLoginPage() {
  // Set the URL of the target page
  var targetPageUrl = "user-login.html";

  // Navigate to the target page
  window.location.href = targetPageUrl;
}


function navigateToSignUpPage() {
  // Set the URL of the target page
  var targetPageUrl = "user-register.html";

  // Navigate to the target page
  window.location.href = targetPageUrl;
}

function navigateToFindWork() {
  // Set the URL of the target page
  var targetPageUrl = "find-work.html";

  // Navigate to the target page
  window.location.href = targetPageUrl;
}
