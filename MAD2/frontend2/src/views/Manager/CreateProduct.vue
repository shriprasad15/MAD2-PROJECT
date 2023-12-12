<template>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet"
          integrity="sha384-9ndCyUaIbzAi2FUVXJi0CjmCapSmO7SnpJef0486qhLnuZ2cdeRhO02iuK6FUUVM" crossorigin="anonymous">
  <div>
    <h1>Manager dashboard</h1>

    <form @submit.prevent="editProduct" class="mb-5">
      <h3>Edit Product</h3>
      <h5>Select Product to Edit</h5>
      <select v-model="selectedProductName" style="height: 40px;">
        <option v-for="item in dropdownItems" :key="item.id" :value="item.name">{{ item.name }}</option>
      </select>

      <div class="form-floating mb-3">
        <input type="text" aria-label="Category Name" v-model="newProductName" class="form-control">
        <label for="floatingInput">Product New Name</label>
      </div>

      <div>
        <label for="m_date">Manufacture date:</label><br>
        <input type="date" id="m_date" v-model="manufactureDate" name="manufacture_date">
      </div>

      <br>

      <div>
        <label for="e_date">Expiry date:</label><br>
        <input type="date" id="e_date" v-model="expiryDate" name="expiry_date">
      </div><br>

      <div class="form-floating mb-3">
        <input type="number" class="form-control" v-model="ratePerUnit" name='rate_per_unit'>
        <label for="floatingInput">Rate per Unit</label>
      </div>

      <div class="form-floating mb-3">
        <input type="number" class="form-control" v-model="quantity" name='quantity'>
        <label for="floatingInput">Quantity</label>
      </div>

      <div class="pt-1 mb-4">
        <button class="btn btn-lg btn-block" type="submit" style="background-color: #6F4E37; color: white;">Submit</button>
      </div>

      <router-link to="/manager-dashboard">
        <button type="button" class="btn btn-primary" style="background-color: #6F4E37; color: white;">Back</button>
      </router-link>
    </form>

    <div v-if="msg" class="alert alert-success" role="alert">{{ msg }}</div>
    <div v-if="error" class="alert alert-danger mt-3" role="alert">{{ error }}</div>
  </div>
</template>

<script>
import { fetchCategories } from "../../../api_helpers/helpers";

export default {
  data() {
    return {
      dropdownItems: [],
      selectedCategory: null,
      productName: '',
      manufactureDate: '',
      expiryDate: '',
      ratePerUnit: 0,
      quantity: 0,
      msg: '',
      error: '',
    };
  },
  methods: {
    async addProductToCategory() {
      try {
        if (!this.productName.trim()) {
          console.error('Product name cannot be empty');
          return;
        }

        if (!this.selectedCategory) {
          console.error('Please select a category');
          return;
        }
        console.log(this.selectedCategory);
        const response = await fetch(`http://127.0.0.1:5003/api/product/cat/${this.selectedCategory.id}`, {

          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            name: this.productName,
            manufactureDate: this.manufactureDate,
            expiryDate: this.expiryDate,
            ratePerUnit: this.ratePerUnit,
            quantity: this.quantity,
          }),
        });

        if (response.ok) {
          console.log('Product added to category successfully');
          this.productName = '';
          this.manufactureDate = '';
          this.expiryDate = '';
          this.ratePerUnit = 0;
          this.quantity = 0;
          // Handle other success logic if needed
        } else {
          console.error('Failed to add product to category');
          // Handle error scenarios or show error messages
        }
      } catch (error) {
        console.error('Error adding product to category:', error);
        // Handle error scenarios or show error messages
      }
    },

    async assignCategories() {
      try {
        this.dropdownItems = await fetchCategories();
      } catch (error) {
        console.error('Error fetching categories:', error);
        // Handle error scenarios or show error messages
      }
    },
  },
  mounted() {
    this.assignCategories();
  },
};
</script>
