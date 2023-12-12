
<template>
      <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-9ndCyUaIbzAi2FUVXJi0CjmCapSmO7SnpJef0486qhLnuZ2cdeRhO02iuK6FUUVM" crossorigin="anonymous">

  <h1>Welcome to Manager Signup Page</h1>
  <form @submit.prevent="handleSignup">
    <div class="input-group">
      <span class="input-group-text">First and last name</span>
      <input type="text" aria-label="First name" v-model="firstName" class="form-control" required>
      <input type="text" aria-label="Last name" v-model="lastName" class="form-control" required>
    </div>
    <br>
    <div class="form-floating mb-3">
      <input type="number" class="form-control" v-model="mobile" placeholder="Mobile" required>
      <label>Mobile</label>
    </div>

    <div class="form-floating mb-3">
      <input type="email" class="form-control" v-model="email" placeholder="Email address" required>
      <label>Email address</label>
    </div>

    <div class="form-floating">
      <input type="password" class="form-control" v-model="password" placeholder="Password" required>
      <label>Password</label>
    </div>
    <br>
    <button type="submit" class="btn btn-primary">Submit</button>
    <router-link to="/manager-login"><button type="button" class="btn btn-primary">Back</button></router-link>
  </form>
</template>

<script>
import { ref } from "vue";

export default {
  name: "Signup",
  setup() {
    const firstName = ref('');
    const lastName = ref('');
    const mobile = ref('');
    const email = ref('');
    const password = ref('');
    const user = ref(null);
    const err = ref(null);
    const errModal = ref(false);

    const handleSignup = async () => {
      const res = await fetch("http://localhost:5050/signup", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          firstName: firstName.value,
          lastName: lastName.value,
          mobile: mobile.value,
          email: email.value,
          password: password.value,
        }),
      });

      const data = await res.json();
      if (res.ok) {
        user.value = data;
        sessionStorage.setItem("user", JSON.stringify(user.value));
        alert("Signup Successful");
        // Redirect or navigate to login page
        // window.location = "/login";
      } else {
        err.value = data.message;
        errModal.value = true;
        setTimeout(() => {
          errModal.value = false;
        }, 3000);
        user.value = null;
      }
    };

    return {
      handleSignup,
      firstName,
      lastName,
      mobile,
      email,
      password,
      err,
      errModal,
    };
  },
};
</script>
