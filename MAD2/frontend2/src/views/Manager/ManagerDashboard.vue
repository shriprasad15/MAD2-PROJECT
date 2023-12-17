<template>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet"
          integrity="sha384-9ndCyUaIbzAi2FUVXJi0CjmCapSmO7SnpJef0486qhLnuZ2cdeRhO02iuK6FUUVM" crossorigin="anonymous">

    <h1>Manager dashboard</h1>
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
      <div class="container-fluid">
        <button class="navbar-toggler" type="button" @click="toggleNavbar">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" :class="{ 'show': isNavbarOpen }" id="navbarNavDropdown">
          <ul class="navbar-nav">
            <li class="nav-item">
              <router-link to="/manager-dashboard" class="nav-link" aria-current="page">Home</router-link>
            </li>

            <li class="nav-item dropdown" @mouseover="openProductDropdown" @mouseleave="closeProductDropdown">
              <a class="nav-link dropdown-toggle" role="button" @click.prevent>
                Product Operations
              </a>
              <div class="dropdown-menu" v-show="isProductDropdownOpen" @mouseover="openProductDropdown" @mouseleave="closeProductDropdown">
                <router-link v-for="item in productItems" :key="item" :to="`/manager-dashboard/${item}`" class="dropdown-item">{{ item }}</router-link>
              </div>
            </li>

            <li class="nav-item dropdown" @mouseover="openCategoryDropdown" @mouseleave="closeCategoryDropdown">
              <a class="nav-link dropdown-toggle" role="button" @click.prevent>
                Category Operations
              </a>
              <ul class="dropdown-menu" :class="{ 'show': isCategoryDropdownOpen }">
                <li v-for="item in categoryItems" :key="item">
                  <router-link :to="`/manager-dashboard/${item}`" class="dropdown-item">{{ item }}</router-link>
                </li>
              </ul>
            </li>
            <li class="nav-item">
              <router-link to="/manager-dashboard/Manager-PendingRequests" class="nav-link" aria-current="page">Pending Requests</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/summary" class="nav-link" aria-current="page">Summary</router-link>
            </li>
            <li class="nav-item">
              <button @click="logout" class="nav-link" >Logout</button>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <RouterView/>
</template>

<script>
import {fetchCategories, fetchPendingCategories, fetchProducts} from "../../../api_helpers/helpers";
export default {

  name: 'ProductList',
  props: {
    msg: String,
    error: String,

  },
  data() {
    return {
      isNavbarOpen: false,
      isCategoryDropdownOpen: false,
      isProductDropdownOpen: false,
      productItems: ['Create-Product', 'Delete-Product', 'Edit-Product'],
      categoryItems: ['Create-Category', 'Delete-Category', 'Edit-Category'],
      category_items: [],
      product_items: [],
    };
  },
  
  mounted() {
    this.assign();
  },
  methods: {
    async  logout() {
          sessionStorage.setItem("token", JSON.stringify(""));
          const response = await fetch('http://127.0.0.1:5003/signout');
          if(response.ok){
            this.$router.push('/manager-login');
            alert('Logout successful');
          }
          else{
            console.log(response)
            alert('Logout failed');
          }
          // console.log(sessionStorage.getItem("token"));

        },
    async assign() {
      this.category_items = await fetchCategories();
      this.product_items= await fetchProducts();
    },
    toggleNavbar() {
      this.isNavbarOpen = !this.isNavbarOpen;
    },
    openProductDropdown() {
      this.isProductDropdownOpen = true;
    },
    closeProductDropdown() {
      this.isProductDropdownOpen = false;
    },
    openCategoryDropdown() {
      this.isProductDropdownOpen = true;
    },
    closeCategoryDropdown() {
      this.isProductDropdownOpen = false;
    },
  },
};
</script>


<style>
.dropdown:hover .dropdown-menu {
  display: block;
}
</style>