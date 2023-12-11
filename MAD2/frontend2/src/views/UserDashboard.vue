<template>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-9ndCyUaIbzAi2FUVXJi0CjmCapSmO7SnpJef0486qhLnuZ2cdeRhO02iuK6FUUVM" crossorigin="anonymous">

  <div>
    <h3>Welcome {{ name }} to MrBean Groceries</h3>
    <!-- Rest of your HTML content goes here -->
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
  <div class="container-fluid">
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavDropdown" aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>

    <div class="collapse navbar-collapse" id="navbarNavDropdown">
      <ul class="navbar-nav">
        <!-- Home Link on the Left -->
        <li class="nav-item">
          <a class="nav-link active" aria-current="page" href="/user_dashboard/{{ userid }}">
            <svg xmlns="http://www.w3.org/2000/svg" width="35" height="35" fill="currentColor" class="bi bi-house-door" viewBox="0 0 16 16">
              <path d="M8.354 1.146a.5.5 0 0 0-.708 0l-6 6A.5.5 0 0 0 1.5 7.5v7a.5.5 0 0 0 .5.5h4.5a.5.5 0 0 0 .5-.5v-4h2v4a.5.5 0 0 0 .5.5H14a.5.5 0 0 0 .5-.5v-7a.5.5 0 0 0-.146-.354L13 5.793V2.5a.5.5 0 0 0-.5-.5h-1a.5.5 0 0 0-.5.5v1.293L8.354 1.146ZM2.5 14V7.707l5.5-5.5 5.5 5.5V14H10v-4a.5.5 0 0 0-.5-.5h-3a.5.5 0 0 0-.5.5v4H2.5Z"/>
            </svg>Home
          </a>
        </li>

        <!-- Profile Link on the Left -->
        <li class="nav-item">
          <a class="nav-link active" aria-current="page" href="/profile/{{ userid }}">
            <svg xmlns="http://www.w3.org/2000/svg" width="35" height="35" fill="currentColor" class="bi bi-person-circle" viewBox="0 0 16 16">
  <path d="M11 6a3 3 0 1 1-6 0 3 3 0 0 1 6 0z"/>
  <path fill-rule="evenodd" d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8zm8-7a7 7 0 0 0-5.468 11.37C3.242 11.226 4.805 10 8 10s4.757 1.225 5.468 2.37A7 7 0 0 0 8 1z"/>
</svg> Profile
          </a>
        </li>

        <!-- Logout Link on the Left -->
        <li class="nav-item">
          <a class="nav-link active" aria-current="page" href="/logout">
            <svg xmlns="http://www.w3.org/2000/svg" width="35" height="35" fill="currentColor" class="bi bi-box-arrow-right" viewBox="0 0 16 16">
  <path fill-rule="evenodd" d="M10 12.5a.5.5 0 0 1-.5.5h-8a.5.5 0 0 1-.5-.5v-9a.5.5 0 0 1 .5-.5h8a.5.5 0 0 1 .5.5v2a.5.5 0 0 0 1 0v-2A1.5 1.5 0 0 0 9.5 2h-8A1.5 1.5 0 0 0 0 3.5v9A1.5 1.5 0 0 0 1.5 14h8a1.5 1.5 0 0 0 1.5-1.5v-2a.5.5 0 0 0-1 0v2z"/>
  <path fill-rule="evenodd" d="M15.854 8.354a.5.5 0 0 0 0-.708l-3-3a.5.5 0 0 0-.708.708L14.293 7.5H5.5a.5.5 0 0 0 0 1h8.793l-2.147 2.146a.5.5 0 0 0 .708.708l3-3z"/>
</svg> Logout
          </a>
        </li>
      </ul>

      <!-- Search Form in the Middle -->
      <form class="d-flex mx-auto" role="search" action="/user_dashboard/{{ userid}}" method="post">
        <input class="form-control me-2" type="search" name="query" placeholder="Search" aria-label="Search">
        <button class="btn btn-outline-success" type="submit">
          <i class="bi bi-search"></i> Search
        </button>
      </form>

      <!-- Cart Button on the Right -->
      <ul class="navbar-nav ml-auto">
        <li class="nav-item">
    <a v-if="cart_value <= 0" class="nav-link" href="/cart/{{ userid }}">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="50"
        height="50"
        fill="currentColor"
        class="bi bi-cart3"
        viewBox="0 0 16 16"
      >
        <!-- SVG path for cart when cart_value <= 0 -->
      </svg>
      Cart (0)
    </a>
    <a v-else class="nav-link" href="/cart/{{ userid }}">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="50"
        height="50"
        fill="currentColor"
        class="bi bi-cart-check-fill"
        viewBox="0 0 16 16"
      >
        <!-- SVG path for cart when cart_value > 0 -->
      </svg>
      Cart ({{ cart_value }})
    </a>
  </li>
      </ul>
    </div>

  </div>
</nav>

    <div class="container mt-5">
      <!-- Render product list dynamically -->
      <div v-if="products.length > 0">
        <h1 class="mb-4">Product List</h1>
        <div v-for="category in categories" :key="category.id">
          <h3>Category: {{ category.name }}</h3>
          <div class="row">
            <div v-for="product in products" :key="product.id" v-if="product.category_id === category.id">
              <!-- Render individual product details -->
              <div class="col-md-4">
                <div class="card mb-4">
                  <div class="card-body">
                    <h5 class="card-title">{{ product.name }}</h5>
                    <!-- Render other product details -->
                    <!-- Add to cart link or button -->
                    <a v-if="product.quantity !== 0" :href="`/Add_to_cart/${userid}/${product.id}`">Add to cart (Qty 1)</a>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <!-- Show a message if there are no products -->
      <div v-else>
        <h1><p>No products available</p></h1>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ProductList',
  props: {
    name: String, // Assuming 'name' is passed as a prop
    userid: String, // Assuming 'userid' is passed as a prop
    cart_value: Number, // Assuming 'cart_value' is passed as a prop
  },
  data() {
    return {
      products: [],
      categories: [],
    };
  },
  created() {
    // Fetch data from Flask backend using Axios/Fetch
    // Example: Fetching product and category data from API endpoints
    // Replace 'YOUR_API_URL' with your actual API endpoint URLs
    this.fetchProducts();
    this.fetchCategories();
  },
  methods: {
    async fetchProducts() {
      try {
        const response = await fetch('YOUR_PRODUCTS_API_URL');
        if (response.ok) {
          const data = await response.json();
          this.products = data; // Assign fetched product data to 'products'
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
          this.categories = data; // Assign fetched category data to 'categories'
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