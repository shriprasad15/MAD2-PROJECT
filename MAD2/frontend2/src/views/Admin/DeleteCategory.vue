<template>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet"
          integrity="sha384-9ndCyUaIbzAi2FUVXJi0CjmCapSmO7SnpJef0486qhLnuZ2cdeRhO02iuK6FUUVM" crossorigin="anonymous">
  <div>
    <h1>Admin dashboard</h1>

    <form @submit.prevent="deleteCategory" class="mb-5">
      <h3>Delete Category</h3>
      <h5>Select Category to delete</h5>
      <div class="dropdown">
        <button class="btn btn-secondary dropdown-toggle" type="button" @click="toggleDropdown">
          {{ selectedCategory ? selectedCategory : 'Select Category to delete' }}
        </button>
        <ul v-if="showDropdown" class="dropdown-menu">
          <li v-for="item in dropdownItems" :key="item.id">
            <button @click="selectCategory(item.name)" class="dropdown-item" type="button" data-bs-toggle="modal" :data-bs-target="'#exampleModal' + item.name">
              {{ item.name }}
            </button>
          </li>
        </ul>
      </div>

      <div v-for="item in dropdownItems" :key="item.id" class="modal fade" :id="'exampleModal' + item.name" tabindex="-1" :aria-labelledby="'exampleModalLabel' + item.name" aria-hidden="true">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title" :id="'exampleModalLabel' + item.name">Deleting Item</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
              Are you sure you want to delete {{ item.name }}?
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
              <form @submit.prevent="confirmDelete(item.name)">
                <button type="submit" class="btn btn-danger">Confirm</button>
              </form>
            </div>
          </div>
        </div>
      </div>

      <br>
      <router-link to="/admin-dashboard">
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
      dropdownItems: [],
      selectedCategory: null,
      showDropdown: false,
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
    async deleteCategory() {
      try {
        if (!this.selectedCategory) {
          console.error('Please select a category');
          return;
        }
        const response = await fetch(`http://127.0.0.1:5003/api/category/${this.selectedCategory.id}`, {
          method: 'DELETE',
        });
        if (response.ok) {
          console.log(`Category '${this.selectedCategory.name}' deleted successfully`);
          this.selectedCategory = null;
          // Refetch categories after deletion
          this.assign();
        } else {
          console.error('Failed to delete category');
        }
      } catch (error) {
        console.error('Error deleting category:', error);
      }
    },
    async confirmDelete(category) {
      this.selectedCategory = category;
      this.showDropdown = false;
      await this.deleteCategory();
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

