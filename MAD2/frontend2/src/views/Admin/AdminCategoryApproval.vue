<template>
  <div class="container mt-5">

    <h2>Pending Category Requests</h2>

    <!-- Create Category -->
    <h3 class="mt-5">Create Category Pending Requests</h3>

    <table v-if="pendingCategoriesCreate.length>0">
      <!-- Table headers -->
      <thead>
        <tr>
          <th>Category Name</th>
          <th>Requested By</th>
          <th>Actions</th>
        </tr>
      </thead>
      <!-- Table body for create category pending requests -->
      <tbody>
        <tr v-for="(category, index) in pendingCategoriesCreate" :key="index">
          <td>{{ category.name[0].oldName }}</td>
          <td>{{ category.requestedBy }}</td>
          <td>
            <button @click="approveCreateCategory(category.id)" class="btn btn-success">Approve</button>
            <button @click="rejectCreateCategory(category.id)" class="btn btn-danger">Reject</button>
          </td>
        </tr>
      </tbody>
    </table>
<!--    <table v-else class="alert alert-danger mt-4 py-5 px-5" role="alert">No requests pending</table>-->
    <div v-else class="alert alert-danger mt-4 " role="alert" style="width: 20%">No requests pending</div>

    <!-- Delete Category -->
    <h3 class="mt-5">Delete Category Pending Requests</h3>
    <table v-if="pendingCategoriesDelete.length>0" class="table">
      <!-- Table headers -->
      <thead>
        <tr>
          <th>Category Name</th>
          <th>Requested By</th>
          <th>Actions</th>
        </tr>
      </thead>
      <!-- Table body for delete category pending requests -->
      <tbody>
        <tr v-for="(category, index) in pendingCategoriesDelete" :key="index">
          <td>{{ category.name[0].oldName }}</td>
          <td>{{ category.requestedBy }}</td>
          <td>
            <button @click="approveDeleteCategory(category.id)" class="btn btn-success">Approve</button>
            <button @click="rejectDeleteCategory(category.id)" class="btn btn-danger">Reject</button>
          </td>
        </tr>
      </tbody>
    </table>
        <div v-else class="alert alert-danger mt-4 " role="alert" style="width: 20%">No requests pending</div>

    <!-- Edit Category -->
    <h3 class="mt-5">Edit Category Pending Requests</h3>
    <table v-if="pendingCategoriesEdit.length>0" class="table">
      <!-- Table headers -->
      <thead>
        <tr>
          <th>Old Name</th>
          <th>New Name</th>
          <th>Requested By</th>
          <th>Actions</th>
        </tr>
      </thead>
      <!-- Table body for edit category pending requests -->
      <tbody>
        <tr v-for="(category, index) in pendingCategoriesEdit" :key="index">
          <td>{{ category.name[0].oldName }}</td>
          <td>{{ category.name[0].newName }}</td>
          <td>{{ category.requestedBy }}</td>
          <td>
            <button @click="approveEditCategory(category.id)" class="btn btn-success">Approve</button>
            <button @click="rejectEditCategory(category.id)" class="btn btn-danger">Reject</button>
          </td>
        </tr>
      </tbody>
    </table>
        <div v-else class="alert alert-danger mt-4" role="alert" style="width: 20%">No requests pending</div>

  </div>
</template>


<script>
import { fetchPendingCategories} from '../../../api_helpers/helpers'
export default {
  data() {
    return {
      pendingCategories: [], // To store pending categories fetched from the backend
      pendingCategoriesCreate: [],
      pendingCategoriesEdit: [],
      pendingCategoriesDelete: [],
      categoryName: '',
      categoryId: ''
    };
  },
  methods: {
    async assign() {
      this.pendingCategories = await fetchPendingCategories()
      this.pendingCategoriesCreate = this.pendingCategories.filter(category => category.is_approved === 0),
          this.pendingCategoriesEdit = this.pendingCategories.filter(category => category.is_approved === -2),
          this.pendingCategoriesDelete = this.pendingCategories.filter(category => category.is_approved === -1)
    },
    async approveCreateCategory(categoryId) {
      // Your approval logic for Create category
      try {
        this.categoryId = this.pendingCategoriesCreate.find(category => category.id === categoryId).id;

        const response = await fetch(`http://127.0.0.1:5003/api/category/${this.categoryId}`, {
          method: 'PATCH',
          headers: {
            'Content-Type': 'application/json',
          },

          body: JSON.stringify({"is_approved": 1}),
        });
        const jsonResponse = await response.json();
        if (jsonResponse.message === 'something went wrong') {
          alert('Category already exists');
        } else {
          if (response.ok) {
            console.log('Category created successfully');
            alert('Category created successfully');
            window.location.href = '/admin-dashboard/Approve-Requests';
          }
        }
      } catch (error) {
        console.error('Error creating category:', error);
      }
    },
    async rejectCreateCategory(categoryId) {
      console.log(categoryId);
      // Your rejection logic for Create category
      try {
        this.categoryId = this.pendingCategoriesCreate.find(category => category.id === categoryId).id;

        const response = await fetch(`http://127.0.0.1:5003/api/category/${this.categoryId}`, {
          method: 'DELETE',
        });
        if (response.ok) {
          alert('Category rejected successfully');
          window.location.href = '/admin-dashboard/Approve-Requests';
        } else {
          console.error('Something went wrong');
        }
      } catch (error) {
        console.error('Error rejecting category:', error);
      }

    },
    async approveEditCategory(categoryId) {
      // Your approval logic for Edit category
      try {
        this.categoryId = this.pendingCategoriesEdit.find(category => category.id === categoryId).id;
        const name={
          "old_name": this.pendingCategoriesEdit.find(category => category.id === categoryId).name[0].newName,
          "new_name": this.pendingCategoriesEdit.find(category => category.id === categoryId).name[0].newName,
          "is_approved": 1
      }
        const response = await fetch(`http://127.0.0.1:5003/api/category/${this.categoryId}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },

          body: JSON.stringify(name),
        });
        const jsonResponse = await response.json();
        if (jsonResponse.message === 'something went wrong') {
          alert('Category already exists');
        } else {
          if (response.ok) {
            console.log('Category created successfully');
            alert('Request Approved successfully');
            window.location.href = '/admin-dashboard/Approve-Requests';
          }
        }
      } catch (error) {
        console.error('Error creating category:', error);
      }
    },
    async rejectEditCategory(categoryId) {
      // Your rejection logic for Edit category
      try {
        this.categoryId = this.pendingCategoriesEdit.find(category => category.id === categoryId).id;
        const name={
          "old_name": this.pendingCategoriesEdit.find(category => category.id === categoryId).name[0].oldName,
          "new_name": this.pendingCategoriesEdit.find(category => category.id === categoryId).name[0].oldName,
          "is_approved": 1
      }
        const response = await fetch(`http://127.0.0.1:5003/api/category/${this.categoryId}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },

          body: JSON.stringify(name),
        });
        const jsonResponse = await response.json();
        if (jsonResponse.message === 'something went wrong') {
          alert('Category already exists');
        } else {
          if (response.ok) {
            // console.log( 'Category created successfully');
            alert('Request Approved successfully');
            window.location.href = '/admin-dashboard/Approve-Requests';
          }
        }
      } catch (error) {
        console.error('Error creating category:', error);
      }
    },
    async approveDeleteCategory(categoryId) {
      // Your approval logic for Delete category
      try {

        this.categoryId = this.pendingCategoriesDelete.find(category => category.id === categoryId).id;
        console.log(this.categoryId);
        const response = await fetch(`http://127.0.0.1:5003/api/category/${this.categoryId}`, {
          method: 'DELETE',
        });
        if (response.ok) {
          alert('Category deleted successfully');
          window.location.href = '/admin-dashboard/Approve-Requests';
        } else {
          console.error('Something went wrong');
        }
      } catch (error) {
        console.error('Error deleting category:', error);
      }
    },
    async rejectDeleteCategory(categoryId) {
      // Your rejection logic for Delete category
      try {
        this.categoryId = this.pendingCategoriesDelete.find(category => category.id === categoryId).id;

        const response = await fetch(`http://127.0.0.1:5003/api/category/${this.categoryId}`, {
          method: 'PATCH',
          headers: {
            'Content-Type': 'application/json',
          },

          body: JSON.stringify({"is_approved": 1}),
        });
        const jsonResponse = await response.json();
        if (jsonResponse.message === 'something went wrong') {
          alert('Category already exists');
        } else {
          if (response.ok) {
            console.log('Category created successfully');
            alert('Request Rejected successfully');
            window.location.href = '/admin-dashboard/Approve-Requests';
          }
        }
      } catch (error) {
        console.error('Error creating category:', error);
      }
    },
  },
  mounted() {
      // Fetch pending categories when the component is mounted
      this.assign();
    }
}
</script>
