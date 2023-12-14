<template>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet"
        integrity="sha384-9ndCyUaIbzAi2FUVXJi0CjmCapSmO7SnpJef0486qhLnuZ2cdeRhO02iuK6FUUVM" crossorigin="anonymous">
  <div>

    <form @submit.prevent="showEditConfirmation" class="mb-5">
      <h3>Edit Category</h3>
      <h5>Enter new category name: </h5>
      <input v-model="newCategoryName">
      <br><br>
      <h5>Select category to change the name: </h5>
      <div>
        <select v-model="selectedCategory" class="form-select">
          <option value="" disabled>Select Category to edit</option>
          <option v-for="item in dropdownItems" :key="item.id" :value="item.id">{{ item.name }}</option>
        </select>
      </div>
      <br>
      <div>
        <button type="submit" class="btn btn-primary">Edit Category</button>
      </div>

      <div v-if="editConfirmationBox" class="alert alert-warning mt-3" role="alert">
        Are you sure you want to edit "{{ selectedCategoryName }}" to "{{ newCategoryName }}"?
        <button @click="confirmEdit" class="btn btn-warning btn-sm ms-2">Confirm</button>
        <button @click="cancelEdit" class="btn btn-secondary btn-sm ms-2">Cancel</button>
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
      selectedCategory: null, // Store only the ID of the selected category
      selectedCategoryName: '', // Store the name of the selected category
      newCategoryName: '', // Store the new category name from input
      editConfirmationBox: false, // Control visibility of the edit confirmation dialog
    };
  },
  methods: {
    async showEditConfirmation() {
      if (!this.selectedCategory || !this.newCategoryName) {
        alert('Please select a category and enter a new name');
        return;
      }

      const selected = this.dropdownItems.find(item => item.id === this.selectedCategory);
      if (selected) {
        this.selectedCategoryName = selected.name;
        this.editConfirmationBox = true;
      }
    },

    async editCategory() {
      try {
        const response = await fetch(`http://127.0.0.1:5003/api/category/${this.selectedCategory}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ edit_cat: this.newCategoryName }),
        });

        if (response.ok) {
          this.selectedCategory = null;
          this.editConfirmationBox = false;
          await this.fetchAndSetCategories();
          alert(`Category '${this.selectedCategoryName}' edited successfully to '${this.newCategoryName}'`);
          this.selectedCategoryName = '';
          this.newCategoryName = '';
        } else {
          console.error('Failed to edit category');
        }
      } catch (error) {
        console.error('Error editing category:', error);
      }
    },

    confirmEdit() {
      this.editCategory();
    },

    cancelEdit() {
      this.editConfirmationBox = false;
    },

    async fetchAndSetCategories() {
      try {
        this.dropdownItems = await fetchCategories();
      } catch (error) {
        console.error('Error fetching categories:', error);
      }
    },
  },
  mounted() {
    this.fetchAndSetCategories();
  },
};
</script>
