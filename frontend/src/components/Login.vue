<template>
  <main>
    <fieldset class="element2">
      <h1 class="login">Log in</h1>
      <br />
      <br />

      <FormKit class="login-form" type="form" @submit="submitHandler">
        <FormKit
          name="username"
          label="Username"
          validation="required"
          v-model="formData.username"
          :rules="[(val) => !!val || 'Username is required']"
        />
        <FormKit
          type="password"
          name="password"
          label="Password"
          validation="required"
          v-model="formData.password"
          :rules="[(val) => !!val || 'Password is required']"
        />
      </FormKit>
      <p class="register-text" @click="goToRegister">
        Don't have an account? Register here
      </p>
    </fieldset>
  </main>
</template>

<script>
import axios from "axios";
import { createToaster } from "@meforma/vue-toaster";
const toaster = createToaster();

export default {
  name: "Login",
  components: {},
  data() {
    return {
      formData: {
        username: "",
        password: "",
        feedback: "",
      },
    };
  },
  methods: {
    submitHandler() {
      axios
        .post(
          "https://airbnb-calculator-backend.herokuapp.com/login",
          this.formData
        )
        .then((response) => {
          if (response.data === "You are now logged in") {
            // Handle successful login
            this.isLoggedIn = true;
            window.alert("You've successfully logged in!");
            this.$router.push({ name: "Home" });

            // Redirect the user to the home page or any other page
          } else {
            window.alert("Invalid email or password!");

          }
        })
        .catch((error) => {
          this.error = error.message;
        });
    },
    goToRegister() {
      this.$router.push({ name: "Register" });
    },
  },
};
</script>

<style>
.input {
  color: rgb(0, 0, 0);
  background-color: rgb(178, 238, 150);
  text-align: center;
  text-decoration: none;
  font-size: 18px;
  cursor: pointer;
  margin-bottom: 16px !important;
  padding: 9px 13px;
  vertical-align: middle;
  overflow: hidden;
  border-radius: 40px;
  margin-left: 135px;
}

.register-text {
  color: rgb(101, 214, 49);
  cursor: pointer;
  text-decoration: underline;
}

fieldset {
  border-radius: 60px;
  margin-top: 700px;
  min-width: 0;
  padding-left: 100px;
  border-top: 2px;
  border-top-style: solid;
  border-bottom: 2px;
  border-bottom-style: solid;
  border-left: 2px;
  border-left-style: solid;
  border-right: 2px;
  border-right-style: solid;
}

h1 {
  font-family: var(--fk-font-family-label);
  -webkit-text-stroke: 1px rgb(178, 238, 150);
  font-style: inherit;
  font-family: var(--fk-font-family-label);
}

.element2 {
  padding-top: 45px;
  margin-right: 700px;
  margin-left: 600px;
}
</style>
