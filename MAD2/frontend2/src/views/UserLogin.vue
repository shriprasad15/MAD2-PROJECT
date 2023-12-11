<!--<template>-->
<!--      <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-9ndCyUaIbzAi2FUVXJi0CjmCapSmO7SnpJef0486qhLnuZ2cdeRhO02iuK6FUUVM" crossorigin="anonymous">-->

<!--    <div class="bg-dark">-->
<!--        <div class="container-fluid">-->
<!--            <div class="row d-flex justify-content-center align-items-center m-0" style="height: 100vh">-->
<!--                <div style="width: max-content;">-->
<!--                    <div id="login" autocomplete="off" class="bg-light border p-5 rounded">-->
<!--                        <div class="form-row">-->
<!--                            <h4 class="display-6 py-2 text-black">Login</h4>-->
<!--                            <div class="col-12">-->
<!--                                <div class="input-group mb-3">-->
<!--                                    <div class="input-group-prepend">-->
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
<!--                                        <span style="cursor: pointer" class="input-group-text h-100 rounded-0 rounded-end-2"-->
<!--                                            @click="password_show_hide()">-->
<!--                                            <i class="fas fa-eye" id="show_eye"></i>-->
<!--                                            <i class="fas fa-eye-slash d-none" id="hide_eye"></i>-->
<!--                                        </span>-->
<!--                                    </div>-->
<!--                                </div>-->
<!--                            </div>-->

<!--                            <div class="col-12 self-right">-->
<!--                                <button @click="handleLogin" class="btn btn-primary w-100" name="signin">-->
<!--                                    Log In-->
<!--                                </button>-->
<!--                            </div>-->
<!--                            <div class="col-sm-12 pt-3 text-center">-->
<!--                                <p class="text-black">-->
<!--                                    Don't have an account yet?-->
<!--                                    <router-link class="link-primary" style="text-decoration: underline" to="/signup">Sign-->
<!--                                        Up</router-link>-->
<!--                                </p>-->
<!--                            </div>-->
<!--                        </div>-->
<!--                         <p style="color: red; font-weight: bold;" class="text-center">{{ err }}</p>-->
<!--                    </div>-->

<!--                </div>-->

<!--            </div>-->
<!--        </div>-->
<!--    </div>-->
<!--</template>-->

<template>

    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-9ndCyUaIbzAi2FUVXJi0CjmCapSmO7SnpJef0486qhLnuZ2cdeRhO02iuK6FUUVM" crossorigin="anonymous">
       <section class="vh-100" style="background-color: #273447;">
  <div class="container py-5 h-100">
    <div class="row d-flex justify-content-center align-items-center h-100">
      <div class="col col-xl-10">
        <div class="card" style="border-radius: 1rem;">
          <div class="row g-0">
            <div class="col-md-6 col-lg-5 d-none d-md-block">
              <img src="../../static/mrbean_login.jpg"
                alt="login form" class="img-fluid" style="border-radius: 1rem 0 0 0;" height="273"/>
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;

                <img src="../../static/mrbean_login.jpg"
                alt="login form" class="img-fluid" style="border-radius: 0 0 0 1rem;" height="273"/>
            </div>
            <div class="col-md-6 col-lg-7 d-flex align-items-center">
              <div class="card-body p-4 p-lg-5 text-black">


                  <div class="d-flex align-items-center mb-3 pb-1">
                    <i class="fas fa-cubes fa-2x me-3" style="color: #ff6219;"></i>
                    <span class="h1 fw-bold mb-0">MrBean Groceries</span>
                  </div>

                  <h5 class="fw-normal mb-3 pb-3" style="letter-spacing: 1px;">Sign into your account</h5>

                 <div class="form-floating mb-3">
                    <input type="email" class="form-control" name='email' id="floatingInput" placeholder="name@example.com" required>
                    <label for="floatingInput">Email address</label>
                  </div>

                  <div class="form-floating">
                    <input type="password" class="form-control" name='password' id="floatingPassword" placeholder="Password" required>
                    <label for="floatingPassword">Password</label>
                  </div>
                  <br>

                  <div class="pt-1 mb-4">
                     <button @click="handleLogin" class="btn btn-lg btn-block" type="submit" style="background-color: #6F4E37; color: white;">Login</button>


                  </div><br>
                  <p class="mb-5 pb-lg-2" style="color: #393f81;">Don't have an account? <a href="/user-signup"
                      style="color: #393f81;">Register here</a></p>
                <a href="/"><button type="button" class="btn btn-primary" style="background-color: #6F4E37; color: white;">Home</button></a>
<!--                </form>-->

              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

</template>

<script>
import { ref } from "vue";

export default {
  name: "Login",
  setup() {
    const email = ref(''); // Initialize with an empty string
    const password = ref(''); // Initialize with an empty string
    const user = ref(null);
    const err = ref('');
    console.log(email, password);
    const loginUser = async () => {
      const response = await fetch("http://localhost:8080/user-login", {
        method: "POST",
        headers: {
          "Content-Type": "text/plain",
        },
        body: JSON.stringify({
          email: email.value, // Access the ref directly without `.value`
          password: password.value, // Access the ref directly without `.value`

        }),

      });

      const data = await response.json();
      // console.log(data);
      if (response.status === 200) {
        user.value = data.message;
        sessionStorage.setItem("token", JSON.stringify(user.value));
        console.log(user.value);
        window.location.href = "/home";
      } else {
        console.log(data.err);
        if (data.err) {
          err.value = data.err;
          setTimeout(() => {
            err.value = '';
          }, 3000);
        } else {
          err.value = "Something went wrong";
          setTimeout(() => {
            err.value = '';
          }, 3000);
        }
      }
    };

    const handleLogin = () => {
      console.log(email.value, password.value); // Access values without `.value`
      console.log("Check");
      loginUser();
    };

    // Rest of your functions remain unchanged

    return {
      email,
      err,
      password,
      handleLogin,
      // Other functions and values
    };
  },
};
</script>


