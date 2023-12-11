
<!--<template>-->
<!--    <div class="bg-dark">-->
<!--        <div style="width: max-content;" class="container-fluid">-->
<!--            <div class="row d-flex justify-content-center align-items-center m-0" style="height: 100vh;">-->
<!--                <div class="login_oueter">-->
<!--                    <div action="" autocomplete="off" class="bg-light border p-5 rounded ">-->
<!--                        <div class="div-row">-->
<!--                            <h4 class="display-6 py-2 text-black">Signup</h4>-->
<!--                            <div class="col-12">-->
<!--                                <div class="input-group mb-3">-->
<!--                                    <div class="input-group-prepend ">-->
<!--                                        <span class="input-group-text h-100 rounded-0 rounded-start-2" id="basic-addon1"><i-->
<!--                                                class="fas fa-user"></i></span>-->
<!--                                    </div>-->
<!--                                    <input ref="username" name="username" type="text" value="" class="input form-control"-->
<!--                                        id="username" placeholder="Username" aria-label="Username"-->
<!--                                        aria-describedby="basic-addon1" />-->
<!--                                </div>-->
<!--                            </div>-->
<!--                            <div class="col-12">-->
<!--                                <div class="input-group mb-3">-->
<!--                                    <div class="input-group-prepend ">-->
<!--                                        <span class="input-group-text h-100 rounded-0 rounded-start-2" id="basic-addon1"><i-->
<!--                                                class="fas fa-envelope"></i></span>-->
<!--                                    </div>-->
<!--                                    <input ref="email" name="email" type="text" value="" class="input form-control"-->
<!--                                        id="email" placeholder="Email" aria-label="email" aria-describedby="basic-addon1" />-->
<!--                                </div>-->
<!--                            </div>-->
<!--                            <div class="col-12">-->
<!--                                <div class="input-group mb-3">-->
<!--                                    <div class="input-group-prepend">-->
<!--                                        <span class="input-group-text h-100 rounded-0 rounded-start-2" id="basic-addon1"><i-->
<!--                                                class="fas fa-lock"></i></span>-->
<!--                                    </div>-->
<!--                                    <input ref="password" name="password" type="password" value=""-->
<!--                                        class="input form-control" id="password" placeholder="password" required="true"-->
<!--                                        aria-label="password" aria-describedby="basic-addon1" />-->
<!--                                    <div class="input-group-append">-->
<!--                                        <span style="cursor: pointer;"-->
<!--                                            class="input-group-text h-100 rounded-0 rounded-end-2"-->
<!--                                            @click="password_show_hide()">-->
<!--                                            <i class="fas fa-eye" id="show_eye"></i>-->
<!--                                            <i class="fas fa-eye-slash d-none" id="hide_eye"></i>-->
<!--                                        </span>-->
<!--                                    </div>-->
<!--                                </div>-->
<!--                            </div>-->

<!--                            <div class="col-12 self-right">-->
<!--                                <button @click.prevent="handleSignup()" class="btn btn-primary w-100" type="submit"-->
<!--                                    name="signin">Sign Up</button>-->
<!--                            </div>-->
<!--                            <div class="col-sm-12 pt-3 text-center">-->
<!--                                <p class="text-black">Already have an account? <router-link class="link-primary"-->
<!--                                        style="text-decoration: underline;" to="/login">Log In</router-link></p>-->
<!--                            </div>-->
<!--                            <p v-show="errModal">{{ err }}</p>-->
<!--                        </div>-->
<!--                    </div>-->
<!--                </div>-->
<!--            </div>-->
<!--        </div>-->
<!--    </div>-->
<!--</template>-->
<template>
      <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-9ndCyUaIbzAi2FUVXJi0CjmCapSmO7SnpJef0486qhLnuZ2cdeRhO02iuK6FUUVM" crossorigin="anonymous">

  <h1>Welcome to User Signup Page</h1>
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
    <router-link to="/user-login"><button type="button" class="btn btn-primary">Back</button></router-link>
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
