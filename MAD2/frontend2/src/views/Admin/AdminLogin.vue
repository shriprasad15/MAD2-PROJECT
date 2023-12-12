<template>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-9ndCyUaIbzAi2FUVXJi0CjmCapSmO7SnpJef0486qhLnuZ2cdeRhO02iuK6FUUVM" crossorigin="anonymous">
  <form @submit.prevent="submitForm">
    <section class="vh-100" style="background-color: #273447;">
      <div class="container py-5 h-100">
        <div class="row d-flex justify-content-center align-items-center h-100">
          <div class="col col-xl-10">
            <div class="card" style="border-radius: 1rem;">
              <div class="row g-0">
                <div class="col-md-6 col-lg-5 d-none d-md-block">
                  <img src="../../../static/mrbean_login.jpg"
                    alt="login form" class="img-fluid" style="border-radius: 1rem 0 0 0;" height="1200" />
                  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;

                  <img src="../../../static/mrbean_login.jpg"
                    alt="login form" class="img-fluid" style="border-radius: 0 0 0 1rem;" height="1200" />
                </div>
                <div class="col-md-6 col-lg-7 d-flex align-items-center">
                  <div class="card-body p-4 p-lg-5 text-black">

                    <div class="d-flex align-items-center mb-3 pb-1">
                      <i class="fas fa-cubes fa-2x me-3" style="color: #ff6219;"></i>
                      <span class="h1 fw-bold mb-0">MrBean Groceries Admin Login</span>
                    </div>

                    <h5 class="fw-normal mb-3 pb-3" style="letter-spacing: 1px;">Only MrBean can login!! 😜</h5>
                    <div v-if="error" class="alert alert-danger mt-3" role="alert">
                      {{ error }}
                    </div>

                    <div class="form-floating mb-3">
                      <input v-model="email" type="email" class="form-control" id="floatingInput" placeholder="name@example.com" required>
                      <label for="floatingInput">Email address</label>
                    </div>

                    <div class="form-floating">
                      <input v-model="password" type="password" class="form-control" id="floatingPassword" placeholder="Password" required>
                      <label for="floatingPassword">Password</label>
                    </div>
                    <br>

                    <div class="pt-1 mb-4">
                      <button class="btn btn-lg btn-block" type="submit" style="background-color: #6F4E37; color: white;">Login</button>
                    </div>
                    <a href="/MAD2/frontend2/static"><button type="button" class="btn btn-primary" style="background-color: #6F4E37; color: white;">Home</button></a>

                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </form>
</template>

<script>
export default {
  data() {
    return {
      email: '',
      password: '',
    };
  },
  props: {
    error: String,
  },
  methods: {
    submitForm() {

      console.log('Submitted:', this.email, this.password);
    },
  },
};
</script>

<style>
/* Your CSS styles */
</style>
