<template>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet"
          integrity="sha384-9ndCyUaIbzAi2FUVXJi0CjmCapSmO7SnpJef0486qhLnuZ2cdeRhO02iuK6FUUVM" crossorigin="anonymous">
  <h1>Pending Requests (Manager Dashboard)</h1>
  <nav class="navbar navbar-expand-lg bg-body-secondary">
      <div class="container-fluid">
        <button class="navbar-toggler" type="button" @click="toggleNavbar">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" :class="{ 'show': isNavbarOpen }" id="navbarNavDropdown">
          <ul class="navbar-nav">
            <li class="nav-item">
              <router-link to="/manager-dashboard" class="nav-link" aria-current="page">Home</router-link>
            </li>
          </ul>
        </div>
      </div>
    </nav>
 <div class="container mt-5">
      <h3 class="mb-4">Pending Create Category</h3>
      <ul class="list-group">
        <li v-for="category in pending_category_items" :key="category.id" class="list-group-item">{{ category.name }}</li>
      </ul>
    </div>

</template>

<script>
import {fetchPendingCategories} from "../../../api_helpers/helpers";

export default {
  name: "PendingRequests",
  data() {
    return {
      pending_category_items: [],
    };
  },
  mounted() {
    this.assign();
  },
  methods:{
    async assign() {
      this.pending_category_items= await fetchPendingCategories()
    },
  },

}
</script>