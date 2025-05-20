function toggleForm() {
  const loginForm = document.getElementById('login-form');
  const signupForm = document.getElementById('signup-form');
  const title = document.getElementById('form-title');
  const toggleText = document.getElementById('toggle-text');

  if (loginForm.style.display === 'none') {
    loginForm.style.display = 'block';
    signupForm.style.display = 'none';
    title.innerText = 'Login';
    toggleText.innerHTML = `Don't have an account? <a href="#" onclick="toggleForm()">Sign Up</a>`;
  } else {
    loginForm.style.display = 'none';
    signupForm.style.display = 'block';
    title.innerText = 'Sign Up';
    toggleText.innerHTML = `Already have an account? <a href="#" onclick="toggleForm()">Login</a>`;
  }
}
