import {createRouter, createWebHistory} from 'vue-router'
import Home from "@/views/Home.vue";
import Login from "@/views/User/UserLogin.vue";
import Signup from "@/views/User/UserSignup.vue";
import UserSignup from "@/views/User/UserSignup.vue";
import UserDashboard from "@/views/User/UserDashboard.vue";
import AdminDashboard from "@/views/Admin/AdminDashboard.vue";
import UserLogin from "@/views/User/UserLogin.vue";
import AdminLogin from "@/views/Admin/AdminLogin.vue";
import ManagerLogin from "@/views/Manager/ManagerLogin.vue";
import ManagerSignup from "@/views/Manager/ManagerSignup.vue";
import ManagerDashboard from "@/views/Manager/ManagerDashboard.vue";
import CreateCategory from "@/views/Admin/CreateCategory.vue";
import DeleteCategory from "@/views/Admin/DeleteCategory.vue";
import EditCategory from "@/views/Admin/EditCategory.vue";
import CreateProduct from "@/views/Manager/CreateProduct.vue";
import DeleteProduct from "@/views/Manager/DeleteProduct.vue";
import EditProduct from "@/views/Manager/EditProduct.vue";
import ManagerCreateCategory from "@/views/Manager/ManagerCreateCategory.vue";
import ManagerPendingRequests from "@/views/Manager/ManagerPendingRequests.vue";
import AdminCategoryApproval from "@/views/Admin/AdminCategoryApproval.vue";

const routes = [

    {
        path: '/',
        name: 'home',
        component: Home
    },
    // User Functions
    {
        path: '/user-login',
        name: 'user-login',
        component: UserLogin
    },
    {
        path: '/user-dashboard',
        name: 'user-dashboard',
        component: UserDashboard
    },
    {
        path: '/user-signup',
        name: 'user-signup',
        component: UserSignup
    },

    // Manager Functions
    {
        path: '/manager-login',
        name: 'manager-login',
        component: ManagerLogin
    },
    {
        path: '/manager-signup',
        name: 'manager-signup',
        component: ManagerSignup
    },
    {
        path: '/manager-dashboard',
        name: 'manager-dashboard',
        component: ManagerDashboard,

    },
    {
        path: '/manager-dashboard/Create-Product',
        name: 'create-product',
        component: CreateProduct,
    },
    {
        path: '/manager-dashboard/Delete-Product',
        name: 'delete-product',
        component: DeleteProduct
    },
    {
        path: '/manager-dashboard/Edit-Product',
        name: 'edit-product',
        component: EditProduct
    },
    {
        path: '/manager-dashboard/Create-Category',
        name: 'manager-create-category',
        component: ManagerCreateCategory,

    },
    {
        path: '/manager-dashboard/Manager-PendingRequests',
        name: 'manager-pending-requests',
        component: ManagerPendingRequests,

    },

    // Admin Functions
    {
        path: '/admin-login',
        name: 'admin-login',
        component: AdminLogin
    },
    {
        path: '/admin-dashboard',
        name: 'admin-dashboard',
        component: AdminDashboard
    },
    {
        path: '/admin-dashboard/Create-Category',
        name: 'admin-create-category',
        component: CreateCategory
    },
    {
        path: '/admin-dashboard/Delete-Category',
        name: 'admin-delete-category',
        component: DeleteCategory
    },
    {
        path: '/admin-dashboard/Edit-Category',
        name: 'admin-edit-category',
        component: EditCategory
    },
    {
        path: '/admin-dashboard/Approve-Requests',
        name: 'admin-approve-category',
        component: AdminCategoryApproval
    },


]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})

export default router
