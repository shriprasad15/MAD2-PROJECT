<!--<script setup>-->
<!--const { todo } = defineProps({-->
<!--  todo: Object-->
<!--})-->
<!--</script>-->

<!--<template>-->
<!--  <li>{{ todo.text }}</li>-->
<!--</template>-->

<script setup>
import { defineProps } from 'vue';

const props = defineProps({
  todo: Object
});
</script>

<template>
  <li>{{ props.todo.text }}</li>
</template>