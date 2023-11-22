<template>
  <div>
    <h1>Products</h1>
    <ul>
      <li v-for="product in products" :key="product.id">
        <h3>{{ product.name }}</h3>
        <p>Manufacture Date: {{ product.manufacture_date }}</p>
        <p>Expiry Date: {{ product.expiry_date }}</p>
        <p>Rate per Unit: ${{ product.rate_per_unit }}</p>
        <p>Quantity: {{ product.quantity }}</p>
        <p>Category ID: {{ product.category_id }}</p>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  data() {
    return {
      products: [] // Initialize as an empty array to hold fetched products
    };
  },
  mounted() {
    // Fetch data when the component is mounted
    this.fetchProducts();
  },
  methods: {
    fetchProducts() {
      var requestOptions = {
        method: 'GET',
        redirect: 'follow'
      };

      fetch("http://127.0.0.1:8081/product/1", requestOptions)
        .then(response => response.json())
        .then(result => {
          // Set the fetched products to the 'products' array
          this.products = result;
        })
        .catch(error => console.log('error', error));
    }
  }
};
</script>
