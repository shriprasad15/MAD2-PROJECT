<template>
      <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-9ndCyUaIbzAi2FUVXJi0CjmCapSmO7SnpJef0486qhLnuZ2cdeRhO02iuK6FUUVM" crossorigin="anonymous">

    <div class="bg-dark">
        <div class="container-fluid">
            <div class="row d-flex justify-content-center align-items-center m-0" style="height: 100vh">
                <div style="width: max-content;">
                    <div id="login" autocomplete="off" class="bg-light border p-5 rounded">
                        <div class="form-row">
                            <h4 class="display-6 py-2 text-black">Login</h4>
                            <div class="col-12">
                                <div class="input-group mb-3">
                                    <div class="input-group-prepend">
                                        <span class="input-group-text h-100 rounded-0 rounded-start-2" id="basic-addon1"><i
                                                class="fas fa-envelope"></i></span>
                                    </div>
                                    <input ref="email" name="email" type="text" value="" class="input form-control"
                                        id="email" placeholder="Email" aria-label="email" aria-describedby="basic-addon1" />
                                </div>
                            </div>
                            <div class="col-12">
                                <div class="input-group mb-3">
                                    <div class="input-group-prepend">
                                        <span class="input-group-text h-100 rounded-0 rounded-start-2" id="basic-addon1"><i
                                                class="fas fa-lock"></i></span>
                                    </div>
                                    <input ref="password" name="password" type="password" value=""
                                        class="input form-control" id="password" placeholder="password" required="true"
                                        aria-label="password" aria-describedby="basic-addon1" />
                                    <div class="input-group-append">
                                        <span style="cursor: pointer" class="input-group-text h-100 rounded-0 rounded-end-2"
                                            @click="password_show_hide()">
                                            <i class="fas fa-eye" id="show_eye"></i>
                                            <i class="fas fa-eye-slash d-none" id="hide_eye"></i>
                                        </span>
                                    </div>
                                </div>
                            </div>

                            <div class="col-12 self-right">
                                <button @click="handleLogin" class="btn btn-primary w-100" name="signin">
                                    Log In
                                </button>
                            </div>
                            <div class="col-sm-12 pt-3 text-center">
                                <p class="text-black">
                                    Don't have an account yet?
                                    <router-link class="link-primary" style="text-decoration: underline" to="/signup">Sign
                                        Up</router-link>
                                </p>
                            </div>
                        </div>
                         <p style="color: red; font-weight: bold;" class="text-center">{{ err }}</p>
                    </div>

                </div>

            </div>
        </div>
    </div>
</template>
<script>
import { ref } from "vue";

export default {
    name: "Login",
    setup() {
        const email = ref();
        const password = ref();
        const user = ref(null);
        const err = ref('');
        const loginUser = async () => {
            const response = await fetch("http://localhost:8081/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    email: email.value.value,
                    password: password.value.value,
                }),
            });
            const data = await response.json();
            console.log(data);
            if (response.status === 200) {
                user.value = data.message;
                sessionStorage.setItem("token", JSON.stringify(user.value));
                console.log(user.value);
                window.location.href = "/home";
            } else {
                console.log(data.err);
                if(data.err){
                    err.value = data.err;
                    setTimeout(() => {
                        err.value = '';
                    }, 3000);
                }
                else{
                    err.value = "Something went wrong";
                    setTimeout(() => {
                        err.value = '';
                    }, 3000);
                }
            }
        }
        const handleLogin = () => {
            console.log(email.value.value, password.value.value);
            loginUser();
        }
        const password_show_hide = () => {
            var x = document.getElementById("password");
            var show_eye = document.getElementById("show_eye");
            var hide_eye = document.getElementById("hide_eye");
            hide_eye.classList.remove("d-none");
            if (x.type === "password") {
                x.type = "text";
                show_eye.style.display = "none";
                hide_eye.style.display = "block";
            } else {
                x.type = "password";
                show_eye.style.display = "block";
                hide_eye.style.display = "none";
            }
        }

        return {
            email,
            err,
            password,
            handleLogin,
            password_show_hide
        }
    }
};
</script>
