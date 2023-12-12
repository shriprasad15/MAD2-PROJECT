<template>
<!--  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet"-->
<!--          integrity="sha384-9ndCyUaIbzAi2FUVXJi0CjmCapSmO7SnpJef0486qhLnuZ2cdeRhO02iuK6FUUVM" crossorigin="anonymous">-->
  <div>
    <h1>Admin dashboard</h1>

    <form @submit.prevent="editCategory" class="mb-5">
      <h3>Edit Category</h3>
      <div class="form-floating">
        <input type="text" class="form-control" v-model="categoryName" id="floatingText" required>
        <label for="floatingText">Enter new name</label>
      </div>
      <br>

      <div class="dropdown">
        <button class="btn btn-secondary dropdown-toggle" type="button" @click="toggleDropdown" aria-expanded="false">
          Select Category to change the name for
        </button>
        <ul v-if="showDropdown" class="dropdown-menu">
          <li v-for="item in dropdownItems" :key="item.id">
            <button @click="selectCategory(item)" class="dropdown-item" type="button">
              {{ item.name }}
            </button>
          </li>
        </ul>
      </div>
      <br>
      <router-link to="/admin_dashboard">
        <button type="button" class="btn btn-primary" style="background-color: #6F4E37; color: white;">Back</button>
      </router-link>
    </form>
  </div>
</template>

<script>
import { fetchCategories } from "../../../api_helpers/helpers";

export default {
  data() {
    return {
      categoryName: "",
      dropdownItems: [],
      selectedCategory: null,
      showDropdown: true,
    };
  },
  methods: {
    toggleDropdown() {
      this.showDropdown = !this.showDropdown;
    },
    selectCategory(category) {
      this.selectedCategory = category;
      this.showDropdown = false;
    },
    async editCategory() {
      try {
        if (!this.selectedCategory || !this.categoryName) {
          console.error('Please select a category and enter a new name');
          return;
        }
        const response = await fetch(`http://127.0.0.1:5003/api/category/${this.selectedCategory.id}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ name: this.categoryName }),
        });
        if (response.ok) {
          console.log(`Category '${this.selectedCategory.name}' edited successfully`);
          this.selectedCategory = null;
          this.categoryName = ""; // Clear input after editing
          // Refetch categories after editing
          await this.assign();
        } else {
          console.error('Failed to edit category');
        }
      } catch (error) {
        console.error('Error editing category:', error);
      }
    },
    async assign() {
      try {
        this.dropdownItems = await fetchCategories();
      } catch (error) {
        console.error('Error fetching categories:', error);
      }
    },
  },
  mounted() {
    this.assign();
  },
};
</script>

<style>
/* Your component-specific styles can be added here */
</style>
