<template>
  <main>
    <fieldset class="element1">
      <h1 class="Register">Make an account</h1>
      <br />
      <br />
      <FormKit type="form" class="register-form" @submit="handleSubmit">
        <FormKit
          name="username"
          label="Create Username"
          validation="required|username"
          v-model="form.username"
          :errors="errors.username"
        />
        <FormKit
          type="email"
          name="email"
          label="Email address"
          validation="required|email"
          v-model="form.email"
          :errors="errors.email"
        />
        <FormKit
          type="password"
          name="password"
          label="Create Password"
          validation="required"
          v-model="form.password"
          :errors="errors.password"
        />
      </FormKit>
    </fieldset>
  </main>
</template>

<script>
import axios from "axios";
import { createToaster } from "@meforma/vue-toaster";

export default {
  name: "Register",
  components: {},
  data() {
    return {
      form: {
        username: "",
        email: "",
        password: "",
      },
      errors: {
        username: [],
        email: [],
        password: [],
      },
    };
  },
  methods: {
    async handleSubmit() {
      try {
        const response = await axios.post(
<<<<<<< HEAD
          "http://127.0.0.1:5001/register",
=======
          "https://ac40-2a01-e0a-585-d830-d0ab-574e-7d8c-ff73.eu.ngrok.io/register",
>>>>>>> f8627e8b27b999bffb23e926d7090d7f1b343306
          this.form
        );
        if (response.data === "success") {
          this.form = { username: "", email: "", password: "" };
          window.alert(`You've successfully made an account!`);
          this.$router.push({ name: 'Home' })

        } else {
          throw new Error(
            "Failed to register, please check your information again"
          );
        }
      } catch (error) {
        this.errors = error.response.data.errors;
        window.alert(`Failure, check your information again`);
      }
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
  margin-left: 310px;
}

fieldset {
  border-radius: 60px;
  margin-top: 30px;
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
  color: rgb(178, 238, 150);
}

.element1 {
  padding-top: 45px;
  margin-right: 700px;
  margin-left: 600px;
}

.Register {
  margin-left: 50px !important;
}
</style>
