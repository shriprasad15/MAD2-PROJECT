<template>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet"
        integrity="sha384-9ndCyUaIbzAi2FUVXJi0CjmCapSmO7SnpJef0486qhLnuZ2cdeRhO02iuK6FUUVM" crossorigin="anonymous">
  <div>
    <h1>Admin dashboard</h1>
    <form @submit.prevent="submitProduct" class="pt-4">
      <h3>Edit Product</h3>
      <h5>Select Product to edit</h5>
      <select v-model="selectedProductId" style="height: 40px;">
        <option v-for="item in product_items" :key="item.id" :value="item.id">{{ item.name }}</option>
      </select>


      <div class="form-floating mb-3">
        <br />
        <input type="text" aria-label="Category Name" v-model="newProductName" class="form-control" />
        <label for="floatingInput">Product New Name</label>
      </div>

      <div>
        <label for="m_date">Manufacture date:</label><br />
        <input type="date" id="m_date" v-model="manufactureDate" />
      </div>
      <br />

      <div>
        <label for="e_date">Expiry date:</label><br />
        <input type="date" id="e_date" v-model="expiryDate" />
      </div>
      <br />

      <div class="form-floating mb-3">
        <input type="number" class="form-control" v-model="ratePerUnit" />
        <label for="floatingInput">Rate per Unit</label>
      </div>

      <div class="form-floating mb-3">
        <input type="number" class="form-control" v-model="quantity" />
        <label for="floatingInput">Quantity</label>
      </div>

      <div>
        <h5>Change Category</h5>
        <p>Current Category: {{ getCategoryName(selectedProductId) }}</p>
        <select v-model="newCategoryId" style="height: 40px;">
          <option value="">-- Select New Category --</option>
          <option v-for="item in category_items" :key="item.id" :value="item.id">{{ item.name }}</option>
        </select>
      </div>

      <div class="pt-1 mb-4">
        <button class="btn btn-lg btn-block" type="submit" style="background-color: #6F4E37; color: white;">Submit</button>
      </div>
      <a href="/manager-dashboard">
        <button type="button" class="btn btn-primary" style="background-color: #6F4E37; color: white;">Back</button>
      </a>
    </form>

    <div v-if="msg" class="alert alert-success" role="alert">{{ msg }}</div>
    <div v-if="error" class="alert alert-danger mt-3" role="alert">{{ error }}</div>
  </div>
</template>

<script>
import { fetchCategories,fetchProducts, updateProduct } from '../../../api_helpers/helpers'; // Replace './api' with your actual API module path

export default {
  data() {
    return {
      selectedProductId: null,
      product_items: [],
      category_items: [],
      newProductName: '',
      manufactureDate: '',
      expiryDate: '',
      ratePerUnit: null,
      quantity: null,
      newCategoryId: '',
      msg: '',
      error: '',
    };
  },
  methods: {
    getCategoryName(productId) {
      const selectedProductId = this.product_items.find(item => item.id === productId);
      if (selectedProductId) {
        const categoryId = selectedProductId.categoryId;
        const category = this.category_items.find(cat => cat.id === categoryId);
        return category ? category.name : '';
      }
      return '';
    },

    async populateProductDetails() {
      console.log(this.selectedProductId);
      try {
        const selectedProduct = this.product_items.find(item => item.id === this.selectedProductId);
        if (selectedProduct) {
          this.newProductName = selectedProduct.name;
          this.manufactureDate = selectedProduct.manufactureDate;
          this.expiryDate = selectedProduct.expiryDate;
          this.ratePerUnit = selectedProduct.rate;
          this.quantity = selectedProduct.quantity;
          this.newCategoryId = selectedProduct.categoryId;
        }
      } catch (error) {
        console.error('Error populating product details:', error);
        this.error = 'Error populating product details';
      }
    },


    async assignProducts() {
      try {
        this.product_items = await fetchProducts();
        // Populate category_items similarly based on your API response
      } catch (error) {
        console.error('Error fetching products:', error);
        this.error = 'Error fetching products';
      }
    },
    async assignCategories() {
      try {
        this.category_items = await fetchCategories();
        // Populate category_items similarly based on your API response
      } catch (error) {
        console.error('Error fetching categories:', error);
        this.error = 'Error fetching categories';
      }
    },

    async submitProduct() {
      try {
        const productData = {
          prod_name: this.newProductName,
          mdate: this.manufactureDate,
          edate: this.expiryDate,
          rate: this.ratePerUnit,
          quantity: this.quantity,
          cat_id: this.newCategoryId,
        };

        const response = await updateProduct(prod_id, productData); // Replace 'updateProduct' with your API call function
        if (response.ok) {
          this.msg = `Product updated successfully`;
          // Reset form fields or perform any other necessary actions after successful update
        } else {
          this.error = 'Failed to update product';
        }
      } catch (error) {
        console.error('Error updating product:', error);
        this.error = 'Error updating product';
      }
    },
  },
  mounted() {
    this.assignProducts();
    this.assignCategories()
    this.populateProductDetails();
  },
};
</script>
