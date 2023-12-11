import { createRouter, createWebHistory } from 'vue-router'
import Home from "@/views/Home.vue";
import Login from "@/views/UserLogin.vue";
import Signup from "@/views/UserSignup.vue";
import UserSignup from "@/views/UserSignup.vue";
import UserDashboard from "@/views/UserDashboard.vue";
import AdminDashboard from "@/views/AdminDashboard.vue";

const routes = [
  // {
  //   path: '/',
  //   name: 'index',
  //   component: HomeView
  // },
  // {
  //   path: '/about',
  //   name: 'about',
  //   // route level code-splitting
  //   // this generates a separate chunk (about.[hash].js) for this route
  //   // which is lazy-loaded when the route is visited.
  //   component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  // },
  {
    path: '/',
    name: 'home',
    component: Home
  },
  {
    path: '/user-login',
    name: 'user-login',
    component: Login
  },
  {
    path:'/user-dashboard',
    name:'user-dashboard',
    component: UserDashboard
  },
    {
    path:'/user-signup',
    name:'user-signup',
    component: UserSignup
  },
    {
    path:'/admin-dashboard',
    name:'admin-dashboard',
    component: AdminDashboard
  },

]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
