<template>
  <div>
    <a href="#/">Home</a> |
    <a href="#/crud">CRUD</a> |
    <a href="#/loop">Loops</a> |
    <a href="#/products">Prods</a>
    <component :is="currentView" />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import CRUDView from "@/components/CRUDView.vue";
import LoopsView from "@/components/LoopsView.vue";
import HelloWorld from "@/components/HelloWorld.vue";
import ProductsView from "@/components/ProductsView.vue";

const routes = {
  '/': HelloWorld,
  '/crud': CRUDView,
  '/loop': LoopsView,
  '/products':ProductsView,
  '/home': HelloWorld
};

const currentPath = ref(window.location.hash);

window.addEventListener('hashchange', () => {
  currentPath.value = window.location.hash;
});

const NotFound = { template: '<div>404 Not Found</div>' };

const currentView = computed(() => {
  return routes[currentPath.value.slice(1) || '/'] || NotFound;
});
</script>
