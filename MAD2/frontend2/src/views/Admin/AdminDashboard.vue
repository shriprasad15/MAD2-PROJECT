<template>
  <div>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet"
          integrity="sha384-9ndCyUaIbzAi2FUVXJi0CjmCapSmO7SnpJef0486qhLnuZ2cdeRhO02iuK6FUUVM" crossorigin="anonymous">

    <h1>Admin dashboard</h1>

    <nav class="navbar navbar-expand-lg bg-body-tertiary">
      <div class="container-fluid">
        <button class="navbar-toggler" type="button" @click="toggleNavbar">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" :class="{ 'show': isNavbarOpen }" id="navbarNavDropdown">
          <ul class="navbar-nav">
            <li class="nav-item">
              <router-link to="/admin-dashboard" class="nav-link" aria-current="page">Home</router-link>
            </li>

            <li class="nav-item dropdown">
              <a class="nav-link dropdown-toggle" href="#" role="button" @click="toggleCategoryDropdown">
                Category Operations
              </a>
              <ul class="dropdown-menu" :class="{ 'show': isCategoryDropdownOpen }">
                <li v-for="item in categoryItems" :key="item">
                  <router-link :to="`/admin-dashboard/${item}`" class="dropdown-item">{{ item }}</router-link>
                </li>
              </ul>
            </li>

            <li class="nav-item">
              <router-link to="/admin-dashboard/Approve-Requests" class="nav-link" aria-current="page">Manager Control</router-link>
            </li>

            <li class="nav-item">
              <router-link to="#" class="nav-link" aria-current="page">Summary</router-link>
            </li>
            <li class="nav-item">
              <router-link to="#" class="nav-link" aria-current="page">Logout</router-link>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <!-- Display success message if available -->
    <div v-if="msg" class="alert alert-success" role="alert">
      {{ msg }}
    </div>
    <!-- Display error message if available -->
    <div v-if="error" class="alert alert-danger mb-3" role="alert">
      {{ error }}
    </div>

    <div class="container mt-5">
<!--      <h1 class="mb-4">Category List</h1>-->
      <h1 class="mb-4">{{category_items.length===0?"No Categories": "Category List"}}</h1>
      <ul class="list-group">
        <li v-for="category in category_items" :key="category.id" class="list-group-item">{{ category.name }}</li>
      </ul>
    </div>

    <div class="container mt-5">
      <h1 class="mb-4">{{product_items.length===0?"No Products": "Product List"}}</h1>      <div class="row">
        <div v-for="product in product_items" :key="product.id" class="col-md-4">
          <div class="card mb-4">
            <div class="card-body">
              <h5 class="card-title">{{ product.name }}</h5>
              <p class="card-text">
                Category:
                <span v-for="category in category_items" :key="category.id">
                  <span v-if="category.id === product.category_id">{{ category.name }}</span>
                </span>
              </p>
              <p class="card-text">Rate Per Unit: ₹{{ product.rate_per_unit }}</p>
              <p class="card-text">Quantity: {{ product.quantity }}</p>
              <p class="card-text">Manufacture Date: {{ product.manufacture_date }}</p>
              <p class="card-text">Expiry Date: {{ product.expiry_date }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {fetchCategories, fetchProducts} from "../../../api_helpers/helpers";

export default {

  name: 'ProductList',
  props: {
    msg: String,
    error: String,

  },
  data() {
    return {
      isNavbarOpen: false,
      isCategoryDropdownOpen: false,
      isProductDropdownOpen: false,
      categoryItems: ['Create-Category', 'Delete-Category', 'Edit-Category'],
      category_items: [],
      product_items: [],
    };
  },

  mounted() {
    this.assign();
  },
  methods: {

    async assign() {
      this.category_items = await fetchCategories();
      this.product_items= await fetchProducts()
    },
    toggleNavbar() {
      this.isNavbarOpen = !this.isNavbarOpen;
    },
    toggleCategoryDropdown() {
      this.isCategoryDropdownOpen = !this.isCategoryDropdownOpen;
    },
  },
};
</script>
