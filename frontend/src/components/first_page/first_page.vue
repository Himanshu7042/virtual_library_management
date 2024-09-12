<template>
    <h1>Welcome to Liberary</h1>

    <router-link :to="{ name: 'admin_auth' }" v-slot="{ navigate }">
      <button class="btn btn-primary" @click="navigate">Admin Login</button>
    </router-link>
    <router-link :to="{ name: 'user_auth' }" v-slot="{ navigate }">
      <button class="btn btn-primary" @click="navigate">User Login</button>
    </router-link>
</template>

<style>
.btn {
    margin-bottom: 2%;
    margin-right: 10px;
}
</style>