<template>
  <div>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-9ndCyUaIbzAi2FUVXJi0CjmCapSmO7SnpJef0486qhLnuZ2cdeRhO02iuK6FUUVM" crossorigin="anonymous">

    <h1>Admin dashboard</h1>
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
      <div class="container-fluid">
        <button class="navbar-toggler" type="button" @click="toggleNavbar">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" :class="{ 'show': isNavbarOpen }" id="navbarNavDropdown">
          <ul class="navbar-nav">
            <li class="nav-item">
              <router-link to="/" class="nav-link" aria-current="page">Home</router-link>
            </li>

            <li class="nav-item dropdown">
              <a class="nav-link dropdown-toggle" href="#" role="button" @click="toggleCategoryDropdown">
                Category Operations
              </a>
              <ul class="dropdown-menu" :class="{ 'show': isCategoryDropdownOpen }">
                <li v-for="item in categoryItems" :key="item">
                  <router-link :to="`/admin_dashboard/${item}`" class="dropdown-item">{{ item }}</router-link>
                </li>
              </ul>
            </li>

            <li class="nav-item dropdown">
              <a class="nav-link dropdown-toggle" href="#" role="button" @click="toggleProductDropdown">
                Product Operations
              </a>
              <ul class="dropdown-menu" :class="{ 'show': isProductDropdownOpen }">
                <li v-for="item in productItems" :key="item">
                  <router-link :to="`/admin_dashboard/${item}`" class="dropdown-item">{{ item }}</router-link>
                </li>
              </ul>
            </li>

            <li class="nav-item">
              <router-link to="/summary" class="nav-link" aria-current="page">Summary</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/logout" class="nav-link" aria-current="page">Logout</router-link>
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
      <h1 class="mb-4">Category List</h1>
      <ul class="list-group">
        <li v-for="category in category_items" :key="category.id" class="list-group-item">{{ category.name }}</li>
      </ul>
    </div>

    <div class="container mt-5">
      <h1 class="mb-4">Product List</h1>
      <div class="row">
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
export default {
  name: 'ProductList',
  props: {
    msg: String,
    error: String,
    category_items: Array,
    product_items: Array,
  },
  data() {
    return {
      isNavbarOpen: false,
      isCategoryDropdownOpen: false,
      isProductDropdownOpen: false,
      categoryItems: ['Create_Category', 'Delete_Category', 'Edit_Category'],
      productItems: ['Create_Product', 'Delete_Product', 'Edit_Product'],
    };
  },
  methods: {
    toggleNavbar() {
      this.isNavbarOpen = !this.isNavbarOpen;
    },
    toggleCategoryDropdown() {
      this.isCategoryDropdownOpen = !this.isCategoryDropdownOpen;
    },
    toggleProductDropdown() {
      this.isProductDropdownOpen = !this.isProductDropdownOpen;
    },
  },
  created() {
    this.fetchProducts();
    this.fetchCategories();
  },
  methods: {
    async fetchProducts() {
      try {
        const response = await fetch('YOUR_PRODUCTS_API_URL');
        if (response.ok) {
          const data = await response.json();
          this.product_items = data;
        } else {
          console.error('Failed to fetch products');
        }
      } catch (error) {
        console.error('Error fetching products:', error);
      }
    },
    async fetchCategories() {
      try {
        const response = await fetch('YOUR_CATEGORIES_API_URL');
        if (response.ok) {
          const data = await response.json();
          this.category_items = data;
        } else {
          console.error('Failed to fetch categories');
        }
      } catch (error) {
        console.error('Error fetching categories:', error);
      }
    },
  },
};
</script>
