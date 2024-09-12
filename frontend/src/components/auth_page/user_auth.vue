<template>
    <h1>User Login Page</h1>
    <form class="login-form" @submit.prevent="signIn">
        <div class="form-group">
            <label for="username">Username:</label>
            <input type="text" v-model="FormData.username" id="username" placeholder="Enter your username" class="form-input">
        </div>
        <div class="form-group">
            <label for="password">Password:</label>
            <input type="password" v-model="FormData.password" id="password" placeholder="Enter your password" class="form-input">
        </div>
        <button type="submit" class="btn btn-primary">Sign In</button>
        <button type="button" class="btn btn-primary" @click="signUp">Sign Up</button>
    </form>
    <router-link :to="{ name: 'admin_auth' }" v-slot="{ navigate }">
      <button class="btn btn-secondary" @click="navigate">Admin Login</button>
    </router-link>
</template>

<script>
import axiosFetch from '../../axios';
export default {
    data() {
        return {
            FormData : {
                username: '',
                password: '',
            }
        };
    },
    methods: {
        signIn() {
            axiosFetch.post('/user/login', this.FormData).then(resp => {
                console.log(resp.data)
                localStorage.setItem('authToken', resp.data.access_token)   
                this.$router.push('/user/home')
              })
                
            .catch(err => {
                console.log(err)

                console.log("Failed to sign in")
            })
                alert(this.FormData);

        },
        signUp(){
            axiosFetch.post('/user/signup', this.FormData).then(resp=>{
                console.log(resp)})
            .catch(err => {
                console.log(err)
                console.log(this.FormData)
                console.log("Failed to sign up")
            })
            alert(this.FormData);
        },
    }
}
</script>


<style>
/* Add custom styles here */
.login-container {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

h1 {
  text-align: center;
  margin-bottom: 20px;
}

.login-form {
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 15px;
}

.form-label {
  display: inline-block;
  width: 100px; /* Adjust width as needed */
}

.form-input {
  width: calc(25% - 100px); /* Adjust width to fit remaining space */
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.btn {
  display: block;
  width: 10%;
  padding: 10px 0;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-left: 45%;
}

.btn-primary {
  background-color: #007bff;
  color: #fff;
}

.btn-secondary {
  background-color: #6c757d;
  color: #fff;
}

.btn:hover {
  opacity: 0.8;
}
</style>