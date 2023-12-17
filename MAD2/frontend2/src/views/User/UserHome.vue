<template>

    <div class="container mt-5">
  <div v-if="categories.length > 0">
    <h1 class="mb-4">Product List</h1>
    <div v-for="category in categories" :key="category.id">


      <h3>Category: {{ category.name[0].oldName }}</h3>
      <div class="row">
  <div v-for="(product, index) in products.filter(prod => prod?.category_id === category.id)" :key="product.id" class="col-md-4">
    <div class="card mb-5">
      <div class="card-body">
        <div v-if="product_quantity[product.id] > 0">
          <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="bi bi-cart-fill" viewBox="0 0 16 16" style="position: absolute; top: 5px; right: 50px;">
            <path d="M.5 1a.5.5 0 0 0 0 1h1.11l.401 1.607 1.498 7.985A.5.5 0 0 0 4 12h1a2 2 0 1 0 0 4 2 2 0 0 0 0-4h7a2 2 0 1 0 0 4 2 2 0 0 0 0-4h1a.5.5 0 0 0 .491-.408l1.5-8A.5.5 0 0 0 14.5 3H2.89l-.405-1.621A.5.5 0 0 0 2 1H.5zM6 14a1 1 0 1 1-2 0 1 1 0 0 1 2 0zm7 0a1 1 0 1 1-2 0 1 1 0 0 1 2 0zm-1.646-7.646-3 3a.5.5 0 0 1-.708 0l-1.5-1.5a.5.5 0 1 1 .708-.708L8 8.293l2.646-2.647a.5.5 0 0 1 .708.708z"/>
          </svg>
          <p>(Item Cart: {{ product_quantity[product.id] }})</p>
        </div>
<!--        <p>(Item Cart: {{ product_quantity[product.id] }})</p>-->
<!--        {{product_quantity}}-->
        <h3 class="card-title">{{ product.name }}</h3>
        <p class="card-text">Rate Per Unit: ₹{{ product.rate_per_unit }}</p>
        <p class="card-text">Quantity: {{ product.quantity ? product.quantity : 'Out of Stock' }}</p>
        <p class="card-text">Manufacture Date: {{ product.manufacture_date }}</p>
        <p class="card-text">Expiry Date: {{ product.expiry_date }}</p>
        <button v-if="product.quantity !== 0" @click="addCart(product.id)">Add to cart</button>
      </div>
    </div>
  </div>
</div>


    </div>

  </div>
      <!-- Show a message if there are no products -->

    </div>
</template>

<script>
import {fetchCategories} from "../../../api_helpers/helpers";

export default {
  name: 'ProductList',
  props: {
    name: String,
    userid: String,
  },
  data() {
    return {

      isNavbarOpen: false,
      products: [],
      categories: [],
      category_with_products: [],
      cart_value: 0,
      product_quantity: {}
    };
  },

  created() {
    this.fetchProducts();
    //this.fetchCategories();
  },
  mounted() {

    this.fetch_cart_quantity();
    this.fetch_product_quantity();
    this.assign();
  },
  methods: {

    async fetch_product_quantity(){
      const response = await fetch('http://127.0.0.1:5003/api/cart',{
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authentication-Token':JSON.parse(sessionStorage.getItem('token'))
        },
      });
      const cart_data = await response.json();
      if (response.ok) {
        //filter the data to get the product id


        this.products.forEach(product => {
  const cartProduct = cart_data.find(item => item.product_id === product.id);

  if (cartProduct) {
    this.product_quantity[product.id] = cartProduct.quantity;
  } else {
    this.product_quantity[product.id] = 0;
  }
});

        console.log(this.product_quantity)
      }
      else {
        console.error('Failed to fetch cart');
      }
    },
    async fetch_cart_quantity(){
      const response = await fetch('http://127.0.0.1:5003/api/cart',{
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authentication-Token':JSON.parse(sessionStorage.getItem('token'))
        },
      });
      const data = await response.json();
      if (response.ok) {
        this.cart_value = data.length;
        console.log(data.length)
      }
      else {
        console.error('Failed to fetch cart');
      }
    },

    async addCart(product_id) {
      try {
      const response = await fetch(`http://127.0.0.1:5003/api/cart`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authentication-Token':JSON.parse(sessionStorage.getItem('token'))
        },
        body: JSON.stringify({
          "product_id": product_id,
        }),
      });
        if (response.ok) {
          alert('Product added to cart');
          await this.fetch_cart_quantity();
          window.location.reload()
        }
        else {
          console.error('Failed to add product to cart');
        }
      }
      catch (error) {
        alert('Item quantity exceeded');
      }

    },
      async fetchProducts() {
        try {
          const response = await fetch('http://127.0.0.1:5003/api/products');
          const data = await response.json();
          if (response.ok) {
            this.products = data;
          }
          else {
            console.error('Failed to fetch products');
          }
        } catch (error) {
          console.error('Error fetching products:', error);
        }
      },

    async fetchCategoryProducts(category_id) {
      try {
        const response = await fetch(`http://127.0.0.1:5003/api/product/cat/${category_id}`);

        const data = await response.json();
        if (response.ok) {
          this.category_with_products = data;

        } else {
          console.error('Failed to fetch products');
        }
      }
      catch (error) {
        console.error('Error fetching products:', error);
      }
    },
    async logout() {
          sessionStorage.removeItem("token");
          const response = await fetch('http://127.0.0.1:5003/signout');
          if(response.ok){
            this.$router.push('/user-login');
            alert('Logout successful');
          }
          else{
            console.log(response)
            alert('Logout failed');
          }
          // console.log(sessionStorage.getItem("token"));

        },
    toggleNavbar() {
      this.isNavbarOpen = !this.isNavbarOpen;
    },
    async assign(){
      this.categories = await fetchCategories();
    }

  },
};
</script>