<template>
  <div>
    <h1>Pending Category Creation Requests</h1>
    <table class="table">
      <thead>
        <tr>
          <th>Category Name</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <!-- Loop through pending requests -->
        <tr v-for="(category, index) in pendingCategories" :key="index">
          <td>{{ category.name }}</td>
          <td>
            <!-- Provide admin options for approval/rejection -->
            <button @click="approveCategory(category.id)" class="btn btn-success">Approve</button>
            <button @click="rejectCategory(category.id)" class="btn btn-danger">Reject</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  data() {
    return {
      pendingCategories: [], // To store pending categories fetched from the backend
    };
  },
  methods: {
    async fetchPendingCategories() {
      try {
        // Fetch pending category creation requests from the backend
        const response = await fetch('http://127.0.0.1:5003/api/admin/pending-categories');
        const data = await response.json();
        this.pendingCategories = data.pendingCategories; // Assuming the backend sends an array of pending categories
      } catch (error) {
        console.error('Error fetching pending categories:', error);
      }
    },
    async approveCategory(categoryId) {
      try {
        // Send request to approve category with categoryId to the backend
        const response = await fetch(`http://127.0.0.1:5003/api/admin/approve-category/${categoryId}`, {
          method: 'PUT',
        });
        if (response.ok) {
          console.log('Category approved successfully');
          // After approval, fetch pending categories again to update the list
          this.fetchPendingCategories();
        }
      } catch (error) {
        console.error('Error approving category:', error);
      }
    },
    async rejectCategory(categoryId) {
      try {
        // Send request to reject category with categoryId to the backend
        const response = await fetch(`http://127.0.0.1:5003/api/admin/reject-category/${categoryId}`, {
          method: 'PUT',
        });
        if (response.ok) {
          console.log('Category rejected successfully');
          // After rejection, fetch pending categories again to update the list
          this.fetchPendingCategories();
        }
      } catch (error) {
        console.error('Error rejecting category:', error);
      }
    },
  },
  mounted() {
    // Fetch pending categories when the component is mounted
    this.fetchPendingCategories();
  },
};
</script>
